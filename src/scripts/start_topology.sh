#!/bin/bash

mkdir -p ~/pox/ext
cp -f /mininet/src/controller_v1.py ~/pox/ext/.

sudo python /mininet/src/CustomTopo.py
