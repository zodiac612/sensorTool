#!/usr/bin/python
# -*- coding: latin-1 -*-

# include libraries -----------------------------------------------------------

import time, datetime # time functions
import requests # library for sending data over http
import socket # to find out our local ip
import thread # loop is slow, needed for fast led pulse

import bme280#, tsl2591 # libraries for our sensors
import gpio # led output
import httpservice # for rt service
import os, sys, ast
from whatsapp import sendWhatsApps
import ConfigParser
from tx35dth import tx35dth
import mysql.connector #import MySQLConnection, Error

config = ConfigParser.ConfigParser()
config.read('/home/pi/sensorTool/sensorTool.conf')
print config.sections()

# constants -------------------------------------------------------------------

INTERVAL       = config.getint('inmonitor', 'data_save_interval')
MAXTIME        = config.get('global', 'maxtime') 
MINTIME        = config.get('global', 'mintime') 

vVerbose       = str(sys.argv[1])
if vVerbose == "test":
    INTERVAL   = config.getint('test', 'test_data_save_interval')
    MAXTIME    = config.get('test', 'test_maxtime')

TriggerCountA  = config.getint('inmonitor', 'trigger_start_count')
TriggerCountB  = config.getint('inmonitor', 'trigger_end_count')
SERVER         = config.get('db', 'server')
PASSWORD       = config.get('db', 'password')
HTTP_TIMEOUT   = config.getint('db', 'http_timeout')
#lacrosseFile   = config.get('lacrosse', 'logfile')
#bme280log      = config.get('inmonitor', 'bme280log')
#ftpCopyScript  = config.get('inmonitor', 'ftpCopyScript')
#mobile1        = config.get('inmonitor', 'mobile1')
#mobile2        = config.get('inmonitor', 'mobile2') 
dictIntervalle = {}
iIntervall = 1
while iIntervall < 100:
    try:
        dictIntervall = {}
        dictIntervall['start'] = config.get('inmonitor', 'intervalstart_' + str(iIntervall))
        dictIntervall['stop']  = config.get('inmonitor', 'intervalstop_' + str(iIntervall))
        #print dictIntervall
        dictIntervalle[iIntervall] = dictIntervall
        iIntervall = iIntervall + 1
    except: iIntervall = 100
#print dictIntervalle

# i1start        = config.get('inmonitor', 'interval1start')
# i1stop         = config.get('inmonitor', 'interval1stop')
# i2start        = config.get('inmonitor', 'interval2start')
# i2stop         = config.get('inmonitor', 'interval2stop')
# i3start        = config.get('inmonitor', 'interval3start')
# i3stop         = config.get('inmonitor', 'interval3stop')
vTitel         = config.get('inmonitor', 'titel')
CountOfSensors = config.getint('inmonitor', 'count_of_sensors')
#hRel1          = config.getfloat('inmonitor', 'humidity_sensor3')
#Sensor1T       = config.getfloat('inmonitor', 'temperature_sensor1')
#Sensor1RH      = config.getfloat('inmonitor', 'humidity_sensor1')
#Sensor1Trigger = config.getint('inmonitor', 'trigger_count_sensor1')
#vSen1Message   = config.get('inmonitor', 'message_sensor1')
#alertDeltaT    = config.getfloat('inmonitor', 'alert_temp_delta')
#alertDeltaRH   = config.getfloat('inmonitor', 'alert_humi_delta')

