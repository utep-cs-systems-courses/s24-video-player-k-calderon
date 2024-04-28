#!/usr/bin/env python3

import threading
import log as l
from BlockingQueue import BlockingQueue
from myExtractFrames import extractFrames
from myDisplayFrames import displayFrames
from myConvertToGrayscale import colorToGrayscale


def main():
    filename = 'clip.mp4'
    maxFramesToLoad = 10000

    coloredFramesQueue = BlockingQueue(10)
    grayscaleFramesQueue = BlockingQueue(10)

    # create and run the frame extraction thread
    extractThread = threading.Thread(target=extractFrames, args=(filename,coloredFramesQueue, maxFramesToLoad))
    extractThread.start()

    # create and run the grayscale converter thread
    grayscaleThread = threading.Thread(target=colorToGrayscale,args=(coloredFramesQueue,grayscaleFramesQueue))
    grayscaleThread.start()

    # create and run the frame displaying thread
    displayThread = threading.Thread(target=displayFrames,args=(grayscaleFramesQueue,))
    displayThread.start()

    '''
    join() blocks main until the thread it's attached to is done.
    join can be thought of as a "wait"
    so this is making sure all the threads finish before the main progresses
    in this case, there's not really anyhing left to do, but join is useful if there was
    '''
    extractThread.join()
    grayscaleThread.join()
    displayThread.join()
    l.log("All done")
    

if __name__ == "__main__":
    main()