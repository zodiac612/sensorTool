#!/usr/bin/python
# -*- coding: latin-1 -*-

from   rfm69 import Rfm69
import rfm69
import bme280
import sensors
from   sensors import rawsensor
import time, datetime # time functions
import ast
import ConfigParser
import io, sys, ast

# HTTP Service Einstellungen
import requests # library for sending data over http
import socket # to find out our local ip
import httpservice # for rt service

#config einlesen
config = ConfigParser.ConfigParser()
config.read('/home/pi/sensorTool/sensorTool.conf')
#print config.sections()

#ACTINTERVAL    = config.getint('lacrosse', 'actinterval')
#MAXTIME        = config.get('global', 'maxtime')
#vLogFile       = config.get('lacrosse', 'logfile')
httpdport      = config.getint('lacrosse', 'httpdport')
#print httpdport
SERVER         = config.get('db', 'server')
PASSWORD       = config.get('db', 'password')
HTTP_TIMEOUT   = config.getint('db', 'http_timeout')
vVerbose       = str(sys.argv[1])

# Sensorspeicher
dictSensors    = {}
if config.has_section('Sensor0'):
    iSensor = 0
    while config.has_section('Sensor' + str(iSensor)):
        dictSensor = {}
        boolBME280 = False
        try:    boolBME280                = config.getboolean('Sensor'+str(iSensor), 'bme280')
        except: pass
        
        if boolBME280:
            dictSensor['id']                    = 'bme280'
        else:
            try:
                dictSensor['id']                    = config.get('Sensor'+str(iSensor), 'hex')
            except:
                dictSensor['id']                    = 'none'
                
        try:    dictSensor['name']                  = config.get('Sensor'+str(iSensor), 'name')
        except: dictSensor['name']                  = 'unkown'
        try:    dictSensor['port']                  = config.getint('Sensor'+str(iSensor), 'httpdport')
        except: pass
        
        if dictSensor['id'] <> 'none':
            dictSensors[dictSensor['id']] = dictSensor
        iSensor = iSensor + 1
    #While iSensor < CountOfSensors:
else:
    exit()
    
#HTTP Service initialisieren
ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

httpServices = {}
# HTTPService for every sensor in actual usage not needed
#for vKey in dictSensors:
#    #print dictSensors
#    if dictSensors[vKey]['port'] > 0:
#        httpServices[vKey] = httpservice.Service(dictSensors[vKey]['port'])
#        if (vVerbose == 'test'):
#            print str(dictSensors[vKey]['name']) + ': '+ str(ip) + ':' + str(dictSensors[vKey]['port'])

print httpdport
# One HTTPService for all sensors
httpDall = httpservice.Service(httpdport)
# Verbose Einstellungen
#if vVerbose == "test":
#    ACTINTERVAL = config.getint('test', 'test_actinterval')
 #   MAXTIME     = config.get('test', 'test_maxtime')

#Initiiern
#refreshTimeAct = time.time() + ACTINTERVAL

#Empfaenger Modul starten
rfm = Rfm69()
 
rfm.SetParams(
    Freq = 868.300, #MHz center frequency
    Datarate = 9.579, #17.241, #kbit/s baudrate
    ModulationType = rfm69.FSK, #modulation
    SyncPattern = [0x2d, 0xd4], #syncword
    Bandwidth = 200, #kHz bandwidth
    LnaGain = 0x88
    )
     
#print hex(rfm.ReadReg(0x07))
#print hex(rfm.ReadReg(0x08))
#print hex(rfm.ReadReg(0x09))
 
data = []

# Werte empfangene Daten bis MAXTIME aus
#while time.strftime('%H%M') < MAXTIME:
while 1:
    data = rfm.ReceivePacket(7)
    obj = rawsensor.CreateSensor(data)
    vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    for vHTTPd in httpServices:
        #print vHTTPd
        #print dictSensors[vHTTPd]
        if httpServices[vHTTPd].provideData(dictSensors[vHTTPd]):
            if vVerbose == 'test':
                print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpServices[vHTTPd].addr[0]

    if httpDall.provideData(dictSensors):
            if vVerbose == 'test':
                print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpDall.addr[0]
    #Betrachte nur La Crosse Daten
    if str(obj)[0:3] == 'La ':
        vSensor = ast.literal_eval(str(obj)[10:])

        # Sicher ist sicher, pruefung ob ID(hex) im Sensorpaket ist.
        if 'ID' in vSensor: 
            vNew = True
            
            #Gehe die vorhandenen Eintraege durch und aktualisiere die vorhanden
            for vKey in dictSensors:
                if vKey == 'bme280':
                    try:
                        (degC, hPa, hRel) = bme280.readData()
                        dictSensors[vKey]['Time'] = vNow
                        dictSensors[vKey]['T']    = round(degC, 2)
                        dictSensors[vKey]['RH']   = round(hRel, 2)
                        dictSensors[vKey]['hPa']  = round(hPa, 2)
                        vNew = False
                    except:
                        pass
                else:        
                    if dictSensors[vKey]['id'] == vSensor['ID']:
                        #print vSensor
                        dictSensors[vKey]['Time'] = vNow
                        if 'T' in vSensor:
                            dictSensors[vKey]['T'] = vSensor['T']
                        if 'RH' in vSensor:
                            dictSensors[vKey]['RH'] = vSensor['RH']
                        vNew = False

            # Wenn der Sensor neu ist, in den Specher aufnehmen
            if vNew:
                dictSensors[vKey]['Time'] = vNow
                if ['T'] in vSensor:
                    dictSensors[vKey]['T'] = vSensor['T']
                if ['RH'] in vSensor:
                    dictSensors[vKey]['RH'] = vSensor['RH']
                    
            if vVerbose == 'test':
                print vSensor
                 
    # Wenn aktualisierungsintervall errecicht, dann schreibe Werte in die Uebergabedatei
#     if time.time() > refreshTimeAct :
#         refreshTimeAct = time.time() + ACTINTERVAL
#  
#         vAct = ''
#         for vKey in dictSensors:
#            vAct = vAct + str(dictSensors[vKey]) + '\n'
#             
#         if vVerbose == "test":
#             print vAct   
#  
#         # In Aktueller Wert LOG-File schreiben
#         fileHandle = open (vLogFile, 'w')
#         fileHandle.write ( vAct )
#         fileHandle.close()
 
        #time.sleep(0.1)
 
if vVerbose == "test":
    print 'script Ende'

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
