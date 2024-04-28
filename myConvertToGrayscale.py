#!/usr/bin/env python3

import cv2

def colorToGrayscale(coloredFramesQueue, grayscaleFramesQueue):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = coloredFramesQueue.get()

        #check if there's no more frames
        if frame is None:
            break

        print(f'Converting frame {count}')        
        
        # grayscale magic
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # put the grayscale frame in the grayscale queue
        grayscaleFramesQueue.put(grayFrame)
        

        count += 1
    # relay the None signal to the grascale queue that there's no more frames left to process
    grayscaleFramesQueue.put(None)