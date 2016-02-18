#!/usr/bin/python
# -*- coding: latin-1 -*-

# include libraries -----------------------------------------------------------

import time, datetime  # time functions
import requests  # library for sending data over http
import socket  # to find out our local ip
import thread  # loop is slow, needed for fast led pulse
import bme280  # , tsl2591 # libraries for our sensors
import gpio  # led output
import httpservice  # for rt service
import os, sys, ast
from whatsapp import sendWhatsApps
import ConfigParser
from tx35dth import tx35dth
from fritzActor import fritzActor
from sensorHistory import sensorHistory
import base64
from sensorCrypt import sensorCrypt

config = ConfigParser.ConfigParser()
config.read('/home/pi/sensorTool/sensorTool.conf')
vVerbose = str(sys.argv[1])
if vVerbose == "test":
    print config.sections()

# constants -------------------------------------------------------------------

sCrypt = sensorCrypt(config.get('global', 'cryptkey'))
INTERVAL = config.getint('inmonitor', 'data_save_interval')
MAXTIME = config.get('global', 'maxtime') 
MINTIME = config.get('global', 'mintime') 
INTERVAL_A = 600

if vVerbose == "test":
    INTERVAL = config.getint('test', 'test_data_save_interval')
    MAXTIME = config.get('test', 'test_maxtime')
    INTERVAL_A = 20
    
TriggerCountA = config.getint('inmonitor', 'trigger_start_count')
TriggerCountB = config.getint('inmonitor', 'trigger_end_count')
SERVER = config.get('db', 'server')
PASSWORD = config.get('db', 'password')
HTTP_TIMEOUT = config.getint('db', 'http_timeout')

dictIntervalle = {}
iIntervall = 1
while iIntervall < 100:
    try:
        dictIntervall = {}
        dictIntervall['start'] = config.get('inmonitor', 'intervalstart_' + str(iIntervall))
        dictIntervall['stop'] = config.get('inmonitor', 'intervalstop_' + str(iIntervall))
        # print dictIntervall
        dictIntervalle[iIntervall] = dictIntervall
        iIntervall = iIntervall + 1
    except: iIntervall = 100
# print dictIntervalle

vTitel = config.get('inmonitor', 'titel')
CountOfSensors = config.getint('inmonitor', 'count_of_sensors')

dictActors = {}    
dictSensors = {}
iControlSensor = None
sH_Log = sensorHistory()
iLog = 0
if CountOfSensors > 0:
    iSensor = 0
    while iSensor < CountOfSensors:
        dictSensor = {}
        try:    dictSensor['bme280'] = config.getboolean('Sensor' + str(iSensor), 'bme280')
        except: dictSensor['bme280'] = False
        try:    dictSensor['hex'] = config.get('Sensor' + str(iSensor), 'hex')
        except:
            if dictSensor['bme280']:
                dictSensor['hex'] = 'bme280'
            else:
                dictSensor['hex'] = 'none'   
                     
        try:    dictSensor['name'] = config.get('Sensor' + str(iSensor), 'name')
        except: dictSensor['name'] = 'unkown'
        try:    dictSensor['message'] = config.get('Sensor' + str(iSensor), 'message')
        except: dictSensor['message'] = 'no message defined'
        try:    dictSensor['delta_message'] = config.get('Sensor' + str(iSensor), 'delta_message')
        except: dictSensor['delta_message'] = 'no delta message defined'
        try:    dictSensor['delta_humidity'] = config.getfloat('Sensor' + str(iSensor), 'delta_humidity')
        except: pass
        try:    dictSensor['delta_temperature'] = config.getfloat('Sensor' + str(iSensor), 'delta_temperature')
        except: pass
        try:    dictSensor['threshold_low_humidity'] = config.getfloat('Sensor' + str(iSensor), 'threshold_low_humidity')
        except: pass
        try:    dictSensor['threshold_low_temperature'] = config.getfloat('Sensor' + str(iSensor), 'threshold_low_temperature')
        except: pass
        try:    dictSensor['threshold_high_humidity'] = config.getfloat('Sensor' + str(iSensor), 'threshold_high_humidity')
        except: pass
        try:    dictSensor['threshold_high_temperature'] = config.getfloat('Sensor' + str(iSensor), 'threshold_high_temperature')
        except: pass
        try:    dictSensor['trigger_count'] = config.getint('Sensor' + str(iSensor), 'trigger_count')
        except: dictSensor['trigger_count'] = 0
        try:    dictSensor['fritzactor'] = config.get('Sensor' + str(iSensor), 'fritzactor')
        except: pass
        try:
            if config.getboolean('Sensor' + str(iSensor), 'control_radiator'):
                iControlSensor = iSensor
        except: pass  
        iMobile = 1
        dictMobile = {}
        while iMobile < 100:
            try:    
                dictMobile[iMobile] = config.get('Sensor' + str(iSensor), 'mobile' + str(iMobile))
                iMobile = iMobile + 1
            except: iMobile = 100
        dictSensor['mobiles'] = dictMobile
        if dictSensor['hex'] <> 'none':
            dictSensors[iSensor] = tx35dth(dictSensor)
        iSensor = iSensor + 1
    # While iSensor < CountOfSensors:

