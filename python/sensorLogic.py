#!/usr/bin/python
# -*- coding: latin-1 -*-

# include libraries -----------------------------------------------------------

import time, datetime  # time functions
import requests  # library for sending data over http
import thread  # loop is slow, needed for fast led pulse
import gpio  # led output
import os, sys, ast
from whatsapp import sendWhatsApps
import ConfigParser
from sensorHistory import sensorHistory
from sensorCrypt import sensorCrypt
from time import sleep
from plottest import plotting #ok
from sensorLight import sensorLight #ok
from sensorInterval import sensorInterval #ok
from sensorConfig import sensorConfig #ok
#from sensorThreads import threadFritzActors
from sensorThreads import threadFritzActors2 #ok
from sensorThreads import threadCreatePHPFile #ok
from sensorSwitches import sensorSwitches
import Queue

vVerbose = str(sys.argv[1])
if vVerbose.startswith('test'):
    print 'sensorService starting'
sConfig = sensorConfig('/home/pi/sensorTool/sensorTool.conf', vVerbose)
sensorSwitches('/home/pi/sensorTool/switches.conf', vVerbose);

# GPIO Settings BCM Layout
RelayIN1 = gpio.GPIOout(sConfig.getGPIORelayIN1())
RelayIN2 = gpio.GPIOout(sConfig.getGPIORelayIN2())
LedG = gpio.GPIOout(sConfig.getGPIOLedGreen())
LedY = gpio.GPIOout(sConfig.getGPIOLedYellow())
LedR = gpio.GPIOout(sConfig.getGPIOLedRed())
BMelder = gpio.GPIOin(sConfig.getGPIOmotion())
Leuchte = sensorLight(sConfig.getGPIOlight())

# Start state
LedG.on()
LedY.on()
LedR.on()
boolLeuchte = False

# constants -------------------------------------------------------------------
sCrypt = sensorCrypt(sConfig.getCryptKey())
INTERVAL_1 = sConfig.getIntervalSensors()
MAXTIME = sConfig.getMaxTime() 
MINTIME = sConfig.getMinTime() 
INTERVAL_2 = sConfig.getIntervalActors()
SERVER = sConfig.getServer()

TriggerCountA = sConfig.getTriggerCountA()
TriggerCountB = sConfig.getTriggerCountB()

#dictInterval = {}
dictInterval = sensorInterval(sConfig.getDictIntervalle())

vTitel = sConfig.getTitel()

dictActors = {}    
dictSensors = {}
dictSensors = sConfig.getDictSensors()
iControlSensor = sConfig.getiControlSensor()
sH_Log = sensorHistory('/var/sensorTool/www/loglatestentry.php', '/var/sensorTool/www/logdata.php')
iLog = 0

# Config Variable leeren
sConfig = None

vBoolLC = True
RelaisStarted = False
RelaisActive = True
# fritz off moved after first fritzactors call

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
    if vVerbose.startswith('test'):
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
    vhttpResult += 'echo "<DIV class=\\"sensor\\"><TABLE class=\\"sensor\\"><TR>\\n";\n'
    vhttpResult += 'echo "<TD>\\n";\n'
    for vKey in dictSensors:
        vhttpResult += dictSensors[vKey].GetHttpTable()
        
    vhttpResult += 'echo "</TD>\\n";\n'
    vhttpResult += 'echo "<TD>\\n";\n'
    vhttpResult += 'echo "<DIV class=\\"sensor\\"><TABLE class=\\"sensor\\"><TR>\\n";\n'
    vhttpResult += 'echo "<TD class=\\"sensorlabel\\"><strong>GPIO</strong></TD>\\n";\n'
    vhttpResult += 'echo "<TD class=\\"sensor\\">RELAIS</TD>\\n";\n'
    vhttpResult += 'echo "<TD class=\\"sensor\\">LED</TD>\\n";\n'
    vhttpResult += 'echo "</TR><TR>\\n";\n'
    vhttpResult += 'echo "<TD class=\\"sensor\\">' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[11:19] + '</TD>\\n";\n'
    vhttpResult += 'echo "<TD class=\\"sensor\\">' + str(RelayIN1.isOn) + str(RelayIN2.isOn) + '</TD>\\n";\n'
    vhttpResult += 'echo "<TD class=\\"sensor\\">' + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn) + '</TD>\\n";\n'
    vhttpResult += 'echo "</TR></TABLE></DIV>\\n";\n'
    vhttpResult += 'echo "<BR \><BR \>\\n";\n'
    for vAKey in dictActors:
        vhttpResult += dictActors[vAKey].GetHttpTable()
        
    vhttpResult += 'echo "</TD></TR></TABLE></DIV>\\n";\n'
    return vhttpResult

