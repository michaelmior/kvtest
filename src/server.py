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
from joinHelpers import socket_send_data_by_json
from joinHelpers import socket_recv_data_by_json
from storage import *



NUM_HOST = int(config['NUM_HOST'])
HOST = ''    # Symbolic name meaning the local host
# TODO: Read this port number form a configuration file
PORT = int(config['SERVER_PORT']) # Arbitrary non-privileged port

def getServerId():
    # hostname = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]
    # print(commands.getoutput("/sbin/ifconfig").split("\n")[1])
    ip = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
    rtn = int(ip.split('.')[3]) - 1
    return rtn

def fetch_users(sId, tuples, result_container, result_sema, barrier,
                waitNum, partial_result):
    server_address = '10.0.0.' + str(sId + 1)
    # this socket is talking to another server to fetch relevant user data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_address, PORT))
    allData = {config['OP'] : config['USERS_OP'],
               config['IDs'] : tuples}
    socket_send_data_by_json(sock, allData)
    partial_seller_result = socket_recv_data_by_json(sock)
    for key in partial_result:
        # err(partial_seller_result)
        # There is no replication at the moment so we can safely grab first item in [0]
        seller_id = 'users:' + partial_result[key]['seller'][0]
        seller_info = partial_seller_result[seller_id]
        partial_result[key]['seller_info'] = seller_info
    with result_sema:
        result_container.update(partial_result)
    sock.close()
    barrier.sync(waitNum)

def serve_user_op(client_socket, storage, client_ids):
    rtn = dict()
    for client_id in client_ids:
        rtn[client_id] = storage.get(client_id)
    socket_send_data_by_json(client_socket, rtn)

def handleJoinItemUserOp(clientsocket, addr, storage, serverId, item_ids):
    # result contains the final result to the users
    # each result entry is a key value pair in the dictionary
    # key is the item id
    # and value is item value in dictionary form aggregated with
    # and extra key 'userInfo' with value of that user information
    result = dict()
    other_traffics = {}
    seller_to_item_map = {}
    partial_results = {}
    for id in item_ids:
        item_id = 'items:' + str(id)
        # There is no replication at the moment
        itemServerId = storage.getServerIds(item_id)[0]
        if(itemServerId == serverId):
            itemRow = storage.get(item_id)
            client_ids = itemRow['seller']
            for c_id in client_ids:
                client_id = 'users:' + str(c_id)
                # Using [0] because we do not have replication at the moment
                client_server_id = storage.getServerIds(client_id)[0]
                if(str(serverId) == str(client_server_id)):
                    itemRow['seller_info'] = storage.get(client_id)
                    result[item_id] = itemRow
                else:
                    # Need to query of user to other hosts
                    if client_server_id not in other_traffics:
                        other_traffics[client_server_id] = []
                        partial_results[client_server_id] = dict()
                    other_traffics[client_server_id].append(client_id)
                    partial_results[client_server_id][item_id] = itemRow
    waitNum = len(other_traffics) + 1
    if(waitNum == 1):
    # if True:
        return result
    # send queries to other servers
    result_sema = threading.Semaphore()
    barrier = BarrierSync()
    for key in other_traffics.keys():
        fetch_users_input = (key, other_traffics[key], result, result_sema,
                             barrier, waitNum, partial_results[key])
        thread.start_new_thread(fetch_users, fetch_users_input)
        # err(('keys', key))
    barrier.sync(waitNum)
    return result


def serve(client_socket, addr, storage, serverId):
    """ Each serve call is a new thread that serves requests """
    lenBuf = client_socket.recv(4)
    dataLen = struct.unpack('>L', lenBuf)[0]
    rawData = socket_read_n(client_socket, dataLen)
    # print >> sys.stderr, 'clientsocket %s is done and total data received = %s' % (str(addr), str(len(rawData)))
    dataDict = json.loads(rawData)
    ids = dataDict[config['IDs']]
    op = dataDict[config['OP']]
    if(op == config['JOIN_ITEM_USER_OP']):
        result = handleJoinItemUserOp(client_socket,addr, storage, serverId, ids)
        # Send data
        socket_send_data_by_json(client_socket, result)
    elif(op == config['USERS_OP']):
        serve_user_op(client_socket, storage, ids)
    else:
        err(('SHOULD NOT REACH HERE, NO OP to handle:', op))
    client_socket.close()


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
    err("Server " + str(sId) + " is initializing...")
    startServer(sId, rFactor = 1)
