#!/usr/bin/env python
import socket
import json
import time
import sys
import csv
import os
import thread
import threading
import time
from random import randint
import inspect
import traceback
import struct

# adds the current dir i.e. src to system path
sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
from joinHelpers import BarrierSync
from joinHelpers import config
from joinHelpers import err
from joinHelpers import socket_read_n
from joinHelpers import current_time_in_milli

NUM_HOST = config['NUM_HOST']
ID_LIST = []
CSV_BASE = 'csv/'

BARRIER = BarrierSync()

SEMAPHORE = threading.Semaphore()
FINAL_JOIN_RESULT = []

def loadItemIDs():
    with open(CSV_BASE + 'items.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\'',
                            doublequote=False, escapechar='\\')
        header = next(reader, None)
        for row in reader:
            id = row[0]
            ID_LIST.append(int(id))
    print ID_LIST

def itemsJoin(host, port = 50007):
    """ The actual function that performs the join operation on item & user """
    # send
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    allData = {config['OP']: config['JOIN_ITEM_USER_OP'], config['IDs']: ID_LIST}
    toSend = json.dumps(allData)
    # using big-endian to pack the data
    dataLen = struct.pack('>L', len(toSend))
    rtn = s.sendall(dataLen)
    assert rtn == None
    rtn = s.sendall(toSend)
    assert rtn == None
    lenBuf = s.recv(4)
    dataLen = struct.unpack('>L', lenBuf)[0]
    if(dataLen == 0):
        partialResult = {}
    else:
        receivedRawData = socket_read_n(s, dataLen)
        # err((receivedRawData, len(receivedRawData)))
        partialResult = json.loads(receivedRawData)
    with SEMAPHORE:
        FINAL_JOIN_RESULT.append(partialResult)
    s.close()

def joinThread(threadName, host):
    start_time = current_time_in_milli()
    # time.sleep(randint(1,10))
    # Block until NUM_HOST + 1 threads have reached this point
    # The + 1 part comes from the main thread
    # print threadName, host
    itemsJoin(host)
    end_time = current_time_in_milli()
    print 'Time spent to retrieve data from host %s: %s ms' % (host, (end_time - start_time))
    # barrierSynchronise(NUM_HOST + 1)
    BARRIER.sync(NUM_HOST + 1)

def joinItems():
    for i in range(NUM_HOST):
        host = '10.0.0.' + str(i+1)
        threadName =  'Thread' + str(i+1)
        try:
            thread.start_new_thread(joinThread, (threadName, host))
        except:
            traceback.print_tb()
            sys.stderr.write("Unexpected error:", sys.exc_info()[0])

if __name__ == '__main__':
    loadItemIDs()
    try:
        joinItems()
    except:
        err(("Unexpected error:", sys.exc_info()[0]))
        raise
    # sys.exit()
    # barrierSynchronise(NUM_HOST + 1)
    BARRIER.sync(NUM_HOST + 1)
    time.sleep(1)
    print FINAL_JOIN_RESULT