if vVerbose == "test":
    print 'control_radiator = Sensor' + str(iControlSensor)

RelayIN1 = gpio.GPIOout(12)
RelayIN2 = gpio.GPIOout(16)
LedG = gpio.GPIOout(36)
LedY = gpio.GPIOout(40)
LedR = gpio.GPIOout(38)
vBoolLC = True
RelaisStarted = False
RelaisActive = True
# fritz off moved after first fritzactors call
# RelayIN1.off()
# RelayIN2.off()
LedG.off()
LedY.off()
LedR.off()

degC = 0
hPa = 0
hRel = 0
degC1 = 0
hPa1 = 0
vBoolSensor1 = True
counterHigh = 0
counterLow = 0
timeDuration = 0

# functions for print out and WhatsApp
def getInfoText(vStatus):
    vHeader = vTitel
    if vVerbose == "test":
        vHeader += ' Test\n'
    else:
        vHeader += '\n'
    
    vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + vStatus
    vSensorPaket = ''
    for vKey in dictSensors:
        vSensorPaket += '\n ' + str(dictSensors[vKey].GetInfo(False, False))
    
    vActorsPaket = ''
    for vAKey in dictActors:
        vActorsPaket += '\n' + str(dictActors[vAKey].GetInfo(False, False))
        
    vGPIOStatus = ''
    vGPIOStatus += '\n Relais: ' + str(RelaisStarted) + ' (' + str(RelayIN1.isOn) + '|' + str(RelayIN2.isOn) + ')'
    vGPIOStatus += '\n Code:   ' + str(timeDuration) + ';' + str(counterHigh) + ';' + str(counterLow)
    vGPIOStatus += '\n LED:    ' + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn)
        
    vReturnText = vHeader + vNow + vSensorPaket + vActorsPaket + vGPIOStatus  # + str(dictActors)
    return vReturnText

# print CSV
def getInfoCSV():
    vReturnText = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ';'
    vReturnText = vReturnText + str(RelaisStarted) + ';'
    vReturnText = vReturnText + str(timeDuration) + ';' + str(counterHigh) + ';' + str(counterLow) + ";"
    vReturnText = vReturnText + str(RelayIN1.isOn) + str(RelayIN2.isOn) + ";"
    vReturnText = vReturnText + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn) + ";"
    
    for vKey in dictSensors:
        vReturnText = vReturnText + str(dictSensors[vKey].GetInfo(True, False))
    return vReturnText

# print html status output
def getHTML():
    vhttpResult = ''
    vhttpResult += '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
    vhttpResult += '<html xmlns="http://www.w3.org/1999/xhtml">'
    vhttpResult += '<head>'
    vhttpResult += '<title>Raspberry PI Status</title>'
    vhttpResult += '<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-15" />'
    vhttpResult += '</head>'
    vhttpResult += '<body bgcolor="#CCCCCC">'
    vhttpResult += '<h3>Raspberry PI SensorTool Status<BR />' + datetime.datetime.now().strftime('%Y-%m-%d') + '</h3>'
    for vKey in dictSensors:
        vhttpResult += dictSensors[vKey].GetHttpTable()

    for vAKey in dictActors:
        vhttpResult += dictActors[vAKey].GetHttpTable()
    
    vhttpResult += '<DIV MARGIN=5><TABLE BORDER=1><TR>'
    vhttpResult += '<TD width=100><strong>GPIO</strong></TD>'
    vhttpResult += '<TD width=60>RELAIS</TD>'
    vhttpResult += '<TD width=60>LED</TD>'
    vhttpResult += '</TR><TR>'
    vhttpResult += '<TD>' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[11:19] + '</TD>'
    vhttpResult += '<TD>' + str(RelayIN1.isOn) + str(RelayIN2.isOn) + '</TD>'
    vhttpResult += '<TD>' + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn) + '</TD>'
    vhttpResult += '</TR></TABLE></DIV>'
    vhttpResult += '<BR /><BR />'
    vhttpResult += sH_Log.GetHttpTable()
    vhttpResult += '</body>'
    vhttpResult += '</html>'
    return vhttpResult

