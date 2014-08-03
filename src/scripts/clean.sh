#!/bin/bash

# kill servers
ps aux | grep \.\/server\.py | awk '{print $2}' | xargs kill -9

# kill the clients
ps aux | grep \.\/client.py | awk '{print $2}' | xargs kill -9
