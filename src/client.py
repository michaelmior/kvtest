# Echo client program
import socket
import json
from test import *
import time
import sys

NUM_HOST = 4
ID_LIST = []

def current_time_in_milli():
    return int(round(time.time() * 1000))

def loadIDs():
    533721
    pass

# all_data = json.dumps(store.data[1])
# sys.stdout.write(str(len(all_data)) + '\n')

HOST = '10.0.0.4'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

all_data = 'abcd'
start_time = current_time_in_milli()
rtn = s.send(all_data)
print rtn
end_time = current_time_in_milli()
print 'Total time spent to send the data %d' % (end_time - start_time)
s.close()
# print 'Received', len(data)
