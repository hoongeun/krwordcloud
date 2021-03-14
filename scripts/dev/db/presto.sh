#!/bin/bash
# Reference: https://github.com/big-data-europe/docker-hive

# run hive
docker-compose up -d

# run prestodb
docker-compose up -d presto-coordinator
