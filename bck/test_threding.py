#!/usr/bin/env python2.7
# -*- coding: latin-1 -*-
# testskript fuer threading
#from queue import Queue

import Queue 
import threading# import Thread
from sensorThreadingSensors import threadSensors
from sensorThreadingLogic import threadLogic
import sys
import time
#import gpio  # led output
#import ConfigParser
import os

def threadLogic():
    iI = 0
    refreshTime = time.time() + 1
    while iI < 30:
        if time.time() > refreshTime:
            refreshTime = time.time() + 4
            print 't2: ' + str(iI)
            iI = iI + 1

def threadSensors():
    iI = 0
    refreshTime = time.time()
    while iI < 30:
        if time.time() > refreshTime:
            refreshTime = time.time() + 4
            print 't1: ' + str(iI)
            iI = iI + 1

vVerbose = str(sys.argv[1])
q = Queue.Queue(maxsize=1)
boolRun = True
    
if vVerbose.startswith('test'):
    print 'MT: Starting'

t1 = threading.Thread(target=threadSensors, args=())
t2 = threading.Thread(target=threadLogic, args=())

if vVerbose.startswith('test'):
    print 'MT: Starting Thread1'
t1.start()

if vVerbose.startswith('test'):
    print 'MT: Starting Thread1'
t2.start()

# refreshtime = time.time() + INTERVAL_A
# iCountTestTime = 0
# boolRun = True
# 
# #while time.strftime('%H%M') < MAXTIME:  # timeDuration <= MAXTIME: 
# while boolRun:
#     iThreads = 0;
#     if time.time() > refreshtime:
#         refreshtime = time.time() + INTERVAL_A
#         
#         if vVerbose.startswith('test'): 
#             iCountTestTime = iCountTestTime + 1
#             if vVerbose.startswith('test1'):
#                 print 'MT: Threads: ' + str(threading.enumerate())
#             print 'MT: Threadanzahl: ' + str(iThreads) + ' - ' + str(iCountTestTime)
#     
# #        if t1.is_alive() and t1.is_alive():
# #            LedR.off()
# #        else:
# #            LedR.on()
#             
#         if iCountTestTime == 10 or (time.strftime('%H%M') >= MAXTIME):
#             boolRunT2.put(False)
#             boolRunT1.put(False)
#             boolRun = False
#         
#         #iThreads = threading.active_count()
#         #if iThreads == 1:# or (time.strftime('%H%M') < MAXTIME):
#         #   boolRun = False
#     
#    if iThreads == 2:
#        t1.start()
# if vVerbose.startswith('test'):
#     print 'MT: GPIOs off'        
# RelayIN1.off()
# RelayIN2.off()
# LedR.off()
# LedY.off()
# LedG.off()

print 'MT: -Ende-'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
