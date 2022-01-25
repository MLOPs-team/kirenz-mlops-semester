FROM bde2020/spark-base:3.2.0-hadoop3.2

LABEL maintainer="Gezim Sejdiu <g.sejdiu@gmail.com>, Giannis Mouchakis <gmouchakis@gmail.com>"

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

RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --update add --no-cache lapack-dev gcc freetype-dev
RUN apk add py-pip python-dev python3-dev
RUN apk add --no-cache --virtual .build-deps gfortran musl-dev g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip3 install --upgrade cython


COPY worker.sh /

ENV SPARK_WORKER_WEBUI_PORT 8081
ENV SPARK_WORKER_LOG /spark/logs
ENV SPARK_MASTER "spark://spark:7077"

EXPOSE 8081

CMD ["/bin/bash", "/worker.sh"]