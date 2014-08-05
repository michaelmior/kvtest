#!/bin/bash

# Add queues with varying minimum bandwidth reservations to each switch port
# queue 0 traffic will have priority over all other traffic

for switch in $(sudo ovs-vsctl list-br); do
    for port in $(sudo ovs-vsctl list-ports $switch); do
        sudo ovs-vsctl -- set Port $port qos=@newqos -- \
          --id=@newqos create QoS type=linux-htb other-config:max-rate=10000000 \
          queues=0=@q0,1=@q1,2=@q2,3=@q3,4=@q4,5=@q5,6=@q6,7=@q7,8=@q8,9=@q9,10=@q10 -- \
          --id=@q0 create Queue other-config:priority=0 -- \
          --id=@q1 create Queue other-config:min-rate=1000000 other-config:priority=1 -- \
          --id=@q2 create Queue other-config:min-rate=2000000 other-config:priority=1 -- \
          --id=@q3 create Queue other-config:min-rate=3000000 other-config:priority=1 -- \
          --id=@q4 create Queue other-config:min-rate=4000000 other-config:priority=1 -- \
          --id=@q5 create Queue other-config:min-rate=5000000 other-config:priority=1 -- \
          --id=@q6 create Queue other-config:min-rate=6000000 other-config:priority=1 -- \
          --id=@q7 create Queue other-config:min-rate=7000000 other-config:priority=1 -- \
          --id=@q8 create Queue other-config:min-rate=8000000 other-config:priority=1 -- \
          --id=@q9 create Queue other-config:min-rate=9000000 other-config:priority=1 -- \
          --id=@q10 create Queue other-config:min-rate=10000000 other-config:priority=1
    done
done
