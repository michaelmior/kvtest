#!/bin/bash

PROJECT_DIR='/mininet/src/'

rm -rf  ~/.ssh/known_hosts
for i in 10.0.0.{1..4}
do
    ssh ${i} "cd ${PROJECT_DIR}; python ./server.py" &
    echo server started at ${i}
done
