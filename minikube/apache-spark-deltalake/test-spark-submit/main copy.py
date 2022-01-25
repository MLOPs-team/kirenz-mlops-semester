import json, requests
import os, datetime
import pyspark
#import pandas as pd

#from databricks import koalas as ks
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import explode, split, col, sum, lit, udf
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from delta import *
from delta.tables import *
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, ArrayType
from sklearn.preprocessing import LabelEncoder
import pyspark.pandas as ps
import json



#blablab
sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages io.delta:delta-core_2.12:1.0.0 pyspark-shell org.postgresql:postgresql:42.1.1 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" '

if __name__ == "__main__":
     # build spark session and enable sql extension & load sample data
    builder = pyspark.sql.SparkSession.builder.appName("NiklasTest") \
    .config("spark.driver.extraClassPath", sparkClassPath) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    
    spark = spark = configure_spark_with_delta_pip(builder).getOrCreate()
    sc = spark.sparkContext
    
    data = spark.range(0, 5)
    data.write.format("delta").save("/tmp/delta-table")