# find out private ip address -------------------------------------------------
ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
# init  -----------------------------------------------------------------------

httpd = httpservice.Service(8086)
sH_Log.Add('Httpservice started: ' + str(ip) + ':8086')
# led = gpio.GPIOout(26)
# refresh for sensor data
refreshTime = time.time() + INTERVAL
# refresh for fritz actors
refreshTime2 = time.time()

# loop ------------------------------------------------------------------------

while time.strftime('%H%M') < MAXTIME:  # timeDuration <= MAXTIME: 
    
    # Get Status HTML
    vhttpResult = getHTML()
    
    # provide Status HTML with httpservice
    if httpd.provideData(vhttpResult, True):
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpd.addr[0]
    #    print 1234

    # get fritz actor data
    if time.time() > refreshTime2:
        print 'Fritz Actor'
        command = "/home/pi/sensorTool/sh/fritzbox-smarthome.sh csvlist"  # raw_input("Kommando: ")
        try:
            handle = os.popen(command)
            line = " "
            while line:
                line = handle.readline()
                if len(line) > 0:
                    dictActor = {}
                    dictActor = ast.literal_eval(line)
                    if 'id' in dictActor:
                        dictActor['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if dictActor['id'] in dictActors:
                            dictActors[dictActor['id']].UpdateActorData(dictActor)
                        else:
                            dictActors[dictActor['id']] = fritzActor(dictActor)
                    
            handle.close()
        except:
            print str(time.time()) + ': Get fritz actor info failed'
            sH_Log.Add('Get fritz actor info failed')
        
#         for vAKey in dictActors:
#             if dictActors[vAKey].GetPower() == 0:
#                 # sendWhatsApps(dictSensors[2].GetMobiles(), dictActors[vAKey].GetName + ' keine Leistung')
#                 sH_Log.Add(str(dictActors[vAKey].GetName()) + ' keine Leistung!')
        refreshTime2 = time.time() + INTERVAL_A
        
        if vBoolLC:
                dictActors[str(dictSensors[iControlSensor].GetFritzActor())].SetActor(False)
        
    
    # every 10 seconds, try to send data to servers
    if time.time() > refreshTime:
        # print str(refreshTime2) + '##' + str(time.time())
        # Werte holen per http request ::D
        try:
            r = requests.get("http://" + SERVER + ":6666")
            # request enthaelt "
            vR = sCrypt.Decrypt(r.text[1:len(r.text)-1])
            dictResponse = {}
            dictResponse = ast.literal_eval(str(vR))
            for vSensor in dictResponse:
                dictTemp = {}
                dictTemp['ID'] = vSensor
                if 'Time' in dictResponse[vSensor]:
                    dictTemp['Time'] = dictResponse[vSensor]['Time']
                if 'RH' in dictResponse[vSensor]:
                    dictTemp['RH'] = dictResponse[vSensor]['RH']
                if 'T' in dictResponse[vSensor]:
                    dictTemp['T'] = dictResponse[vSensor]['T']
                if 'hPa' in dictResponse[vSensor]:    
                    dictTemp['hPa'] = dictResponse[vSensor]['hPa']
                boolBME280 = False
                if (vSensor == 'bme280') :
                    boolBME280 = True
             
                for vKey in dictSensors:
                    if dictSensors[vKey].GetHex() == vSensor:
                        dictSensors[vKey].SetSensorData(dictTemp, boolBME280)
        except: 
            pass
        
        # Dynamische Config einlesen #soll ueber http request gesteuert werden.
        dynamicConf = ConfigParser.ConfigParser()
        dynamicConf.read('/home/pi/sensorTool/dynamic.conf')
        # print relaisStat.sections()
        
        # Try to change the Relais Status 
        try:
            # print relaisStat.getboolean('relais', 'relais_active')
            # print RelaisActive
            if dynamicConf.getboolean('relais', 'relais_active') != RelaisActive:
                RelaisActive = dynamicConf.getboolean('relais', 'relais_active')
                print ' RelaisActive set to ' + str(RelaisActive)
                sH_Log.Add(' RelaisActive set to ' + str(RelaisActive))
        except: pass
        
        # iterate through sensor data
        for vKey in dictSensors:
            # print relaisStat.getfloat('Sensor' + str(vKey), 'threshold_high_humidity')
            # print dictSensors[vKey].GetThresholdHighHumidity()
            try:
                # print relaisStat.getfloat('Sensor' + str(vKey), 'threshold_high_humidity')
                # print dictSensors[vKey].GetThresholdHighHumidity()
                
                vSetHighRH = False
                if dictSensors[vKey].GetThresholdHighHumidity() == False:
                    vSetHighRH = True
                elif dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_high_humidity') != dictSensors[vKey].GetThresholdHighHumidity():
                    vSetHighRH = True
                
                if vSetHighRH:
                    dictSensors[vKey].SetThresholdHighHumidity(dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_high_humidity'))
                    sH_Log.Add('Threshold High RH S' + str(vKey) +':' + str(dictSensors[vKey].GetThresholdHighHumidity()))
                    if vVerbose == 'test':
                        print 'Threshold High RH S' + str(vKey) +':' + str(dictSensors[vKey].GetThresholdHighHumidity())
            except: pass #Exception, e:
                #import traceback
                #print traceback.format_exc()
            
            try:
                vSetLowT = False
                if dictSensors[vKey].GetThresholdLowTemperature() == False:
                    vSetLowT = True
                elif dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_low_temperature') != dictSensors[vKey].GetThresholdLowTemperature():
                    vSetLowT = True
                
                if vSetHighRH:
                    dictSensors[vKey].SetThresholdLowTemperature(dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_low_temperature'))
                    sH_Log.Add('Threshold Low T S' + str(vKey) +':' + str(dictSensors[vKey].GetThresholdLowTemperature()))
                    if vVerbose == 'test':
                        print 'Threshold Low T S' + str(vKey) +':' + str(dictSensors[vKey].GetThresholdLowTemperature())
                    
            except: pass # Exception, e:
                #import traceback
                #print traceback.format_exc()
        
        timeDuration = timeDuration + INTERVAL
        # print str(timeDuration) + '#' + str(INTERVAL)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        if vBoolLC == True:
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Active"))
            sH_Log.Add('sensorTool started')
            vBoolLC = False
        
        vStunde = time.strftime('%H%M')
        vBoolTimeToCount = False
        for vIv in dictIntervalle:
            # print vStunde + '>' + dictIntervalle[vIv]['start'] + ' and ' + vStunde + ' < ' + dictIntervalle[vIv]['stop']
            if vStunde > dictIntervalle[vIv]['start'] and vStunde < dictIntervalle[vIv]['stop'] and datetime.date.today().weekday() != 6:
                vBoolTimeToCount = True
                
        # print 'dictSensors[0].GetThreshold(): ' + str(dictSensors[0].GetThreshold())
        # print 'dictSensors[0].GetRH(): ' + str(dictSensors[0].GetRH())
        # print 'RelaisStarted: ' + str(RelaisStarted)
        # print 'vBoolTimeToCount ' + str(vBoolTimeToCount)
        # print 'RelaisActive: ' + str(RelaisActive)
        if dictSensors[iControlSensor].GetThreshold() and RelaisStarted == False and vBoolTimeToCount and RelaisActive:
            counterHigh = counterHigh + 1
            if LedY.isOn == False:
                LedY.on()
                sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (H)!')
        else:
            counterHigh = 0
            
        if dictSensors[0].GetThreshold() == False and RelaisStarted and vBoolTimeToCount and RelaisActive:
            counterLow = counterLow + 1
            if LedY.isOn == False:
                LedY.on()
                sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (L)!')
        else:
            counterLow = 0
                
        for vKey in dictSensors:
#            if dictSensors[vKey].GetBME() != True:
            print 
            if iControlSensor <> vKey:
                vBoolThreshold = dictSensors[vKey].GetThreshold()
                print str(iControlSensor) + '-' + str(vKey) + '# threshold ' + str(vBoolThreshold) + '#' +  str(dictSensors[vKey].GetSendMessage())
                
                # Grenzwert
                if vBoolThreshold and dictSensors[vKey].GetSendMessage():
                    sendWhatsApps(dictSensors[vKey].GetMobiles(), dictSensors[vKey].GetMessage())
                    dictSensors[vKey].SetSendMessage(False)
                    sH_Log.Add(dictSensors[vKey].GetSensor() + dictSensors[vKey].GetMessage())
                elif dictSensors[vKey].GetSendMessage() == False:
                    dictSensors[vKey].SetSendMessage(True)
                
                # Delta
                vBoolDelta = dictSensors[vKey].GetDelta()
                counterDelta = dictSensors[vKey].GetDeltaCounter()
                # print str(vKey) + '# delta' + str(vBoolDelta) + '#' + str(counterDelta) + '##'+str(dictSensors[vKey].GetTriggerCount())+'#' + str(dictSensors[vKey].GetDeltaMessage())
                if vBoolDelta and dictSensors[vKey].GetDeltaCounter() == 0:
                    dictSensors[vKey].SetDeltaCounter(counterDelta + 1)
                elif counterDelta > 0:
                    if counterDelta > dictSensors[vKey].GetTriggerCount():
                        sendWhatsApps(dictSensors[vKey].GetMobiles(), dictSensors[vKey].GetDeltaMessage())
                        sH_Log.Add(dictSensors[vKey].GetDeltaMessage())
                        dictSensors[vKey].SetDeltaCounter(0)
                    else:
                        dictSensors[vKey].SetDeltaCounter(counterDelta + 1)

        if counterHigh == TriggerCountA and RelaisStarted == False and vBoolTimeToCount and RelaisActive:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(True)

            # RelayIN1.on()
            # RelayIN2.on()
            LedR.on()
            LedY.off()
            RelaisStarted = True
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Started"))
            sH_Log.Add('Radiator activated')
        elif counterLow == TriggerCountB and RelaisStarted and vBoolTimeToCount and RelaisActive:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)
            # RelayIN1.off()
            # RelayIN2.off()
            LedR.off()
            LedY.off()
            RelaisStarted = False
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Stopped"))
            sH_Log.Add('Radiator deactivated')
        elif (vBoolTimeToCount == False or RelaisActive == False) and RelaisStarted:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)
            # RelayIN1.off()
            # RelayIN2.off()
            RelaisStarted = False
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Stopped"))
            sH_Log.Add('Radiator deactivated')

        # Vorzeitiges beenden    
        # elif counterLow == TriggerCountB and RelaisStarted == False:
            # timeDuration = MAXTIME + 1
        if vVerbose == 'test':
            print getInfoText("Status")

# # Write data to SQL Database see inmonitor        
#         for vKey in dictSensors:
#             conn = mysql.connector.connect(host='localhost', database='inmonitor',user='pi', password='raspberry')
#             cursor = conn.cursor()
#             try:
#                 dictSQL = {}
#                 dictSQL['device']        = vKey #DEVICE_ID
#                 dictSQL['timestamp']     = now
#                 dictSQL['password']      = PASSWORD
#                 dictSQL['name']          = dictSensors[vKey].GetSensor()
#                 dictSQL['time']          = dictSensors[vKey].GetTime()
#                 dictSQL['temperature']   = dictSensors[vKey].GetT()
#                 dictSQL['pressure']      = dictSensors[vKey].GetPA()
#                 dictSQL['humidity']      = dictSensors[vKey].GetRH()
#                 dictSQL['illuminance']   = 0
#                 dictSQL['relais']        = str(RelayIN1.isOn)+str(RelayIN2.isOn)
#                 dictSQL['led']           = str(LedG.isOn)+str(LedY.isOn)+str(LedR.isOn)
#                 dictSQL['localaddr']     = ip
# 
#                 query_update_devices = """ UPDATE devices SET private_ip = %s, last_ip = %s, last_conn = %s where id = %s and password = MD5( %s ) """
#                 args_devices = (dictSQL['localaddr'], dictSQL['localaddr'], str(dictSQL['timestamp']), str(dictSQL['device']), dictSQL['password'])
# 
#                 query_insert_data = "INSERT INTO data (device_id, timestamp, name, time, temperature, humidity, pressure, illuminance, relais, led) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#                 args_data = (str(dictSQL['device']), str(dictSQL['timestamp']), str(dictSQL['name']), str(dictSQL['time']), str(dictSQL['temperature']), str(dictSQL['humidity']), str(dictSQL['pressure']), str(dictSQL['illuminance']), str(dictSQL['relais']), str(dictSQL['led']))
# 
#                 cursor.execute(query_update_devices, args_devices)
#                 cursor.execute(query_insert_data, args_data)
#            
#                 #if cursor.lastrowid:
#                 #    print('last insert id', cursor.lastrowid)
#                 #else:
#                 #    print('last insert id not found')
#                 conn.commit()
#  
#             except mysql.connector.Error as error:
#                 print(error)
#  
#             finally:
#                 cursor.close()
#                 conn.close()


        refreshTime = time.time() + INTERVAL;
        time.sleep(0.1)

if RelaisStarted:
    dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)
    # RelayIN1.off()
    # RelayIN2.off()
    LedY.off()
    LedR.off()

sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Inactive - going down"))
LedG.off()
if vVerbose <> "test":
    os.system("sudo init 0")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
