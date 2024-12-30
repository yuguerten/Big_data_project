FROM openjdk:11-jdk-slim

RUN apt-get update && apt-get install -y \
    wget \
    ssh \
    rsync

ENV SPARK_VERSION=3.5.3
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && tar -xzvf spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop3 ${SPARK_HOME} \
    && rm spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && mkdir -p ${SPARK_HOME}/logs