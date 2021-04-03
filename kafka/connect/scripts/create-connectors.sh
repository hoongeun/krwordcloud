#!/bin/bash

sleep 10

echo "Waiting for Kafka Connect to start listening on kafka-connect  "
while :; do
    # Check if the connector endpoint is ready
    # If not check again
    curl_status=$(curl -s -o /dev/null -w %{http_code} http://localhost:8083/connectors)
    echo -e $(date) "Kafka Connect listener HTTP state: " $curl_status " (waiting for 200)"
    if [ $curl_status -eq 200 ]; then
        break
    fi
    sleep 5
done

curl -X GET localhost:8083/connector-plugins

echo "======> Creating connectors"
# Send a simple POST request to create the connector

# Create the HdfsSinkConnector
curl -X POST \
    -H "Content-Type: application/json" \
    --data '{
        "name": "add-article",
        "config": {
            "connector.class": "io.confluent.connect.hdfs.HdfsSinkConnector",
            "topics.regex": "^add-article-((?:[1-9]\\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29))$",
            "tasks.max": 3,
            "store.url": "hdfs://'$HDFS_HOST':9000",
            "flush.size": 10,
            "topic.capture.groups.regex": "^add-article-((?:[1-9]\\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29))$",
            "topics.dir": "/add-article/${0}",
            "format.class": "io.confluent.connect.hdfs.orc.OrcFormat"
        }
    }' http://localhost:8083/connectors

# # Create the CouchbaseSinkConnector
curl -X POST \
    -H "Content-Type: application/json" \
    --data '{
    "name": "add-trend",
    "config": {
            "connector.class": "com.couchbase.connect.kafka.CouchbaseSinkConnector",
            "topics": "add-trend",
            "tasks.max": 3,
            "couchbase.seed.nodes": "'$COUCHBASE_HOST'",
            "couchbase.bucket": "Trend",
            "couchbase.username": "'$COUCHBASE_USER'",
            "couchbase.password": "'$COUCHBASE_PASSWORD'",
            "couchbase.persist.to": "ACTIVE",
            "couchbase.document.id": "${/date}-${/press}-${category}",
            "key.converter": "org.apache.kafka.connect.storage.StringConverter",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter"
        }
    }' http://localhost:8083/connectors

# # Create the CouchbaseSinkConnector
curl -X POST \
    -H "Content-Type: application/json" \
    --data '{
    "name": "add-trend",
    "config": {
            "connector.class": "com.couchbase.connect.kafka.CouchbaseSinkConnector",
            "topics": "add-trend",
            "tasks.max": 3,
            "couchbase.seed.nodes": "'$COUCHBASE_HOST'",
            "couchbase.bucket": "Stats",
            "couchbase.username": "'$COUCHBASE_USER'",
            "couchbase.password": "'$COUCHBASE_PASSWORD'",
            "couchbase.persist.to": "ACTIVE",
            "couchbase.document.id": "${/date}-${/press}-${category}",
            "key.converter": "org.apache.kafka.connect.storage.StringConverter",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter"
        }
    }' http://localhost:8083/connectors
