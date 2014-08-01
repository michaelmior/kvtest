# Echo server program
import socket
import thread
import sys
import commands
import json
import threading
import os
import inspect
import traceback
import ast
import struct

# adds the current dir i.e. src to system path
sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
from joinHelpers import BarrierSync
from joinHelpers import config
from joinHelpers import err
from joinHelpers import socket_read_n
from storage import *

NUM_HOST = int(config['NUM_HOST'])
HOST = ''    # Symbolic name meaning the local host
# TODO: Read this port number form a configuration file
PORT = 50007 # Arbitrary non-privileged port

def getServerId():
    # hostname = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]
    # print(commands.getoutput("/sbin/ifconfig").split("\n")[1])
    ip = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
    rtn = int(ip.split('.')[3]) - 1
    return rtn

def fetchUsers(sId, tuples, barrier):
    pass

def handleJoinItemUserOp(clientsocket, addr, storage, serverId, itemIds):
    result = dict()
    otherTraffic = {}
    for id in itemIds:
        itemId = 'items:' + str(id)
        # There is no replication at the moment
        itemServerId = storage.getServerIds(itemId)[0]
        if(itemServerId == serverId):
            itemRow = storage.get(itemId)
            clientIds = itemRow['seller']
            for cId in clientIds:
                clientId = 'users:' + str(cId)
                # Using [0] because we do not have replication at the moment
                clientServerId = storage.getServerIds(clientId)[0]
                if(str(serverId) == str(clientServerId)):
                    itemRow['userInfo'] = storage.get(clientId)
                    result[id] = itemRow
                else:
                    # Need to query of user to other hosts
                    if clientServerId not in otherTraffic:
                        otherTraffic[clientServerId] = []
                    otherTraffic[clientServerId].append(clientId)
                    pass
    waitNum = len(otherTraffic) + 1
    if(waitNum == 1):
        return result
    # send queries to other servers
    barrier = BarrierSync()
    for key in otherTraffic.keys():
        fetchUsers(key, otherTraffic[key], barrier)
        # err(('keys', key))
    # barrier.sync(waitNum)
    return result

def serve(clientsocket, addr, storage, serverId):
    lenBuf = clientsocket.recv(4)
    dataLen = struct.unpack('>L', lenBuf)[0]
    rawData = socket_read_n(clientsocket, dataLen)
    # print >> sys.stderr, 'clientsocket %s is done and total data received = %s' % (str(addr), str(len(rawData)))
    dataDict = json.loads(rawData)
    ids = dataDict[config['IDs']]
    op = dataDict[config['OP']]
    if(op == config['JOIN_ITEM_USER_OP']):
        result = handleJoinItemUserOp(clientsocket,addr, storage, serverId, ids)
    elif(op == config['USER_OP']):
        err('TO BE Handled')
    else:
        err(('SHOULD NOT REACH HERE, NO OP to handle:', op))

    # Send data
    if(len(result) == 0):
        dataLen = 0
        lenBuf = struct.pack('>L', dataLen)
        clientsocket.sendall(lenBuf)
    else:
        toSend = json.dumps(result)
        lenBuf = struct.pack('>L', len(toSend))
        clientsocket.sendall(lenBuf)
        rtn = clientsocket.sendall(toSend)
    clientsocket.close()


def startServer(sId = None, rFactor = 1):
    store = Store(NUM_HOST, sId, rFactor)
    users = User(store).read()
    items = Item(store).read()
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(5)
    while 1:
        conn, addr = serverSocket.accept()
        # print >> sys.stderr, 'Connected by', addr
        thread.start_new_thread(serve, (conn, addr, store, sId))

if __name__ == '__main__':
    sId = getServerId()
    print("Server " + str(sId) + " is initializing...")
    startServer(sId, rFactor = 1)
