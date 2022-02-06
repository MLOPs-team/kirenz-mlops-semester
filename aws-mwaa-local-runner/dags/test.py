"THIS IS A DAG TO DOWNLOAD THE DATA FROM THE DELTA LAKE"
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import pyspark
from pyspark.sql import SparkSession
from delta import *

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
    df.write.parquet('/usr/local/airflow/data/data.gzip')   

dag = DAG("Download-Data-from-Delta-Lake", default_args=default_args, schedule_interval=timedelta(1))
python_task	= PythonOperator(task_id='python_task', python_callable=my_func)


python_task