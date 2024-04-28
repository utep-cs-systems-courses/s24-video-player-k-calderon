import threading
import cv2
import numpy as np
import base64
import queue
import log as l

def displayFrames(grayscaleFramesQueue):
    # initialize frame count
    count = 0

    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frame = grayscaleFramesQueue.get()

        if frame is None:
            break

        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1


    print('Finished displaying all frames')
    # cleanup the windows
    cv2.destroyAllWindows()
