import threading
import threading

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
