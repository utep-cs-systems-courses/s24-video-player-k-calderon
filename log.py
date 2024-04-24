import sys
import time

startTime = time.time() * 1000

debugLogging = False
timestampLogging = False

if ("--debug") in sys.argv:
    debugLogging = True
if ("--timestamp") in sys.argv:
    timestampLogging = True

def getMsgTimestamp():
    return round(time.time() * 1000 - startTime)
def log(msg, obj = None):
    if timestampLogging:
        msg = str(getMsgTimestamp()) + "ms > " + msg
    if obj is not None:
        msg = msg + " > " + str(obj)
    print(msg)
def debug(msg, obj = None):
    if debugLogging:
        msg = "DEBUG > " + msg
        log(msg, obj)