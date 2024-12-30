FROM openjdk:11-jdk-slim

RUN apt-get update && apt-get install -y \
    wget \
    ssh \
    rsync

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xzvf hadoop-${HADOOP_VERSION}.tar.gz \
    && mv hadoop-${HADOOP_VERSION} ${HADOOP_HOME} \
    && rm hadoop-${HADOOP_VERSION}.tar.gz \
    && mkdir -p ${HADOOP_HOME}/logs

COPY core-site.xml ${HADOOP_HOME}/etc/hadoop/