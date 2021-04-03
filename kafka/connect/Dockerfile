ARG BASE_PREFIX=confluentinc
ARG CONNECT_IMAGE=cp-kafka-connect-base

FROM $BASE_PREFIX/$CONNECT_IMAGE:6.0.1

RUN confluent-hub install --no-prompt couchbase/kafka-connect-couchbase:4.0.5
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-hdfs:10.0.2

RUN mkdir -p /etc/kafka/scripts
COPY ./scripts /etc/kafka/scripts
