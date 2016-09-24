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

vVerbose = str(sys.argv[1])
q = Queue.LifoQueue(maxsize=1)
boolRun = Queue.LifoQueue(maxsize=1)
    
if vVerbose.startswith('test'):
    print 'MT: Starting'

t1 = threading.Thread(target=threadSensors, args=(q, boolRun, vVerbose,))
t2 = threading.Thread(target=threadLogic, args=(q, boolRun, vVerbose,))

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

if not vVerbose.startswith('test'):
    os.system("sudo init 0")

print 'MT: -Ende-'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
