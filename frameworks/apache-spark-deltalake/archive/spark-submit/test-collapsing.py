
  
from pyspark.sql import SparkSession
#from pyspark import DBUtils
from pyspark.sql.functions import col
from pyspark.sql.types import StructType

spark = SparkSession.builder.getOrCreate()

# declare dummy data to demonstrate how the collapse mechanism works
jsonStrings = [{'"age_range":"18-24","outcome":"A no further action disposal","involved_person":true,"self_defined_ethnicity":"Other ethnic group - Not stated","gender":"Male","legislation":"Misuse of Drugs Act 1971 (section 23)","outcome_linked_to_object_of_search":false,"datetime":"2021-10-01T00:15:00+00:00","removal_of_more_than_outer_clothing":false,"outcome_object":{"id":"bu-no-further-action","name":"A no further action disposal"},"location":{"latitude":"54.769980","street":{"id":666241,"name":"On or near Sports\/Recreation Area"},"longitude":"-1.558844"},"operation":null,"officer_defined_ethnicity":"Black","type":"Person search","operation_name":null,"object_of_search":"Controlled drugs"'}]

otherPeopleRDD = spark.sparkContext.parallelize(jsonStrings)
df = spark.read.json(otherPeopleRDD)
  
# Recursively iterates over the schema, creating an array of arrays, whereby each item
# of the master array, is an array of column names
#
# For example, lets say there are three columns of which two are hierarchical and the following schema/structure
#    name
#    address
#      street
#      town
#    details
#      age
#      gender
#
# The function will return the following array:
# [["name"],["address","street"],["address","town"],["details","age"],["details","gender"]]
def get_all_columns_from_schema(source_schema):
  branches = []
  def inner_get(schema, ancestor=None):
    if ancestor is None: ancestor = []
    for field in schema.fields:
      branch_path = ancestor+[field.name]     
      if isinstance(field.dataType, StructType):    
        inner_get(field.dataType, branch_path) 
      else:
        branches.append(branch_path)
        
  inner_get(source_schema)
        
  return branches

# collapse_columns is passed the dataframe schema, which is then passes
# to get_all_columns_from_schema.  On return, it iterates through the array
# of columns in order to build up the select list that will be used
# to collapse the hierarchical columns into a single 2d structure
#
# for example, lets say _all_columns has the following array: [["name"],["address","street"]]
# after iterating through the array, the function response will be
# [col("name"), col("address.street").alias("address_street")]
def collapse_columns(source_schema, columnFilter=None):
  _columns_to_select = []
  if columnFilter is None: columnFilter = ""
  _all_columns = get_all_columns_from_schema(source_schema)
  for column_collection in _all_columns:
    if (len(columnFilter) > 0) & (column_collection[0] != columnFilter): 
        continue

    if len(column_collection) > 1:
      _columns_to_select.append(col('.'.join(column_collection)).alias('_'.join(column_collection)))
    else:
      _columns_to_select.append(col(column_collection[0]))

  return _columns_to_select

# as above but for individual columns
def collapse_column(source_df, source_column):
    column_name = ""
    if isinstance(source_column, Column):
      column_name = source_column.name
    else:
      column_name = source_column

    return collapse_columns(source_df.schema, column_name)

# returns a dataframe that has been collapsed.  Input is the dataframe to be collapsed
def collapse_to_dataframe(source_df):
  return source_df.select(collapse_columns(source_df.schema))
  
# now test
collapse_to_dataframe(df).show()