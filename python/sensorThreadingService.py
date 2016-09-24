#!/usr/bin/env python2.7
# -*- coding: latin-1 -*-
# testskript fuer threading

from   rfm69 import Rfm69
import rfm69
import bme280
from   sensors import rawsensor
import time, datetime  # time functions
import ast

def threadSensors(out_q, vVerbose=''):
#def threadSensors(vVerbose=''):
    vDebug = vVerbose
    vDebug = 'test'
    print str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'- Anfang -'+'\n'
    if vDebug.startswith('test'):
        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'w')
        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'- Anfang -'+'\n')
        fileHandle.close()
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

    if vDebug.startswith('test'):
        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'RFM initialized'+'\n')
        fileHandle.close()
        pass

 
    data = []
    dictSensors = {}
    dictSensors['bme280'] = {}

    # Werte empfangene Daten bis MAXTIME aus
    # while time.strftime('%H%M') < MAXTIME:
    refreshTime = 0
    refreshTX35 = 18
    refreshTX29 = 10
    #if vVerbose.startswith('test'):
    #    refreshTX35 = 9
    #    refreshTX29 = 5
    
    refreshTime = 0
    
    iInterval = refreshTX35 + refreshTX29 + 1
    refreshTime2 = time.time() + iInterval
    boolTX35 = True
    boolRun = True
    #iCountRuns = 0
#    while 1:
    if vDebug.startswith('test'):
        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'SensorService starts while'+'\n')
        fileHandle.close()
        pass

    while boolRun:
        print 'while'
        #if not boolRunQ.empty():
        #    boolRun = boolRunQ.get()
        #    if vVerbose.startswith('test'):
        #        print 'T1: boolRun = ' + str(boolRun) 
            
        if time.time() > refreshTime:
             
            if boolTX35:
                try:
                    if vDebug.startswith('test'):
                        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': TX 35'+'\n')
                        fileHandle.close()
                        print 'TX35'
                        rfm.SetParams(Datarate=9.579),  # 17.241, #kbit/s baudrate
                except Exception as e:
                    if vDebug.startswith('test'):
                        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': TX35 ' + str(e)+'\n')
                        fileHandle.close()
                    pass
                refreshTime = time.time() + refreshTX35
                boolTX35 = False
            else:
                try:
                    if vDebug.startswith('test'):
                        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': TX 29'+'\n')
                        fileHandle.close()
                        print 'TX29'
                        rfm.SetParams(Datarate=17.241),  # 17.241, #kbit/s baudrate
                except Exception as e:
                    if vDebug.startswith('test'):
                        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': TX29 ' + str(e)+'\n')
                        fileHandle.close()
                        print str(e)
                    pass
                refreshTime = time.time() + refreshTX29
                boolTX35 = True
                
            #iCountRuns = iCountRuns + 1

        obj = None
        data = rfm.ReceivePacket(7)
        obj = rawsensor.CreateSensor(data)
        try:
            pass
        except Exception as e:
            if vDebug.startswith('test'):
                fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': ' + str(e)+'\n')
                fileHandle.close()
            print str(e)
            pass
            
        vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # bme280 values to dictsensor
        try:
            (degC, hPa, hRel) = bme280.readData()
            dictSensors['bme280']['Time'] = vNow
            dictSensors['bme280']['T'] = round(degC, 2)
            dictSensors['bme280']['RH'] = round(hRel, 2)
            dictSensors['bme280']['hPa'] = round(hPa, 2)
            vNew = False
        except Exception as e:
            if vDebug.startswith('test'):
                fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': ' + str(e)+'\n')
                fileHandle.close()
            print str(e)
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

        if vDebug.startswith('test'):
            fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
            fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': T1 Sensors:'+'\n')
            for vKey in dictSensors:
                fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': T1:  ' + str(vKey) + ': ' + str(dictSensors[vKey])+'\n')
                print ': T1:  ' + str(vKey) + ': ' + str(dictSensors[vKey])+'\n'
            fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': T1: out_q leer: ' + str(out_q.empty())+'\n')
            fileHandle.close()
            
        
        if time.time() > refreshTime2:
            
            if vDebug.startswith('test'):
                fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': ' + 'T1: Q.PUT nach ' + str(refreshTime2) + 's'+'\n')
                fileHandle.close()
                pass
            refreshTime2 = time.time() + iInterval
            try:
                if not out_q.empty():
                    out_q.get()
                    out_q.task_done()
           
                out_q.put(dictSensors)
            except Exception as e:
                if vDebug.startswith('test'):           
                    fileHandle = open ('/var/sensorTool/sServiceErr.log', 'a')
                    fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+': ' + str(e)+'\n')
                    fileHandle.close()
                print str(e)
        time.sleep(0.1)

    if vDebug.startswith('test'):
        fileHandle = open ('/var/sensorTool/sServiceErr.log', 'w')
        fileHandle.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+'- Ende -\n')
        fileHandle.close()
        
#threadSensors('test')        

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
