from threading import Semaphore, Lock
from queue import Queue

class BlockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = Queue(capacity)  # This is a FIFO queue
        
        # semaphores that track empty and full "slots"
        self.empty = Semaphore(capacity)  
        self.full = Semaphore(0)
        # mutex - mutually exclusive lock. protects the queue  
        self.qLock = Lock()

    def put(self, item):
        # decrements empty if greater than zero, else it blocks
        self.empty.acquire() 
        try:
            self.qLock.acquire() 
            self.queue.put(item)
        finally:
            # always release the lock
            self.qLock.release()
        # produces 1 full item
        self.full.release()

    def get(self):
        self.full.acquire()
        try:
            self.qLock.aquire()
            item = self.queue.get()
        finally:
            self.qLock.release()
        self.empty.release()
        return item