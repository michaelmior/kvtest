import threading
import threading
import time
import sys
import json
import struct

config = {
    'SERVER_PORT' : 50007,
    'NUM_HOST': 4,  # Update when when change topology
    'CSV_BASE': 'csv/',  # source of RUBiS data
    'OP': 'op',
    'ITEMS_OP': 'item',
    'USERS_OP' : 'user',
    # item is the primary key and user is the foreign key
    'JOIN_ITEM_USER_OP' : 'join_item_user',
    'IDs': 'ids',
}

def socket_send_data_by_json(sock, data):
    toSend = json.dumps(data)
    # using big-endian to pack the data
    dataLen = struct.pack('>L', len(toSend))
    rtn = sock.sendall(dataLen)
    assert rtn == None
    rtn = sock.sendall(toSend)
    assert rtn == None
    return

def socket_recv_data_by_json(sock):
    """
    If data the msg_len == 0
    this function returns None
    otherwise this returns the data
    """
    len_buf = sock.recv(4)
    # using big-endian to pack the data
    msg_len = struct.unpack('>L', len_buf)[0]
    if(msg_len == 0):
        return None
    else:
        raw_data = socket_read_n(sock, msg_len)
        assert len(raw_data) == msg_len
        data = json.loads(raw_data)
        return data

def socket_read_n(sock, n):
    """
    Read exactly n bytes from the socket.
    Raise RuntimeError if the connection closed before
    n bytes were read.
    """
    buf = ''
    while n > 0:
        data = sock.recv(n)
        if data == '':
            raise RuntimeError('unexpected connection close')
        buf += data
        n -= len(data)
    return buf

def err(listOfInput):
    sys.stderr.write('DEBUG\n')
    if type(listOfInput) is list or type(listOfInput) is tuple:
        for input in listOfInput:
            sys.stderr.write(str(input) + ' ')
    else:
        sys.stderr.write(str(listOfInput))
    sys.stderr.write('\nDEBUG\n')

class BarrierSync(object):
    def __init__(self):
        self.thread_count = 0
        self.semaphore = threading.Semaphore()
        self.event = threading.Event()
    def sync(self, count):
        """ All calls to this METHOD WILL block until the last (count) call is made """
        with self.semaphore:
            self.thread_count += 1
            if self.thread_count == count:
                self.event.set()
        self.event.wait()

def current_time_in_milli():
    return int(round(time.time() * 1000))
