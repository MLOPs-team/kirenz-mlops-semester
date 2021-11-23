import os, datetime
from databricks import koalas as ks
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import explode, split, col, sum, lit
from pyspark.sql import SparkSession

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

if __name__ == "__main__":

    # build spark session and enable sql extension & load sample data
    spark = SparkSession.builder.appName("MyApp")\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog").getOrCreate()

    data = spark.range(0, 5)
    data.write.format("delta").save("/tmp/delta-table")

    df = spark.read.format("delta").load("/tmp/delta-table")
    df.show()

    data = spark.range(5, 10)
    data.write.format("delta").mode("overwrite").save("/tmp/delta-table")
    df.show()
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