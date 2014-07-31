#!/bin/bash

PROJECT_DIR='/media/sf_vm_shared/latest//new_project/kvtest/src/'

rm -rf  ~/.ssh/known_hosts
for i in h{1..4}
do
    ssh ${i} "cd ${PROJECT_DIR}; python ./server.py" &
    echo server started at ${i}
done