dictSensors    = {}
if CountOfSensors > 0:
    iSensor = 0
    while iSensor < CountOfSensors:
        dictSensor = {}
        try:    dictSensor['bme280']                = config.getboolean('Sensor'+str(iSensor), 'bme280')
        except: dictSensor['bme280']                = False
        try:    dictSensor['hex']                   = config.get('Sensor'+str(iSensor), 'hex')
        except:
            if dictSensor['bme280']:
                dictSensor['hex']                   = 'bme280'
            else:
                dictSensor['hex']                   = 'none'   
                     
        try:    dictSensor['name']                  = config.get('Sensor'+str(iSensor), 'name')
        except: dictSensor['name']                  = 'unkown'
        try:    dictSensor['message']               = config.get('Sensor'+str(iSensor), 'message')
        except: dictSensor['message']               = 'no message defined'
        try:    dictSensor['delta_message']          = config.get('Sensor'+str(iSensor), 'delta_message')
        except: dictSensor['delta_message']          = 'no delta message defined'
        try:    dictSensor['delta_humidity']         = config.getfloat('Sensor'+str(iSensor), 'delta_humidity')
        except: pass
        try:    dictSensor['delta_temperature']      = config.getfloat('Sensor'+str(iSensor), 'delta_temperature')
        except: pass
        try:    dictSensor['threshold_low_humidity']     = config.getfloat('Sensor'+str(iSensor), 'threshold_low_humidity')
        except: pass
        try:    dictSensor['threshold_low_temperature']  = config.getfloat('Sensor'+str(iSensor), 'threshold_low_temperature')
        except: pass
        try:    dictSensor['threshold_high_humidity']    = config.getfloat('Sensor'+str(iSensor), 'threshold_high_humidity')
        except: pass
        try:    dictSensor['threshold_high_temperature'] = config.getfloat('Sensor'+str(iSensor), 'threshold_high_temperature')
        except: pass
        try:    dictSensor['trigger_count']         = config.getint('Sensor'+str(iSensor), 'trigger_count')
        except: dictSensor['trigger_count']         = 0
        iMobile = 1
        dictMobile = {}
        while iMobile < 100:
            try:    
                dictMobile[iMobile]                 = config.get('Sensor'+str(iSensor), 'mobile' + str(iMobile))
                iMobile = iMobile + 1
            except: iMobile = 100
        dictSensor['mobiles']                       = dictMobile
        if dictSensor['hex'] <> 'none':
            dictSensors[iSensor] = tx35dth(dictSensor)
        iSensor = iSensor + 1
    #While iSensor < CountOfSensors:

RelayIN1       = gpio.GPIOout(12)
RelayIN2       = gpio.GPIOout(16)
LedG           = gpio.GPIOout(36)
LedY           = gpio.GPIOout(40)
LedR           = gpio.GPIOout(38)
vBoolLC        = True
RelaisStarted  = False
RelaisActive   = True
RelayIN1.off()
RelayIN2.off()
LedG.off()
LedY.off()
LedR.off()

degC         = 0
hPa          = 0
hRel         = 0
degC1        = 0
hPa1         = 0
vBoolSensor1 = True
counterHigh  = 0
counterLow   = 0
timeDuration = 0

# functions for print out and WhatsApp
def getInfoText(vStatus): #, degC, hPa, hRel, vBad, vWozi, vKeller, vAussen):
    #(degC, hPa, hRel) = bme280.readData()
    #(vBad, vWozi, vKeller, vAussen) = test.readdata('b8', 'c4', 'b0', 'ec')
    vHeader = vTitel
    if vVerbose == "test":
        vHeader = vHeader + ' Test\n'
    else:
        vHeader = vHeader + '\n'
    
    vNow=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' + vStatus
    vSensorPaket = ''
    for vKey in dictSensors:
        vSensorPaket = vSensorPaket + '\n '+str(dictSensors[vKey].GetInfo(False, False))
    
    vGPIOStatus = ''
    vGPIOStatus = vGPIOStatus + '\n Relais: '+str(RelaisStarted)+' ('+str(RelayIN1.isOn)+'|'+str(RelayIN2.isOn)+')'
    vGPIOStatus = vGPIOStatus + '\n Code:   '+str(timeDuration)+';'+str(counterHigh)+';'+str(counterLow)
    vGPIOStatus = vGPIOStatus + '\n LED:    '+str(LedG.isOn)+str(LedY.isOn)+str(LedR.isOn)
        
    vReturnText = vHeader + vNow + vSensorPaket + vGPIOStatus
    return vReturnText

def getInfoCSV(): #degC, hPa, hRel, vBad, vWozi, vKeller, vAussen):
    #(degC, hPa, hRel) = bme280.readData()
    #(vBad, vWozi, vKeller, vAussen) = test.readdata('b8', 'c4', 'b0', 'ec')
    vReturnText = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ';'
    vReturnText = vReturnText + str(RelaisStarted) + ';'
    vReturnText = vReturnText + str(timeDuration)+';'+str(counterHigh)+';'+str(counterLow) + ";"
    vReturnText = vReturnText + str(RelayIN1.isOn)+str(RelayIN2.isOn)+";"
    vReturnText = vReturnText + str(LedG.isOn)+str(LedY.isOn)+str(LedR.isOn) + ";"
    
    for vKey in dictSensors:
        vReturnText = vReturnText + str(dictSensors[vKey].GetInfo(True, False))
    return vReturnText

