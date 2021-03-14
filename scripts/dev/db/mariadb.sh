#!/bin/sh

docker run -p 3306:3306  --name mariadb -v ~/docker/krwordcloud/maria:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d mariadb:latest