# Echo server program
import socket
import thread
import sys
import commands

from storage import *


NUM_HOST = 4
HOST = ''    # Symbolic name meaning the local host
# TODO: Read this port number form a configuration file
PORT = 50007 # Arbitrary non-privileged port

def getServerId():
    # hostname = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]
    ip = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:]
    rtn = int(ip.split('.')[3]) - 1
    return rtn

def serve(clientsocket, addr):
    recv_size = 0
    while 1:
        data = clientsocket.recv(1024)
        recv_size += len(data)
        if not data: break
    print >> sys.stderr, 'clientsocket %s is done and total data received = %s' % (str(addr), str(recv_size))
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
        print >> sys.stderr, 'Connected by', addr
        thread.start_new_thread(serve, (conn, addr))

if __name__ == '__main__':
    sId = getServerId()
    print(sId)
    startServer(sId, rFactor = 1)