def getHTML():
    vhttpResult  = ''
    vhttpResult += '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
    vhttpResult += '<html xmlns="http://www.w3.org/1999/xhtml">'
    vhttpResult += '<head>'
    vhttpResult += '<title>Raspberry PI Status</title>'
    vhttpResult += '<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-15" />'
    vhttpResult += '</head>'
    vhttpResult += '<body bgcolor="#CCCCCC">'
    vhttpResult += '<h3>Raspberry PI SensorTool Status<BR />'+datetime.datetime.now().strftime('%Y-%m-%d')+'</h3>'
    for vKey in dictSensors:
        vhttpResult += dictSensors[vKey].GetHttpTable()
        vhttpResult += '<BR />'
    vhttpResult += '<DIV MARGIN="5"><TABLE BORDER=1><TR>'
    vhttpResult += '<TD><strong>GPIO</strong></TD>'
    vhttpResult += '<TD>RELAIS</TD>'
    vhttpResult += '<TD>LED</TD>'
    vhttpResult += '</TR><TR>'
    vhttpResult += '<TD>'+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[11:16]+'</TD>'
    vhttpResult += '<TD>'+str(RelayIN1.isOn)+str(RelayIN2.isOn)+'</TD>'
    vhttpResult += '<TD>'+str(LedG.isOn)+str(LedY.isOn)+str(LedR.isOn)+'</TD>'
    vhttpResult += '</TR></TABLE></DIV>' 
    vhttpResult += '</body>'
    vhttpResult += '</html>'
    return vhttpResult

# find out private ip address -------------------------------------------------
ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
#print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "My private IP is:", ip

# init  -----------------------------------------------------------------------

httpd = httpservice.Service(2222)
httpd1 = httpservice.Service(8086)
#led = gpio.GPIOout(26)
refreshTime = time.time() + INTERVAL;

# loop ------------------------------------------------------------------------

#LedG.on()

#vlogsize = os.system("ls -l /home/pi/inmonitor/python/log/ | grep bme280.log | awk '{print $5}'")
#if time.strftime('%H%M') < MINTIME:
#    fileHandle = open (bme280log, 'w')
#    fileHandle.write ( 'time;temperatur;druck;feuchtigkeit;RelaisStatus;timeDuration;High;Low;RelaisGPIO;LedGPIO;BadT;BadRH;WoziT;WoziRH;KellerT;KellerRH;AussenT;AussenRH;s1tt;s2tt;s3tt;s4tt;\n' )
#    fileHandle.close()

