import threading
import threading
import time
import sys

config = {
    'NUM_HOST': 4,  # Update when when change topology
    'OP': 'op',
    'ITEMS_OP': 'item',
    'USERS_OP' : 'user',
    # item is the primary key and user is the foreign key
    'JOIN_ITEM_USER_OP' : 'join_item_user',
    'IDs': 'ids',
}

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
