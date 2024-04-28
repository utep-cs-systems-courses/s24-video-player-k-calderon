#!/usr/bin/env python3

import cv2

def extractFrames(fileName, coloredFramesQueue, maxFramesToLoad=9999):
    # frame counter
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print(f'Reading frame {count} {success}')
    while success and count < maxFramesToLoad:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        # break if the frame couldn't be read
        if not success:
            break

        # add the frame to the buffer
        coloredFramesQueue.put(image)

        # extract the next frame and get ready for the next loop
        success,image = vidcap.read()
        print(f'Reading frame {count} {success}')
        count += 1

    print('Frame extraction complete')
    # signal frame extraction is complete with None
    coloredFramesQueue.put(None)
