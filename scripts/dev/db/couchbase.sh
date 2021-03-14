#!/bin/sh

# run couchbase with persistent volume
docker run -d --name couchbase -p 8091-8094:8091-8094 -p 11210:11210 -v ~/docker/couchbase:/opt/couchbase/var couchbase