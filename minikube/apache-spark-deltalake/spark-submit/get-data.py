from pyspark.sql import SparkSession
import requests
import json
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType, BooleanType
from pyspark.sql import Row
from pyspark.sql.functions import randn, rand


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

df_1 =  spark.createDataFrame([
        (1, 1.0), 
        (1, 2.0), 
        (2, 3.0), 
        (2, 5.0), 
        (2, 10.0)
    ])

df_2 = spark.createDataFrame([
        (2, 1.0, 3), 
        (2, 2.0, 3), 
        (3, 3.0, 3), 
        (4, 5.0, 3), 
        (5, 10.0, 3)
    ])

df_3 = spark.createDataFrame([
        (3, 1.0, 3, 4), 
        (4, 2.0, 3, 4), 
        (5, 3.0, 3, 4), 
        (5, 5.0, 3, 4), 
        (6, 10.0, 3, 4)
    ])    

res1and2=df_1.unionByName(df_2, allowMissingColumns=True)
res1and2.show()
resand3=res1and2.unionByName(df_3, allowMissingColumns=True).show()

#Requests
RestApiRequest = Row("verb", "url", "headers", "body")
for month in jsonForces:
    if str(month['date']) > '2020-12':
            print(month['date'])
            for force in month['stop-and-search']:
                request_df = spark.createDataFrame([RestApiRequest("get", 'https://data.police.uk/api/stops-force?force=' + str(force) + '&date=' + str(month['date']), headers, body)
                ])\
                .withColumn("execute", udf_executeRestApi(col("verb"), col("url"), col("headers"), col("body")))
                print(request_df)

            request_df.select("execute").show()
spark.stop()
