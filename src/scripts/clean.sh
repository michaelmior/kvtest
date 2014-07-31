#!/bin/bash

PROJECT_DIR='~/xcui/new_project/kvtest/src/'

for i in h{1..4}
do
    ssh ${i} "kill -9 $(ps aux | grep server.p\[y\] | awk '{print $2}')"
    echo server stopped at ${i}
done


for i in h{1..4}
do
    ssh ${i} "kill -9 $(ps aux | grep server.p\[y\] | awk '{print $2}')"
    echo server stopped at ${i}
done
