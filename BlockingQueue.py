from threading import Semaphore, Lock
from queue import Queue
import log as l

class BlockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = Queue(capacity)
        
        # semaphores that track empty and full "slots"
        self.empty = Semaphore(capacity)  
        self.full = Semaphore(0)
        # mutex - mutually exclusive lock. protects the queue
        self.qLock = Lock()

    def put(self, item):
        l.debug("BlockingQueue > put > started")
        # decrements empty if greater than zero, else it blocks
        self.empty.acquire()
        self.qLock.acquire()
        try:
            self.queue.put(item)
        finally:
            # always release the lock
            self.qLock.release()
        # produces 1 full item
        self.full.release()
        l.debug("self.full._value:", self.full._value)

    def get(self):
        l.debug("BlockingQueue > get > started")
        self.full.acquire()
        self.qLock.acquire()
        try:
            item = self.queue.get()
        finally:
            self.qLock.release()
        self.empty.release()
        l.debug("self.empty._value:", self.empty._value)
        return item
    