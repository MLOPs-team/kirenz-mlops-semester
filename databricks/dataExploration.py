# Databricks notebook source
import numpy as np
import pandas as pd
import json

# Read json stop and searches

#Read Raw Data from JSON File, which was acquired in a separate script
rawdf = spark.read.json("/FileStore/shared_uploads/dataForces_2.json")
rawdf.printSchema()
rawdf.show()

# Write the raw data to its target in the delta lake
rawdf.write \
  .format('delta') \
  .mode('overwrite') \
  .save('s3a://delta-lake-mlops/dataForcesRaw')

# COMMAND ----------


# delete all rows with null values in the following columns
df_cleared = rawdf.na.drop(subset=["age_range","gender","officer_defined_ethnicity","self_defined_ethnicity","object_of_search","location","legislation"])

# COMMAND ----------

# Split the DataFrame into noAction = 0 and Action = 1
from pyspark.sql.functions import when, lit

#Introdurce new Column action for usage as a label for the classification later
df_cleared.withColumn("action", \
                     when((df_cleared.outcome == "A no further action disposal"), lit(0)) \
                     .otherwise(lit(1)))

#@passer pyspark is lit ;)

# COMMAND ----------

# Normalize DataFrame 
df_clean = df_cleared.drop('outcome','outcome_linked_to_object_of_search', 'datetime', 'removal_of_more_than_outer_clothing', 'outcome_object',  'operation', 'operation_name', 'location')

# COMMAND ----------

#Set Self Defined Ethnicity in new column to group people by their ethnicity
#This might be slightly racist, there also might be a more elegant way of doing this but it works
df_clean.withColumn("self_defined_ethnicity_white", \
                     when(((df_cleared.self_defined_ethnicity == 'White - English/Welsh/Scottish/Northern Irish/British') | \
                           (df_cleared.self_defined_ethnicity == 'White - Any other White background') | (df_cleared.self_defined_ethnicity=='White - Irish') | \
                           (df_cleared.self_defined_ethnicity == 'White - Irish') | (df_cleared.self_defined_ethnicity == 'White - Gypsy or Irish Traveller')), lit(1)) \
                     .otherwise(lit(0)))

df_clean = df_clean.withColumn("self_defined_ethnicity_black", \
                    when(((df_cleared.self_defined_ethnicity == 'Black/African/Caribbean/Black British - Any other Black/African/Caribbean background') | \
                         (df_cleared.self_defined_ethnicity == 'Black/African/Caribbean/Black British - African') | \
                         (df_cleared.self_defined_ethnicity == 'Black/African/Caribbean/Black British - Caribbean')), lit(1)) \
                         .otherwise(lit(0)))

df_clean = df_clean.withColumn("self_defined_ethnicity_asian", \
                    when(((df_cleared.self_defined_ethnicity == 'Asian/Asian British - Any other Asian background') | \
                         (df_cleared.self_defined_ethnicity == 'Asian/Asian British - Pakistani') | \
                         (df_cleared.self_defined_ethnicity == 'Asian/Asian British - Bangladeshi') | \
                         (df_cleared.self_defined_ethnicity == 'Asian/Asian British - Indian') | \
                         (df_cleared.self_defined_ethnicity == 'Asian/Asian British - Chinese')), lit(1)) \
                         .otherwise(lit(0)))

df_clean = df_clean.withColumn("self_defined_ethnicity_other", \
                    when(((df_cleared.self_defined_ethnicity == 'Other ethnic group - Not stated') | \
                         (df_cleared.self_defined_ethnicity == 'Other ethnic group - Any other ethnic group') | \
                         (df_cleared.self_defined_ethnicity == 'Other ethnic group - Arab')), lit(1)) \
                         .otherwise(lit(0)))               

df_clean = df_clean.withColumn("self_defined_ethnicity_mixed", \
                    when(((df_cleared.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - Any other Mixed/Multiple ethnic background') | \
                         (df_cleared.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - White and Black Caribbean') | \
                          (df_cleared.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - White and Black African') | \
                         (df_cleared.self_defined_ethnicity == 'Mixed/Multiple ethnic groups - White and Asian')), lit(1)) \
                         .otherwise(lit(0)))                     

# COMMAND ----------

from pyspark.sql.types import IntegerType,BooleanType,DateType

df_clean = df_clean.withColumn("involved_person",df_clean.involved_person.cast(IntegerType()))
df_clean = df_clean.drop('self_defined_ethnicity')

df_clean.write \
  .format('delta') \
  .mode('overwrite') \
  .save('s3a://delta-lake-mlops/dataForcesSilver')

# COMMAND ----------

import pandas as pd
#Gold Standard

#this is the pandas way of life
pandas_df_clean = df_clean.toPandas()
pandas_df_dummies = pd.get_dummies(pandas_df_clean, columns=['age_range','gender', 'legislation', 'officer_defined_ethnicity', 'type', 'object_of_search', 'force'])

#this is the spark way of life
from pyspark.ml.feature import OneHotEncoder, StringIndexer

df_clean.printSchema()
# used for encoding strings
indexer = StringIndexer(inputCols=['age_range','gender'], outputCols=['age_range_index','gender_index']).fit(df_clean)

#used for encoding integers 
encoder = OneHotEncoder(inputCols=['involved_person', 'self_defined_ethnicity_black'],
                                 outputCols=['involved_person_vec', 'self_defined_ethnicity_black_vec'])
model = encoder.fit(df_clean)
encoded = model.transform(df_clean)
encoded.show(20, False)

# COMMAND ----------

"""
import numpy as np
spark.conf.set("spark.sql.execution.arrow.enabled", "true")
#Save Data to Delta Lake for TFX Pipline
# Define the output format, output mode, columns to partition by, and the output path.
write_format = 'delta'
write_mode = 'overwrite'
save_path = 's3a://delta-lake-mlops/dataForcesGold'
 
#Silver Standard    
#Convert from Pandas to Spark DF
dfT.columns = dfT.columns.str.replace(' ','_')
dfT.columns = dfT.columns.str.replace('(','')
dfT.columns = dfT.columns.str.replace(')','')
dfT.columns = dfT.columns.str.replace('-','_')


#sdf.show()


# Write the data to its target.
sdf.write \
  .format(write_format) \
  .mode(write_mode) \
  .save(save_path)

"""

# COMMAND ----------

#spark.read.format("delta").load("/dbfs/FileStore/delta/dataForces") 
dbutils.fs.ls("s3a://delta-lake-mlops/")
