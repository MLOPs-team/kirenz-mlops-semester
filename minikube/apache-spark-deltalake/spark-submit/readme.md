#To Launch Spark Job locally:
spark-submit --master spark://localhost:7077 --packages io.delta:delta-core_2.12:1.1.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" main.py

This requires a running spark cluster!