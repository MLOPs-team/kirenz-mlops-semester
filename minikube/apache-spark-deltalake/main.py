import json, requests
import os, datetime
import pyspark

#from databricks import koalas as ks
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import explode, split, col, sum, lit
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import *
from delta.tables import *

#blablab
sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.1.1 pyspark-shell io.delta:delta-core_2.12:1.1.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"'

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

#Helper Function to turn JSON into Line delimited JSON, as neede by PySpark: https://spark.apache.org/docs/latest/sql-data-sources-json.html
def dump_jsonl(data, output_path, append=False):
    """
    Write list of objects to a JSON lines file.
    """
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')
    print('Wrote {} records to {}'.format(len(data), output_path))

if __name__ == "__main__":
     # build spark session and enable sql extension & load sample data
    builder = SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")  \
    .config("spark.driver.extraClassPath", sparkClassPath)
    
    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    #Load Data from UK Police API
    r = requests.get('https://data.police.uk/api/leicestershire/NC04/events')
    dump_jsonl(r.json(),"data.json")
    #create df from JSON Content of UK Police API
    df = spark.read.json("data.json")
    df.printSchema()

    #Save data as Delta Table
    df.write.format("delta").save("delta-table")

    df.show()
    df.describe()

    #Apply Transformations

    #Build Koalas DF

    #SQL Metadata
    properties = {"user": 'postgres',"password": 'postgres',"driver": "org.postgresql.Driver"}
    #url = f"jdbc:postgresql://{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB_NAME']}"
    print("****************")
    #print(url)
    url = f"jdbc:postgresql://localhost:5432/police-data"
    
    #Write to Postgres DB
    df.write.jdbc(url=url, table='data', mode="overwrite", properties=properties)

    #Read out History of Table
    deltaTable = DeltaTable.forPath(spark,"delta-table")

    fullHistoryDF = deltaTable.history()    # get the full history of the table
    print(fullHistoryDF)
    lastOperationDF = deltaTable.history(1) # get the last operation
    print(lastOperationDF)

    spark.stop()
    """
   

    data = spark.range(0, 5)
    data.write.format("delta").save("/tmp/delta-table")

    df = spark.read.format("delta").load("/tmp/delta-table")
    df.show()

    data = spark.range(5, 10)
    data.write.format("delta").mode("overwrite").save("/tmp/delta-table")
    df.show()
    """
    """
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