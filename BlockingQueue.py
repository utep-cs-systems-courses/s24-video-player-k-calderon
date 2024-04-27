from threading import Semaphore, Lock
from queue import Queue
import log as l
import time

class BlockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = Queue(capacity)
        
        # semaphores that track empty and full "slots"
        self.empty = Semaphore(capacity)  
        self.full = Semaphore(0)
        # mutex - mutually exclusive lock. protects the queue
        l.debug("Full semaphore initialized", self.full)  
        self.qLock = Lock()

    def put(self, item):
        l.debug("BlockingQueue > put > started")
        l.debug("Put > Checking self.full address", self.full)
        # decrements empty if greater than zero, else it blocks
        self.empty.acquire()
        l.debug("BlockingQueue > put > empty.aquire() finished")
        self.qLock.acquire()
        l.debug("BlockingQueue > put > qLock.aquire() finished")
        l.debug("put > self.empty", self.empty._value)
        try:
            self.queue.put(item)
            l.debug("BlockingQueue > put > queue.put(item) finished")
        finally:
            # always release the lock
            self.qLock.release()
        # produces 1 full item
        self.full.release()
        l.debug("BlockingQueue > put > full.release() finished")
        l.debug("self.full._value:", self.full._value)

    def get(self):
        l.debug("Get sleeping for 5 seconds")
        time.sleep(5)
        l.debug("BlockingQueue > get > started")
        l.debug("Get > Checking self.full address", self.full)
        l.debug("self.full._value", self.full._value)
        self.full.acquire()
        l.debug("BlockingQueue > get > full.aquire() finished")
        self.qLock.acquire()
        l.debug("BlockingQueue > get > qLock.aquire() finished")
        try:
            item = self.queue.get()
            l.debug("BlockingQueue > get > queue.get() finished")
        finally:
            self.qLock.release()
        self.empty.release()
        return item
    
    def isEmpty(self):
        l.debug("empty > self.empty._value < 1 is: ", self.empty._value < 1)
        return self.empty._value < 1