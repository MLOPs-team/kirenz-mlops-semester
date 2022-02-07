"THIS IS A DAG TO DOWNLOAD THE DATA FROM THE DELTA LAKE"
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import pyspark
from pyspark.sql import SparkSession
from delta import *
import pandas as pd

default_args = {
    'owner': 'airflow',    
    'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(2018, 12, 30),
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    }

def my_func():
    builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    df = spark.read.format("delta").load("/mnt/s3/dataForcesGold")
    pandas_df = df.toPandas()
    pandas_df = pandas_df.sample(n=10000)
    pandas_df.to_csv("/usr/local/airflow/data/data.csv")

    df = df.sample(0.01)
    #df.show()
    
    #df.coalesce(1).write.mode("overwrite").format("parquet").mode("overwrite").option("compression", "none").save("data")
    #df.write.csv("/usr/local/airflow/data/data.csv", mode='overwrite')
    #df.coalesce(1).write.csv("data", mode='overwrite')


with DAG('Download-Data-from-Delta-Lake', default_args=default_args) as dag:
    python_task	= PythonOperator(
        task_id='python_task',
        python_callable=my_func
        )
