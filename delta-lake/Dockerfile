FROM ubuntu:latest

RUN apt update
RUN apt install -y nano
RUN apt install -y python3-pip
RUN pip install pyspark==3.1.2
RUN export PYSPARK_PYTHON=python3

# For tzdata, otherwise the openjdk installation will wait til you type in the region
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y tzdata

RUN apt install -y openjdk-11-jdk

# You only need the following if you have multiple java instances installed
# ENV JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64

RUN pyspark --packages io.delta:delta-core_2.12:1.0.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"