# refresh for sensor data
refreshTime1 = time.time() + INTERVAL_1
# refresh for fritz actors
refreshTime2 = time.time()
# refresh for Queue
# INTERVAL_3 = 10
# if vVerbose.startswith('test'):
#     INTERVAL_3 = 3   
# refreshTime3 = time.time() + INTERVAL_3
# FAInProgress = False
# qFA = Queue.LifoQueue(maxsize=1)

# loop ------------------------------------------------------------------------
LedR.off()
if vVerbose.startswith('test1'):
    print 'Config loaded'
    print str(refreshTime1) + '##' + str(time.time())
    
while time.strftime('%H%M') < MAXTIME:  # timeDuration <= MAXTIME: 
    # Check NDD Queue every INTERVAL_3 secs
#     if time.time() > refreshTime3:
#         if FAInProgress:
#             if not qFA.empty():
#                 dictActors = qFA.get()
#                 qFA.task_done()
#                 FAInProgress = False
#             
#         refreshTime3 = time.time() + INTERVAL_3

    # get fritz actor data
    if time.time() > refreshTime2:
        dictActors = threadFritzActors2()
#         if not FAInProgress:
#             if vVerbose.startswith('test'):
#                 print 'Start Fritz Actor Discovery!'
#                 
#             thread.start_new_thread(threadFritzActors,  (qFA, ) )
#             FAInProgress = True
#         else:
#             if vVerbose.startswith('test'):
#                 print 'Fritz Actor Discovery running'
                
        # On Startup stop running radiators
        if vBoolLC:# and not FAInProgress:
            dictActors[str(dictSensors[iControlSensor].GetFritzActor())].SetActor(False)
 
        refreshTime2 = time.time() + INTERVAL_2

    # every refreshtime  seconds,  get data from SensorService
    if time.time() > refreshTime1:
        if vVerbose.startswith('test1'):
            print str(refreshTime1) + '##' + str(time.time())
        # Werte holen per http request ::D
        try:
            # print 'Get HTTP Service'
            r = requests.get("http://" + SERVER + ":6666")
            # request enthaelt "
            # print r
            vR = sCrypt.Decrypt(r.text[1:len(r.text) - 1])
            # print vR
            dictResponse = {}
            dictResponse = ast.literal_eval(str(vR))
            #print dictResponse
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
        
        except Exception as e:
            print e 
            # pass

        # ############### Dynamic Config  Start ###################
        # Dynamische Config einlesen #soll ueber http request gesteuert werden.
        dynamicConf = ConfigParser.ConfigParser()
        dynamicConf.read('/var/sensorTool/www/dynamic.conf')
        # Try to change the Relais Status 
        try:
            # print relaisStat.getboolean('relais', 'relais_active')
            # print RelaisActive
            if dynamicConf.getboolean('relais', 'relais_active') != RelaisActive:
                RelaisActive = dynamicConf.getboolean('relais', 'relais_active')
                #print ' RelaisActive set to ' + str(RelaisActive)
                sH_Log.Add(' RelaisActive set to ' + str(RelaisActive))

        except: 
            pass
            
        # iterate through sensor data
        for vKey in dictSensors:
            try:
                vSetHighRH = False
                if dictSensors[vKey].GetThresholdHighHumidity() == False:
                    vSetHighRH = True
                elif dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_high_humidity') != dictSensors[vKey].GetThresholdHighHumidity():
                    vSetHighRH = True
                    
                if vSetHighRH:
                    dictSensors[vKey].SetThresholdHighHumidity(dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_high_humidity'))
                    sH_Log.Add('Threshold High RH S' + str(vKey) + ':' + str(dictSensors[vKey].GetThresholdHighHumidity()))
                    if vVerbose.startswith('test'):
                        print 'Threshold High RH S' + str(vKey) + ':' + str(dictSensors[vKey].GetThresholdHighHumidity())
                        
            except: 
                pass  # Exception, e:

            try:
                vSetLowT = False
                if dictSensors[vKey].GetThresholdLowTemperature() == False:
                    vSetLowT = True
                elif dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_low_temperature') != dictSensors[vKey].GetThresholdLowTemperature():
                    vSetLowT = True
                    
                if vSetHighRH:
                    dictSensors[vKey].SetThresholdLowTemperature(dynamicConf.getfloat('Sensor' + str(vKey), 'threshold_low_temperature'))
                    sH_Log.Add('Threshold Low T S' + str(vKey) + ':' + str(dictSensors[vKey].GetThresholdLowTemperature()))
                    if vVerbose == 'test':
                        print 'Threshold Low T S' + str(vKey) + ':' + str(dictSensors[vKey].GetThresholdLowTemperature())
                        
            except: 
                pass  # Exception, e:
                
        # ############### Dynamic Config  Ende ###################
        
        if vBoolLC == True:
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Active"))
            sH_Log.Add('sensorTool started')
            LedY.off()
            vBoolLC = False

        # ############### Check for Radiator interval  start ##################
        vBoolInterval = dictInterval.isNowInInterval()
        # ############### Check for Radiator interval  Ende ##################

        if vVerbose.startswith('test1'):
            print( 'Threshold: ' + str(dictSensors[iControlSensor].GetThreshold()) + ' RelaisStarted: ' + str(RelaisStarted) + ' vBoolInterval: ' + str(vBoolInterval) +' RelaisActive: ' + str(RelaisActive))
            
        if dictSensors[iControlSensor].GetThreshold() and RelaisStarted == False and vBoolInterval and RelaisActive:
            counterHigh = counterHigh + 1
            if LedY.isOn == False:
                LedY.on()
                sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (H)!')
        else:
            counterHigh = 0
            
        if dictSensors[iControlSensor].GetThreshold() == False and RelaisStarted and vBoolInterval and RelaisActive:
            counterLow = counterLow + 1
            if LedY.isOn == False:
                LedY.on()
                sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (L)!')
        else:
            counterLow = 0

        if vVerbose.startswith('test1'):
            print( 'counterLow: ' + str(counterLow) + ' counterHigh: ' + str(counterHigh) )
        
        boolInfoLight = False
        # Alle anderen Sensoren (außer Keller) durchgehen
        for vKey in dictSensors:
            # if dictSensors[vKey].GetBME() != True: 
            if iControlSensor <> vKey:
                vBoolThreshold = dictSensors[vKey].GetThreshold()

                # Grenzwert
                if vBoolThreshold and dictSensors[vKey].GetSendMessage():
                    sendWhatsApps(dictSensors[vKey].GetMobiles(), dictSensors[vKey].GetMessage())
                    dictSensors[vKey].SetSendMessage(False)
                    sH_Log.Add(dictSensors[vKey].GetSensor() + dictSensors[vKey].GetMessage())
                    boolInfoLight = True
                elif dictSensors[vKey].GetSendMessage() == False:
                    dictSensors[vKey].SetSendMessage(True)

                # Delta
                vBoolDelta = dictSensors[vKey].GetDelta()
                counterDelta = dictSensors[vKey].GetDeltaCounter()
                if vBoolDelta and dictSensors[vKey].GetDeltaCounter() == 0:
                    dictSensors[vKey].SetDeltaCounter(counterDelta + 1)
                elif counterDelta > 0:
                    if counterDelta > dictSensors[vKey].GetTriggerCount():
                        sendWhatsApps(dictSensors[vKey].GetMobiles(), dictSensors[vKey].GetDeltaMessage())
                        sH_Log.Add(dictSensors[vKey].GetDeltaMessage())
                        dictSensors[vKey].SetDeltaCounter(0)
                        boolInfoLight = True
                    else:
                        dictSensors[vKey].SetDeltaCounter(counterDelta + 1)
                        
        if boolInfoLight:
            if not boolLeuchte:
                boolLeuchte = Leuchte.activate(boolLeuchte)
        else:
            if boolLeuchte:
                boolLeuchte = Leuchte.deactivate(boolLeuchte)
                
        if counterHigh == TriggerCountA and RelaisStarted == False and vBoolInterval and RelaisActive:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(True)
            LedR.on()
            LedY.off()
            RelaisStarted = True
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Started"))
            sH_Log.Add('Radiator activated')
        elif (counterLow == TriggerCountB or vBoolInterval == False or RelaisActive == False) and RelaisStarted:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)
            LedR.off()
            LedY.off()
            RelaisStarted = False
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Stopped"))
            sH_Log.Add('Radiator deactivated')
            
        if vVerbose.startswith('test'):
            print getInfoText("Status")

        dictPlotSens = {}
        dictPlotAussen = {}
        for vKey in dictSensors:
            dictPlotS = {}
            ListT = []
            ListRH = []
            ListTime = []
            sName = dictSensors[vKey].GetSensor()
            dictPlotS['ListTime'] = dictSensors[vKey].GetListTime()
            dictPlotS['ListT'] = dictSensors[vKey].GetListT()
            dictPlotS['ListRH'] = dictSensors[vKey].GetListRH()
            dictPlotSens[sName] = dictPlotS
 
        plotting(dictPlotSens, dictPlotAussen, vVerbose)
#        thread.start_new_thread(plotting, (dictPlotSens, dictPlotAussen, vVerbose,))
          
        threadCreatePHPFile('/var/sensorTool/www/sensor.php', getHTML())
#        thread.start_new_thread(threadCreatePHPFile, ('/var/sensorTool/www/sensor.php', getHTML(),))
        
        refreshTime1 = time.time() + INTERVAL_1
    sleep(1) # 0.1

if RelaisStarted:
    dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)

sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Inactive - going down"))
if vVerbose.startswith('test'):
    print 'GPIO Down'
LedY.off()
LedR.off()
LedG.off()
if boolLeuchte:
    Leuchte.deactivate(boolLeuchte)

if not vVerbose.startswith('test'):
    os.system("sudo init 0")
else:
    print ' - Ende - '

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