while time.strftime('%H%M') < MAXTIME: #timeDuration <= MAXTIME: 
    # read temperature, pressure, humidity

    lux = 0
    dictHTTPD = {}
    dictHTTPD['timestamp']   = 'ALMOST REAL TIME!'
    dictHTTPD['temperature'] = dictSensors[0].GetT()
    dictHTTPD['humidity']    = dictSensors[0].GetRH()
    dictHTTPD['pressure']    = dictSensors[0].GetPA()
    dictHTTPD['illuminance'] = lux
    dictHTTPD['S1T']         = dictSensors[1].GetT()
    dictHTTPD['S1RH']        = dictSensors[1].GetRH()
    dictHTTPD['S2T']         = dictSensors[2].GetT()
    dictHTTPD['S2RH']        = dictSensors[2].GetRH()
    dictHTTPD['S3T']         = dictSensors[3].GetT()
    dictHTTPD['S3RH']        = dictSensors[3].GetRH()
    dictHTTPD['S4T']         = dictSensors[4].GetT()
    dictHTTPD['S4RH']        = dictSensors[4].GetRH()
    
    vhttpResult = getHTML()
    
    if httpd1.provideData(vhttpResult):
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpd1.addr[0]

    if httpd.provideData(dictHTTPD):
        print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "direct request from", httpd.addr[0]
    
    # every 10 seconds, try to send data to servers
    if time.time() > refreshTime:
        
        #Werte holen per http request ::D
        try:
            r=requests.get( "http://"+SERVER+":6666")
            vR = r.text
            dictResponse = {}
            dictResponse = ast.literal_eval(str(vR))
            for vSensor in dictResponse:
                dictTemp = {}
                dictTemp['ID'] = vSensor
                if 'Time' in dictResponse[vSensor]:
                    dictTemp['Time'] = dictResponse[vSensor]['Time']
                if 'RH' in dictResponse[vSensor]:
                    dictTemp['RH']   = dictResponse[vSensor]['RH']
                if 'T' in dictResponse[vSensor]:
                    dictTemp['T']    = dictResponse[vSensor]['T']
                if 'hPa' in dictResponse[vSensor]:    
                    dictTemp['hPa']  = dictResponse[vSensor]['hPa']
                boolBME280 = False
                if (vSensor == 'bme280') :
                    boolBME280 = True
             
                for vKey in dictSensors:
                    if dictSensors[vKey].GetHex() == vSensor:
                        dictSensors[vKey].SetSensorData(dictTemp, boolBME280)
        except: 
            pass
        
        # Dynamische Config einlesen
        relaisStat = ConfigParser.ConfigParser()
        relaisStat.read('/home/pi/inmonitor/www/RelaisStat.cfg')
        print relaisStat.sections()
        
        # Versuche das Relais Status zu aendern 
        try:
            #print relaisStat.getboolean('relais', 'relais_active')
            #print RelaisActive
            if relaisStat.getboolean('relais', 'relais_active') != RelaisActive:
                RelaisActive = relaisStat.getboolean('relais', 'relais_active')
                print ' RelaisActive set to '+ str(RelaisActive)
        except: pass
        
        for vKey in dictSensors:
            #print relaisStat.getfloat('Sensor' + str(vKey), 'threshold_high_humidity')
            #print dictSensors[vKey].GetThresholdHighHumidity()
            try:
                #print relaisStat.getfloat('Sensor' + str(vKey), 'threshold_high_humidity')
                #print dictSensors[vKey].GetThresholdHighHumidity()
                
                vSetHighRH = False
                if dictSensors[vKey].GetThresholdHighHumidity() == False:
                    vSetHighRH = True
                elif relaisStat.getfloat('Sensor' + str(vKey), 'threshold_high_humidity') != dictSensors[vKey].GetThresholdHighHumidity():
                    vSetHighRH = True
                
                if vSetHighRH:
                    dictSensors[vKey].SetThresholdHighHumidity(relaisStat.getfloat('Sensor' + str(vKey), 'threshold_high_humidity'))
                    print 'Threshold High RH S0:' + str(dictSensors[vKey].GetThresholdHighHumidity())
                    
            except: pass
        
        timeDuration = timeDuration + INTERVAL
        #print str(timeDuration) + '#' + str(INTERVAL)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        refreshTime = time.time() + INTERVAL;
            
        if vBoolLC == True:
            sendWhatsApps(dictSensors[0].GetMobiles(), getInfoText("Active"))
            vBoolLC = False
        
        vStunde = time.strftime('%H%M')
        vBoolTimeToCount = False
        for vIv in dictIntervalle:
            #print vStunde + '>' + dictIntervalle[vIv]['start'] + ' and ' + vStunde + ' < ' + dictIntervalle[vIv]['stop']
            if vStunde > dictIntervalle[vIv]['start'] and vStunde < dictIntervalle[vIv]['stop'] and datetime.date.today().weekday() != 6:
                vBoolTimeToCount = True
                
        #print 'dictSensors[0].GetThreshold(): ' + str(dictSensors[0].GetThreshold())
        #print 'dictSensors[0].GetRH(): ' + str(dictSensors[0].GetRH())
        #print 'RelaisStarted: ' + str(RelaisStarted)
        #print 'vBoolTimeToCount ' + str(vBoolTimeToCount)
        #print 'RelaisActive: ' + str(RelaisActive)
        if dictSensors[0].GetThreshold() and RelaisStarted == False and vBoolTimeToCount and RelaisActive:
            counterHigh = counterHigh + 1
            #LedY.on()
        else:
            counterHigh = 0
            
        if dictSensors[0].GetThreshold() == False and RelaisStarted and vBoolTimeToCount and RelaisActive:
            counterLow = counterLow + 1
            #LedY.on()
        else:
            counterLow = 0
                
        for vKey in dictSensors:
            if dictSensors[vKey].GetBME() != True:
                vBoolThreshold = dictSensors[vKey].GetThreshold()
                #print str(vKey) + '# threshold ' + str(vBoolThreshold) + '#' +  str(dictSensors[vKey].GetSendMessage())
                
                # Grenzwert
                if vBoolThreshold and dictSensors[vKey].GetSendMessage():
                    sendWhatsApps(dictSensors[vKey].GetMobiles(), dictSensors[vKey].GetMessage())
                    dictSensors[vKey].SetSendMessage(False)
                elif dictSensors[vKey].GetSendMessage() == False:
                    dictSensors[vKey].SetSendMessage(True)
                
                # Delta
                vBoolDelta = dictSensors[vKey].GetDelta()
                counterDelta = dictSensors[vKey].GetDeltaCounter()
                #print str(vKey) + '# delta' + str(vBoolDelta) + '#' + str(counterDelta) + '##'+str(dictSensors[vKey].GetTriggerCount())+'#' + str(dictSensors[vKey].GetDeltaMessage())
                if vBoolDelta and dictSensors[vKey].GetDeltaCounter() == 0:
                    dictSensors[vKey].SetDeltaCounter(counterDelta + 1)
                elif counterDelta > 0:
                    if counterDelta > dictSensors[vKey].GetTriggerCount():
                        sendWhatsApps(dictSensors[vKey].GetMobiles(), dictSensors[vKey].GetDeltaMessage())
                        dictSensors[vKey].SetDeltaCounter(0)
                    else:
                        dictSensors[vKey].SetDeltaCounter(counterDelta + 1)

        if counterHigh == TriggerCountA and RelaisStarted == False and vBoolTimeToCount and RelaisActive:
            RelayIN1.on()
            RelayIN2.on()
            #LedR.on()
            #LedY.off()
            RelaisStarted = True
            sendWhatsApps(dictSensors[0].GetMobiles(), getInfoText("Started"))
        elif counterLow == TriggerCountB and RelaisStarted and vBoolTimeToCount and RelaisActive:
            RelayIN1.off()
            RelayIN2.off()
            #LedR.off()
            #LedY.off()
            RelaisStarted = False
            sendWhatsApps(dictSensors[0].GetMobiles(), getInfoText("Stopped"))
        elif (vBoolTimeToCount == False or RelaisActive == False) and RelaisStarted:
            RelayIN1.off()
            RelayIN2.off()
            RelaisStarted = False
            sendWhatsApps(dictSensors[0].GetMobiles(), getInfoText("Stopped"))

        #Vorzeitiges beenden    
        #elif counterLow == TriggerCountB and RelaisStarted == False:
            #timeDuration = MAXTIME + 1
        if vVerbose == 'test':
            print getInfoText("Status")
        #fileHandle = open (bme280log, 'a')
        #fileHandle.write ( getInfoCSV()+'\n' )
        #fileHandle.close()
        #os.system(ftpCopyScript)
        
        for vKey in dictSensors:
            conn = mysql.connector.connect(host='localhost', database='inmonitor',user='pi', password='raspberry')
            cursor = conn.cursor()
            try:
                dictSQL = {}
                dictSQL['device']        = vKey #DEVICE_ID
                dictSQL['timestamp']     = now
                dictSQL['password']      = PASSWORD
                dictSQL['name']          = dictSensors[vKey].GetSensor()
                dictSQL['time']          = dictSensors[vKey].GetTime()
                dictSQL['temperature']   = dictSensors[vKey].GetT()
                dictSQL['pressure']      = dictSensors[vKey].GetPA()
                dictSQL['humidity']      = dictSensors[vKey].GetRH()
                dictSQL['illuminance']   = 0
                dictSQL['relais']        = str(RelayIN1.isOn)+str(RelayIN2.isOn)
                dictSQL['led']           = str(LedG.isOn)+str(LedY.isOn)+str(LedR.isOn)
                dictSQL['localaddr']     = ip

                query_update_devices = """ UPDATE devices SET private_ip = %s, last_ip = %s, last_conn = %s where id = %s and password = MD5( %s ) """
                args_devices = (dictSQL['localaddr'], dictSQL['localaddr'], str(dictSQL['timestamp']), str(dictSQL['device']), dictSQL['password'])

                query_insert_data = "INSERT INTO data (device_id, timestamp, name, time, temperature, humidity, pressure, illuminance, relais, led) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                args_data = (str(dictSQL['device']), str(dictSQL['timestamp']), str(dictSQL['name']), str(dictSQL['time']), str(dictSQL['temperature']), str(dictSQL['humidity']), str(dictSQL['pressure']), str(dictSQL['illuminance']), str(dictSQL['relais']), str(dictSQL['led']))

                cursor.execute(query_update_devices, args_devices)
                cursor.execute(query_insert_data, args_data)
           
                #if cursor.lastrowid:
                #    print('last insert id', cursor.lastrowid)
                #else:
                #    print('last insert id not found')
                conn.commit()
 
            except mysql.connector.Error as error:
                print(error)
 
            finally:
                cursor.close()
                conn.close()
    
        time.sleep(0.1)

if RelaisStarted:
    RelayIN1.off()
    RelayIN2.off()
    LedY.off()
    LedR.off()

sendWhatsApps(dictSensors[0].GetMobiles(), getInfoText("Inactive - going down"))
LedG.off()
if vVerbose <> "test":
    os.system("sudo init 0")

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
