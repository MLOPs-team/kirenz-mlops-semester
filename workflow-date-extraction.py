from delta import *
#Step 1: Initalize Delta Lake
builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = spark = configure_spark_with_delta_pip(builder).getOrCreate()


data = spark.range(0, 5)
data.write.format("delta").save("/tmp/delta-table")

#Load Data from API
import requests
response = requests.get("http://api.open-notify.org/astros.json")


#Write Data to Delta Lake
#Parsing etc

#Finished

