from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType, BooleanType
from pyspark.sql import Row
from pyspark.sql.functions import randn, rand, explode


#
headers = {
    'content-type': "application/json"
}

body = json.dumps({
})

# response function - udf
def executeRestApi(verb, url, headers, body):
  res = None
  # Make API request, get response object back, create dataframe from above schema.
  try:
    if verb == "get":
      res = requests.get(url, data=body, headers=headers)
    elif verb == "post":
      res = requests.post(url, data=body, headers=headers)
    else:
      print("another HTTP verb action")
  except Exception as e:
    return e

  if res != None and res.status_code == 200:
    return json.loads(res.text)

  return None


# 
#udf_executeRestApi = udf(executeRestApi, new_schema)

spark = SparkSession.builder.appName("UDF REST Demo").getOrCreate()

jsonSchema = spark.read.json('response.json').schema

print(jsonSchema)

udf_executeRestApi = udf(executeRestApi, jsonSchema)

#Get initial list of forces
reqForces = requests.get('https://data.police.uk/api/crimes-street-dates')
jsonForces = reqForces.json()

overall_request_df =  spark.createDataFrame([], StructType([]))
#overall_request_df.printSchema()


#Requests
RestApiRequest = Row("verb", "url", "headers", "body")
for month in jsonForces:
  print(month)
  if str(month['date']) > '2021-09':
    print(month['date'])
    for force in month['stop-and-search']:
      print(force)
      newdf = spark.createDataFrame([RestApiRequest("get", 'https://data.police.uk/api/stops-force?force=' + str(force) + '&date=' + str(month['date']), headers, body)
      ])\
      .withColumn("execute", udf_executeRestApi(col("verb"), col("url"), col("headers"), col("body")))
      overall_request_df = overall_request_df.unionByName(newdf, allowMissingColumns=True)
      overall_request_df.show()
      """ overall_request_df.select(col('execute')).show(truncate=False) """


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


_columns_to_select = []
_all_columns = get_all_columns_from_schema(jsonSchema)
for column_collection in _all_columns:
  print('columsn collection', column_collection)
  if len(column_collection) > 1:
    _columns_to_select.append(col('.'.join(column_collection)).alias('_'.join(column_collection)))
  else:
    _columns_to_select.append(col(column_collection[0]))

print('list', _columns_to_select)
""" df = overall_request_df(explode(col('execute')))
df.select(get_all_columns_from_schema(jsonSchema)) """
print(get_all_columns_from_schema(jsonSchema))
df_col = overall_request_df.select(col('execute'))
collapsed_df = df_col.select(_columns_to_select)
collapsed_df.show()


"""                 df = overall_request_df.select(explode(col("execut")))
                df.show() """
"""                 df.select(collapse_columns(df.jsonSchema)).show() """
"""                 overall_request_df = overall_request_df.unionByName(newdf, allowMissingColumns=True)
                overall_request_df.select(col('execute.gender'),col(overall_request_df.outcome)) """
                
            
spark.stop()
