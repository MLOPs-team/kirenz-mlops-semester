FROM bde2020/spark-submit:3.1.1-hadoop3.2

LABEL maintainer="Niklas Denneler <niklas.denneler@gmail.com>"
ARG AWS_ACCESS_KEY
ARG AWS_SECRET_KEY

RUN echo "Oh dang look at that $AWS_ACCESS_KEY"
RUN echo "Oh dang look at that $AWS_SECRET_KEY"

#Some Python Fuckery
RUN echo "**** install Python ****" && \
    apk add --no-cache python && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi


# Install dependencies
# the lapack package is only in the community repository
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --update add --no-cache lapack-dev gcc freetype-dev
RUN apk add py-pip python-dev python3-dev
RUN apk add --no-cache --virtual .build-deps gfortran musl-dev g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip3 install --upgrade cython

# Copy the requirements.txt first, for separate dependency resolving and downloading
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the source code
COPY main.py .

# Envoirnment Variables for Spark
ENV SPARK_MASTER_NAME "spark"
ENV SPARK_APPLICATION_PYTHON_LOCATION /main.py
ENV SPARK_APPLICATION_ARGS "/spark/README.md"
ENV SPARK_SUBMIT_ARGS "--packages io.delta:delta-core_2.12:1.0.0,org.postgresql:postgresql:42.1.1,org.apache.hadoop:hadoop-aws:3.2.0 --conf spark.hadoop.fs.s3a.access.key=${AWS_ACCESS_KEY}  --conf spark.hadoop.fs.s3a.secret.key=${AWS_SECRET_KEY}"
#pyspark-shell org.postgresql:postgresql:42.1.1
ENV PYSPARK_PYTHON python3
#CMD ["/bin/bash", "/template.sh"]

# removing dependencies
#RUN apk del .build-deps
