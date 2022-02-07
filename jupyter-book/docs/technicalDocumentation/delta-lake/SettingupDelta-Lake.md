# Setting up Delta-Lake

![Delta Lake](https://docs.delta.io/latest/_static/delta-lake-logo.png)

This is heavily inspired by the Delta-Lake [Quickstart Guide]([Quickstart &mdash; Delta Lake Documentation](https://docs.delta.io/latest/quick-start.html))

## Spark ? Delta ? Delta - Lake?

When reading up on the concept of the delta-lake, the concept seems easy to comprehend. But the separation between technology / naming conventions can be tough at times.

Delta-Lake is built on top of Apache Spark, so for running your own Delta Lake you will need a Spark Shell in your programming language of choice (Scala or Python).

This is not part of the official guide, but it is always good to start with a new virtual python environment. Use conda / virtualenv to setup a new one and start it.

Then you will need to install the Pyspark Shell can be installed via this command:

```python
pip install pyspark==<compatible-spark-version>
```

Afterwards you can run Spark with the Delta-Lake Packages with this command:

```bash
pyspark --packages io.delta:delta-core_2.12:1.1.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"`
```

Afterwards you can setup your Delta-Lake project from your python scripts by running these commands below:

```python
import pyspark
from delta import *

builder = pyspark.sql.SparkSession.builder.appName("MyApp") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()
```

You can then start creating / modifying / deleting tables in Delta.
In our situation we decided to save the Delta Tables in a central AWS S3 Bucket so we could later use the Delta Lake in our TFX Pipeline aswell.

Further configuration options regarding storage and other setup tipps can be found [here](https://docs.delta.io/latest/delta-storage.html).

## This feels like magic - kind of.

Delta Lake utilizes Parquet files to store its delta tables, while all ACID conform transactions are saved in a delta-log file. This allows one to time travel through the changes made to the table and keeps files access times really low. 
While the inital setup of the delta-lake is very straight forward it is not very easy to interact with it without having any prior knowledge in Spark.

Also to make full usage of the capabilities of the Delta-Lake you will need to have proceesses in place and might need a data governance team and guidelines.

### What still needs to be explored?

- How does the delta-lake Streaming Data?

- How can the MLOps process make real use of the extra capabilities the delta approach provides. (-> Time Travel, Schema Merging etc)

- What is the ideal solution to extracting data from the delta lake?

- How can we solve the pandas vs spark dataframe dilemma?
