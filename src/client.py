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
import traceback
import struct

# adds the current dir i.e. src to system path
sys.path.append(os.path.dirname(__file__))
from joinHelpers import BarrierSync
from joinHelpers import config
from joinHelpers import err
from joinHelpers import socket_read_n
from joinHelpers import current_time_in_milli
from joinHelpers import socket_send_data_by_json
from joinHelpers import socket_recv_data_by_json
from joinHelpers import LoadDifferentiator


NUM_HOST = config['NUM_HOST']
ID_LIST = []
CSV_BASE = config['CSV_BASE']

BARRIER = BarrierSync()

SEMAPHORE = threading.Semaphore()
FINAL_JOIN_RESULT = []


def loadItemIDs():
    with open(CSV_BASE + '/items.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\'',
                            doublequote=False, escapechar='\\')
        header = next(reader, None)
        ld = LoadDifferentiator()
        for row in reader:
            id = row[0]
            if(ld.include_huh(id)):
                ID_LIST.append(int(id))
    print('Total item to be read:' + str(len(ID_LIST)))
    # print ID_LIST

def itemsJoin(host, port = 50007):
    """ The actual function that performs the join operation on item & user """
    # send
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    allData = {config['OP']: config['JOIN_ITEM_USER_OP'], config['IDs']: ID_LIST}
    socket_send_data_by_json(s, allData)
    partialResult = socket_recv_data_by_json(s)
    with SEMAPHORE:
        FINAL_JOIN_RESULT.append(partialResult)
    s.close()

def joinThread(threadName, host):
    start_time = current_time_in_milli()
    # time.sleep(randint(1,10))
    # Block until NUM_HOST + 1 threads have reached this point
    # The + 1 part comes from the main thread
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
            err(("Unexpected error:", sys.exc_info()[0]))
            raise

if __name__ == '__main__':
    loadItemIDs()
    global_start_time = current_time_in_milli()
    try:
        joinItems()
    except:
        err(("Unexpected error:", sys.exc_info()[0]))
        raise
    BARRIER.sync(NUM_HOST + 1)
    time.sleep(1)
    total_len = 0
    for single_result in FINAL_JOIN_RESULT:
        total_len += len(single_result)
    err(('Operation completed, # of entries fetched:', total_len))
    global_end_time = current_time_in_milli()
    err(('Total time cost is: ', global_end_time - global_start_time,'ms'))
