#!/usr/bin/env python2.7
# -*- coding: latin-1 -*-
# testskript fuer threading

from   rfm69 import Rfm69
import rfm69
import bme280
from   sensors import rawsensor
import time, datetime  # time functions
import ast
# from Queue import Queue
# from threading import Thread

def threadSensors(out_q, boolRunQ, vVerbose=''):
    # Empfaenger Modul starten
    rfm = Rfm69()
     
    rfm.SetParams(
        Freq=868.300,  # MHz center frequency
        Datarate=9.579,  # 17.241, #kbit/s baudrate
        ModulationType=rfm69.FSK,  # modulation
        SyncPattern=[0x2d, 0xd4],  # syncword
        Bandwidth=200,  # kHz bandwidth
        LnaGain=0x88
        )
 
    data = []
    dictSensors = {}
    dictSensors['bme280'] = {}

    # Werte empfangene Daten bis MAXTIME aus
    # while time.strftime('%H%M') < MAXTIME:
    refreshTime = 0
    refreshTX35 = 18
    refreshTX29 = 10
    if vVerbose.startswith('test'):
        refreshTX35 = 9
        refreshTX29 = 5
    
    iInterval = refreshTX35 + refreshTX29 + 1
    refreshTime2 = time.time() + iInterval
    boolTX35 = True
    boolRun = True
    iCountRuns = 0
#    while 1:
    while boolRun:
        if not boolRunQ.empty():
            boolRun = boolRunQ.get()
            if vVerbose.startswith('test'):
                print 'T1: boolRun = ' + str(boolRun) 
            
        if time.time() > refreshTime:
            if boolTX35:
                if vVerbose.startswith('test1'):
                    print 'T1: TX35'
                rfm.SetParams(Datarate=9.579),  # 17.241, #kbit/s baudrate
                refreshTime = time.time() + refreshTX35
                boolTX35 = False
            else:
                if vVerbose.startswith('test1'):
                    print 'T1: TX29'
                rfm.SetParams(Datarate=17.241)  # 9.579, #17.241, #kbit/s baudrate
                refreshTime = time.time() + refreshTX29
                boolTX35 = True
            iCountRuns = iCountRuns + 1

        data = rfm.ReceivePacket(7)
        obj = rawsensor.CreateSensor(data)
        vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # bme280 values to dictsensor
        try:
            (degC, hPa, hRel) = bme280.readData()
            dictSensors['bme280']['Time'] = vNow
            dictSensors['bme280']['T'] = round(degC, 2)
            dictSensors['bme280']['RH'] = round(hRel, 2)
            dictSensors['bme280']['hPa'] = round(hPa, 2)
            vNew = False
        except:
            pass

        # Betrachte nur La Crosse Daten
        if str(obj)[0:3] == 'La ':
            vSensor = ast.literal_eval(str(obj)[10:])
            
            if vSensor['ID'] not in dictSensors:
                dictSensors[vSensor['ID']] = {}  

            dictSensors[vSensor['ID']]['Time'] = vNow
            if 'T' in vSensor:
                dictSensors[vSensor['ID']]['T'] = vSensor['T']
            if 'RH' in vSensor:
                dictSensors[vSensor['ID']]['RH'] = vSensor['RH']
        
        if vVerbose.startswith('test1'):
            print 'T1: Sensors Thread'
            for vKey in dictSensors:
                print 'T1:  ' + str(vKey) + ': ' + str(dictSensors[vKey])
        
        if vVerbose.startswith('test1'):
            print 'T1: out_q leer: ' + str(out_q.empty())            
        
        if time.time() > refreshTime2:
            if vVerbose.startswith('test'):
                print 'T1: Q.PUT nach ' + str(refreshTime2) + 's'
            refreshTime2 = refreshTime2 + iInterval
            if not out_q.empty():
                out_q.get()
                out_q.task_done()
            
            out_q.put(dictSensors)            

#        if iCountRuns == 2:
#            boolRun = False

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4