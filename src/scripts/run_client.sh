#!/bin/bash

if [ $# -ne 3 ]
then
    echo "Usage: ${0} client_ip bandwidth experiment_name"
    echo "Example Usage:"
    echo "    ${0} 10.0.0.5 1mbps norm"
    exit 66
fi

PROJECT_DIR='/mininet/src/'
result_dir="${PROJECT_DIR}/result/${2}/${3}/"
mkdir -p ${result_dir}
rm -rf  ~/.ssh/known_hosts

for i in {0..5};
do
    ssh ${1} "cd ${PROJECT_DIR}; ./client.py  > ${result_dir}/client_${i}.out 2>&1"
    sleep 5
done


# Make some sound so we know this is finished!
echo -ne '\007'
echo -ne '\007'
echo -ne '\007'
echo -ne '\007'
echo -ne '\007'
