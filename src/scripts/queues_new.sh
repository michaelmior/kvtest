#!/bin/bash


if [ ${#} -ne 1 ]
then
    echo "Usage: ${0} bandwidth_in_bps"
fi

# total_bandwidth=1000000
total_bandwidth=${1}

# Add queues with varying minimum bandwidth reservations to each switch port
# queue 0 traffic will have priority over all other traffic
for switch in $(sudo ovs-vsctl list-br); do
    for port in $(sudo ovs-vsctl list-ports $switch); do
        sudo ovs-vsctl -- set Port $port qos=@newqos -- \
          --id=@newqos create QoS type=linux-htb other-config:max-rate=${total_bandwidth} \
          queues=0=@q0,1=@q1,2=@q2,3=@q3,4=@q4,5=@q5,6=@q6,7=@q7,8=@q8,9=@q9,10=@q10 -- \
          --id=@q0 create Queue other-config:priority=0 -- \
          --id=@q1 create Queue other-config:min-rate=$((total_bandwidth/10*1)) other-config:priority=1 -- \
          --id=@q2 create Queue other-config:min-rate=$((total_bandwidth/10*2)) other-config:priority=1 -- \
          --id=@q3 create Queue other-config:min-rate=$((total_bandwidth/10*3)) other-config:priority=1 -- \
          --id=@q4 create Queue other-config:min-rate=$((total_bandwidth/10*4)) other-config:priority=1 -- \
          --id=@q5 create Queue other-config:min-rate=$((total_bandwidth/10*5)) other-config:priority=1 -- \
          --id=@q6 create Queue other-config:min-rate=$((total_bandwidth/10*6)) other-config:priority=1 -- \
          --id=@q7 create Queue other-config:min-rate=$((total_bandwidth/10*7)) other-config:priority=1 -- \
          --id=@q8 create Queue other-config:min-rate=$((total_bandwidth/10*8)) other-config:priority=1 -- \
          --id=@q9 create Queue other-config:min-rate=$((total_bandwidth/10*9)) other-config:priority=1 -- \
          --id=@q10 create Queue other-config:min-rate=$((total_bandwidth/10*10)) other-config:priority=1
    done
done
