import json, requests
import os, datetime
import pyspark
#import pandas as pd

#from databricks import koalas as ks
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import explode, split, col, sum, lit
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import *
from delta.tables import *

#blablab
sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages io.delta:delta-core_2.12:1.0.0 pyspark-shell org.postgresql:postgresql:42.1.1 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" '
#org.postgresql:postgresql:42.1.1,pyspark-shell,


#can be ignored for the moment
def apply_transforms(df: DataFrame) -> DataFrame:
    # split _c0 column as it is a string and we want the population data from it
    split_col = split(df['_c0'], '\t')

    
    # add population column, group by country, sum population
    return df \
            .withColumn("population", split_col.getItem(2).cast('float')) \
            .groupBy("country") \
            .agg(col("country"), sum("population")).select(col("country"), col("sum(population)") \
            .alias("population"))

def remove_html_tags(df: DataFrame) -> DataFrame:
        df = df.withColumn('address', F.trim(F.col('description')))
        return df 

def request(url):
    response_API = requests.get(url)
    return json.loads(response_API.text)    

if __name__ == "__main__":
     # build spark session and enable sql extension & load sample data
    builder = pyspark.sql.SparkSession.builder.appName("NiklasTest") \
    .config("spark.driver.extraClassPath", sparkClassPath) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    spark = spark = configure_spark_with_delta_pip(builder).getOrCreate()
    sc = spark.sparkContext

    #Load Data from UK Police API - Niklas
    response = requests.get('https://data.police.uk/api/leicestershire/NC04/events')
    data = response.json()

    json_rdd = sc.parallelize([data])
   
    #data_df= pd.read_json(r.json(), lines=True)
    #print(data_df)
    
    #create df from JSON Content of UK Police API
    df = spark.read.json(json_rdd)
    df.show()
    df.printSchema()
    df.show()
    df.describe()
    
    
    #Save data as Delta Table
    #df.write.format("delta").save("delta-table")
    
    #Apply Transformations

    #Build Koalas DF
    
    #SQL Metadata
    properties = {"user": 'postgres',"password": 'postgres',"driver": "org.postgresql.Driver"}
    #url = f"jdbc:postgresql://{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB_NAME']}"
    print("****************")
    #print(url)
    url = f"jdbc:postgresql://postgres:5432/police-data"
    
    #Write to Postgres DB
    df.write.jdbc(url=url, table='data', mode="overwrite", properties=properties)
    

    #Read out History of Table
    #deltaTable = DeltaTable.forPath(spark,"delta-table")

    #fullHistoryDF = deltaTable.history()    # get the full history of the table
    #print(fullHistoryDF)
    #lastOperationDF = deltaTable.history(1) # get the last operation
    #print(lastOperationDF)
    

    spark.stop()
    
    """
    data = spark.range(0, 5)
    data.write.format("delta").save("/tmp/delta-table")

    df = spark.read.format("delta").load("/tmp/delta-table")
    df.show()

    data = spark.range(5, 10)
    data.write.format("delta").mode("overwrite").save("/tmp/delta-table")
    df.show()
    
    
    # read data from publc bucket into Spark DF
    data_path = "s3a://dataforgood-fb-data/csv/" 
    df = spark.read.csv(data_path)

    # apply spark transformations
    transformedDF = df.transform(apply_transforms)

    # build Koalas DF from Spark DF, get median, convert back to Spark DataFrame, add column with current date
    kDF = ks.DataFrame(transformedDF)
    medianDF = kDF.median().withColumn
    finalDF = medianDF.to_spark().withColumn("etl_time", lit(datetime.datetime.now()))

    # SQL metadata
    properties = {"user": os.environ['PG_USER'],"postgres": os.environ['PG_PASSWORD'],"driver": "org.postgresql.Driver"}
    url = f"jdbc:postgresql://{os.environ['PG_HOST']}:{os.environ['PG_PORT']}/{os.environ['PG_DB_NAME']}"

    # write to db
    finalDF.write.jdbc(url=url, table=os.environ['TABLE_NAME'], mode="overwrite", properties=properties)
    """