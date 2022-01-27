FROM frolvlad/alpine-glibc:alpine-3.14

ARG CONDA_VERSION="4.7.12.1"
ARG CONDA_MD5="81c773ff87af5cfac79ab862942ab6b3"
ARG CONDA_DIR="/opt/conda"

ENV PATH="$CONDA_DIR/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1

ENV ENABLE_INIT_DAEMON false
ENV INIT_DAEMON_BASE_URI http://identifier/init-daemon
ENV INIT_DAEMON_STEP spark_master_init

ENV BASE_URL=https://archive.apache.org/dist/spark/
ENV SPARK_VERSION=3.2.0
ENV HADOOP_VERSION=3.2
ENV PYTHONHASHSEED 1

RUN apk update && apk add bash

# Install conda
RUN echo "**** install dev packages ****" && \
    apk add --virtual .build-dependencies ca-certificates wget bash && \
    \
    echo "**** get Miniconda ****" && \
    mkdir -p "$CONDA_DIR" && \
    wget "http://repo.continuum.io/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh" -O miniconda.sh && \
    echo "$CONDA_MD5  miniconda.sh" | md5sum -c && \
    \
    echo "**** install Miniconda ****" && \
    bash miniconda.sh -f -b -p "$CONDA_DIR" && \
    echo "export PATH=$CONDA_DIR/bin:\$PATH" > /etc/profile.d/conda.sh && \
    \
    echo "**** setup Miniconda ****" && \
    conda update --all --yes && \
    conda config --set auto_update_conda False && \
    \
    echo "**** cleanup ****" && \
    apk del --purge .build-dependencies && \
    rm -f miniconda.sh && \
    conda clean --all --force-pkgs-dirs --yes && \
    find "$CONDA_DIR" -follow -type f \( -iname '*.a' -o -iname '*.pyc' -o -iname '*.js.map' \) -delete && \
    \
    echo "**** finalize ****" && \
    mkdir -p "$CONDA_DIR/locks" && \
    chmod 777 "$CONDA_DIR/locks"

LABEL maintainer="Niklas Denneler <niklas.denneler@gmail.com>"
ARG AWS_ACCESS_KEY
ARG AWS_SECRET_KEY

RUN echo "Oh dang look at that $AWS_ACCESS_KEY"
RUN echo "Oh dang look at that $AWS_SECRET_KEY"

#Installing required dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN apk add openjdk8-jre nss coreutils procps \ 
      && wget ${BASE_URL}/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      && tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark \
      && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      && cd /
   
# Copy the source code
COPY main.py .

COPY submit.sh /
RUN ["chmod", "+x", "/submit.sh"]

# Envoirnment Variables for Spark
ENV SPARK_MASTER_NAME "spark"
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_PYTHON_LOCATION /main.py
ENV SPARK_APPLICATION_ARGS "/spark/README.md"
ENV SPARK_SUBMIT_ARGS "--packages io.delta:delta-core_2.12:1.1.0,org.apache.hadoop:hadoop-aws:3.2.2,com.amazonaws:aws-java-sdk-bundle:1.11.375"
ENV PYSPARK_PYTHON python3

CMD ["/bin/sh", "/submit.sh"]

