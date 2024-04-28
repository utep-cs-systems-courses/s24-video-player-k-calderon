#!/usr/bin/env python3

import cv2
import base64

def extractFrames(fileName, coloredFramesQueue, maxFramesToLoad=9999):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        if not success:
            break

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        coloredFramesQueue.put(image)
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print('Frame extraction complete')
    coloredFramesQueue.put(None)      # End of frame
