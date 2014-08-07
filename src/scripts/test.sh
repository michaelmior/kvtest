#!/bin/bash

if [ ${#} -ne 1 ]
then
    echo "Usage: ${0} link_bandwidth_in_bsp"
fi

total_bandwidth=${1}

PROJECT_DIR='/mininet/src/'

mkdir -p ${PROJECT_DIR}/out
rm -rf  ~/.ssh/known_hosts

bash /mininet/src/scripts/queues_new.sh ${total_bandwidth}

for i in 10.0.0.{1..4}
do
    ssh ${i} "cd ${PROJECT_DIR}; python ./server.py >> out/server${i} 2>&1" &
    echo server started at ${i}
done
