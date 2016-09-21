#!/usr/bin/python
# -*- coding: latin-1 -*-

from   rfm69 import Rfm69
import rfm69
import bme280
from   sensors import rawsensor
import time, datetime  # time functions
import ast
import sys
from sensorCrypt import sensorCrypt

# HTTP Service Einstellungen
#import requests  # library for sending data over http
import socket  # to find out our local ip
import httpservice  # for rt service
from sensorConfig import sensorConfig

# config einlesen
print 'sensorService starts'
vVerbose = str(sys.argv[1])
sConfig = sensorConfig('/home/pi/sensorTool/sensorTool.conf', vVerbose)

sCrypt = sensorCrypt(sConfig.getCryptKey())
httpdport = sConfig.getHttpdPort()
# print httpdport
print 'sensorService config'
sConfig = None

# HTTP Service initialisieren
ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
print 'IP: ' + str(ip) +':'+str(httpdport)

httpServices = {}
# HTTPService for every sensor in actual usage not needed
# for vKey in dictSensors:
#    #print dictSensors
#    if dictSensors[vKey]['port'] > 0:
#        httpServices[vKey] = httpservice.Service(dictSensors[vKey]['port'])
#        if (vVerbose == 'test'):
#            print str(dictSensors[vKey]['name']) + ': '+ str(ip) + ':' + str(dictSensors[vKey]['port'])

print httpdport
# One HTTPService for all sensors
httpDall = httpservice.Service(httpdport)

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
print 'sensorTool: Rfm69 initialized'
 
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

refreshTime = 0
boolTX35 = True
print 'sensorTool started (' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ')'
while 1:
    if time.time() > refreshTime:
        if boolTX35:
            if vVerbose.startswith('test'):
                print 'TX35'
            rfm.SetParams(Datarate=9.579)  # 17.241, #kbit/s baudrate
            refreshTime = time.time() + refreshTX35
            boolTX35 = False
        else:
            if vVerbose.startswith('test'):
                print 'TX29'
            rfm.SetParams(Datarate=17.241)  # 9.579, #17.241, #kbit/s baudrate
            refreshTime = time.time() + refreshTX29
            boolTX35 = True
    
    data = rfm.ReceivePacket(7)
    obj = rawsensor.CreateSensor(data)
    vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     for vHTTPd in httpServices:
#         # print vHTTPd
#         # print dictSensors[vHTTPd]
#         if httpServices[vHTTPd].provideData(sCrypt.Encrypt(dictSensors[vHTTPd])):
#         # if httpServices[vHTTPd].provideData(dictSensors[vHTTPd]):
#             if vVerbose.startswith('test'):
#                 print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpServices[vHTTPd].addr[0]

    vData = sCrypt.Encrypt(str(dictSensors))
    # vData = dictSensors
    try:
        if httpDall.provideData(vData):
        # if httpDall.provideData(dictSensors):
            if vVerbose.startswith('test'):
                print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpDall.addr[0]
    except:
        pass

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

        if vVerbose.startswith('test'):
            print 'T1: Sensors Thread'
            for vKey in dictSensors:
                print 'T1:  ' + str(vKey) + ': ' + str(dictSensors[vKey])
    time.sleep(0.1)

if vVerbose.startswith('test'):
    print 'script Ende'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
