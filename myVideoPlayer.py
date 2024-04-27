#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
import log as l
import sys
import os
from BlockingQueue import BlockingQueue
from myExtractFrames import extractFrames
from myDisplayFrames import displayFrames

# take and parse user arguments
# filename
# grayscale

def main2():
    filename = "clip.mp4"
    maxFrames = 72
    queueCapacity = 10

    grayscaleHandler = BlockingQueue(queueCapacity)
    displayHander = BlockingQueue(queueCapacity)
    # Create thread to run Extracting frames in parallel
    extractWorker = threading.Thread(target=extractFrames, args=(filename,coloredFramesQueue,10000))
    extractWorker.start()

    # Create thread to run color to grayscale function in parallel
    #grayscaleWorker = threading.Thread(target=colorToGrayscale,args=(coloredFramesQueue,grayscaleFramesQueue))
    #grayscaleWorker.start()

    # Create thread to run display frames in parallel 
    displayWorker = threading.Thread(target=displayFrames,args=(grayscaleFramesQueue,))
    displayWorker.start()

    # Join all created threads to main thread
    extractWorker.join()
    grayscaleWorker.join()
    displayWorker.join()
def main():
    filename = 'clip.mp4'
    maxFrames = 72
    queue_capacity = 10

    # Create a shared BlockingQueue
    extractionQueue = BlockingQueue(queue_capacity)
    l.debug("Initialized extractionQueue", extractionQueue)

    # Fork a process
    pid = os.fork()

    if pid == 0:
        l.debug("Child process: responsible for extracting frames")
        # Child process: responsible for extracting frames
        l.debug("Child > passing exQ to extractFrames", extractionQueue)
        extractFrames(filename, extractionQueue, maxFrames)
    else:
        # Parent process forks again to create another process for display
        pid = os.fork()
        if pid == 0:
            l.debug("Second child process: responsible for displaying frames")
            # Second child process: responsible for displaying frames
            l.debug("Child > passing exQ to displayFrames", extractionQueue)
            displayFrames(extractionQueue)
        else:
            l.debug("Parent process waits for child processes to finish")
            # Parent process waits for child processes to finish
            os.wait()

if __name__ == "__main__":
    main()


'''
# filename of clip to load
filename = 'clip.mp4'

# shared queue  
extractionQueue = BlockingQueue(10)

# extract the frames
extractFrames(filename,extractionQueue, 72)

# display the frames
displayFrames(extractionQueue)
'''