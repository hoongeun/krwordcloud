
## A script similar to this can be used to create connectors making sure the endpoints are ready

echo "Waiting for Kafka Connect to start listening on kafka-connect  "
while :; do
    # Check if the connector endpoint is ready
    # If not check again
    curl_status=$(curl -s -o /dev/null -w %{http_code} http://localhost:{{ .Values.servicePort }}/connectors)
    echo -e $(date) "Kafka Connect listener HTTP state: " $curl_status " (waiting for 200)"
    if [ $curl_status -eq 200 ]; then
        break
    fi
    sleep 5
done

echo "======> Creating connectors"
# Send a simple POST request to create the hive connector
curl -X POST \
    -H "Content-Type: application/json" \
    --data '{
    "name": "hbase-sink-connector",
    "config": {
        "connector.class": "io.confluent.connect.hdfs3.Hdfs3SinkConnector",
        "tasks.max": "5",
        "topics": "add-articles",
        "hdfs.url": "hdfs://localhost:9000",
        "flush.size": "3",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "io.confluent.connect.avro.AvroConverter",
        "value.converter.schema.registry.url":"http://localhost:8081",
        "confluent.topic.bootstrap.servers": "localhost:9092",
        "confluent.topic.replication.factor": "1"
        }
    }' http://$CONNECT_REST_ADVERTISED_HOST_NAME:8083/connectors

curl -X POST \
    -H "Content-Type: application/json" \
    --data '{
    "name": "couchbase-sink-connector",
    "config": {
        "connector.class": "com.couchbase.connect.kafka.CouchbaseSinkConnector",
        "tasks.max": 5,
        "topics: "add-spark-evaluation",
        "flush.size": "3",
        "couchbase.user": "couchuser",
        "couchbase.bucket: "trend",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter.schemas.enable"=false,
        "confluent.topic.bootstrap.servers": "kafka:9092",
        "confluent.topic.replication.factor": "1"
        }
    }' http://$CONNECT_REST_ADVERTISED_HOST_NAME:8083/connectors