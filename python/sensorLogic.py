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
from sensorThreads import threadPICAM2
from sensorThreads import threadFritzActors2 #ok
from sensorThreads import threadNetDiscovery2 #ok
from sensorThreads import threadCreatePHPFile #ok
from sensorThreads import threadWebradioService
from sensorSwitches import sensorSwitches
from sensorDevice import sensorDevice
import Queue

vVerbose = str(sys.argv[1])
if vVerbose.startswith('test'):
    print 'sensorService starting'
sConfig = sensorConfig('/home/pi/sensorTool/sensorTool.conf', vVerbose)
sensorSwitches('/home/pi/sensorTool/switches.conf', vVerbose);

# GPIO Settings BCM Layout
#RelayIN1 = gpio.GPIOout(sConfig.getGPIORelayIN1())
#RelayIN2 = gpio.GPIOout(sConfig.getGPIORelayIN2())
#LedG = gpio.GPIOout(sConfig.getGPIOLedGreen())
#LedY = gpio.GPIOout(sConfig.getGPIOLedYellow())
#LedR = gpio.GPIOout(sConfig.getGPIOLedRed())
BMelder = gpio.GPIOin(sConfig.getGPIOmotion())
Leuchte = sensorLight(sConfig.getGPIOlight())

# Start state
#LedG.on()
#LedY.on()
#LedR.on()
boolLeuchte = False

# constants -------------------------------------------------------------------
sCrypt = sensorCrypt(sConfig.getCryptKey())
INTERVAL_1 = sConfig.getIntervalSensors()
MAXTIME = sConfig.getMaxTime() 
MINTIME = sConfig.getMinTime() 
INTERVAL_2 = sConfig.getIntervalActors()
SERVER = sConfig.getServer()
INTERVAL4Radio = 5

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

modules_webradio = sConfig.getModuleWebradio() # ok
webradio_active = False 
modules_surveillance = sConfig.getModuleSurveillance() # ok
modules_motiondetector = sConfig.getModuleMotiondetector() 
motion_detected = False
motion_detected_report = False
DeviceMotion=sensorDevice('Motiondetector')

modules_radiators = sConfig.getModuleRadiators() # ok
RadiatorStarted = False
DeviceRadiator=sensorDevice('Radiators')
modules_relais = sConfig.getModuleRelais()
modules_fritzactors = sConfig.getModuleFritzActors() # ok
modules_LANDevices = sConfig.getModuleLANDevices() # ok
LANDevices_Present = False
DeviceNetworkDetector=sensorDevice('NetworkDeviceDetector')

sConfig.SetupDynamicConfig('/var/sensorTool/www/dynamic.conf')

# Config Variable leeren
sConfig = None

vBoolLC = True
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
#    vGPIOStatus += '\n Relais: ' + str(RadiatorStarted) + ' (' + str(RelayIN1.isOn) + '|' + str(RelayIN2.isOn) + ')'
    vGPIOStatus += '\n Code:   ' + str(timeDuration) + ';' + str(counterHigh) + ';' + str(counterLow)
#    vGPIOStatus += '\n LED:    ' + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn)
    vReturnText = vHeader + vNow + vSensorPaket + vActorsPaket + vGPIOStatus  # + str(dictActors)
    return vReturnText

# print CSV
def getInfoCSV():
    vReturnText = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ';'
    vReturnText = vReturnText + str(RadiatorStarted) + ';'
    vReturnText = vReturnText + str(timeDuration) + ';' + str(counterHigh) + ';' + str(counterLow) + ";"
#    vReturnText = vReturnText + str(RelayIN1.isOn) + str(RelayIN2.isOn) + ";"
#    vReturnText = vReturnText + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn) + ";"
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
#    vhttpResult += 'echo "<DIV class=\\"sensor\\"><TABLE class=\\"sensor\\"><TR>\\n";\n'
#    vhttpResult += 'echo "<TD class=\\"sensorlabel\\"><strong>GPIO</strong></TD>\\n";\n'
#    vhttpResult += 'echo "<TD class=\\"sensor\\">RELAIS</TD>\\n";\n'
#    vhttpResult += 'echo "<TD class=\\"sensor\\">LED</TD>\\n";\n'
# #   vhttpResult += 'echo "</TR><TR>\\n";\n'
# #   vhttpResult += 'echo "<TD class=\\"sensor\\">' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[11:19] + '</TD>\\n";\n'
# #   vhttpResult += 'echo "<TD class=\\"sensor\\">' + str(RelayIN1.isOn) + str(RelayIN2.isOn) + '</TD>\\n";\n'
# #   vhttpResult += 'echo "<TD class=\\"sensor\\">' + str(LedG.isOn) + str(LedY.isOn) + str(LedR.isOn) + '</TD>\\n";\n'
#    vhttpResult += 'echo "</TR></TABLE></DIV>\\n";\n'
#    vhttpResult += 'echo "<BR \><BR \>\\n";\n'
 
    if modules_radiators:
        vhttpResult += DeviceRadiator.GetHttpTable()
        vhttpResult += 'echo "<BR \>\\n";\n'
    if modules_motiondetector:
        vhttpResult += DeviceMotion.GetHttpTable()
        vhttpResult += 'echo "<BR \>\\n";\n'
    if modules_LANDevices:
        vhttpResult += DeviceNetworkDetector.GetHttpTable()
        vhttpResult += 'echo "<BR \>\\n";\n'
 
    if modules_fritzactors:
        for vAKey in dictActors:
            vhttpResult += dictActors[vAKey].GetHttpTable()
        
    vhttpResult += 'echo "</TD></TR></TABLE></DIV>\\n";\n'
    return vhttpResult

# refresh for sensor data
refreshTime1 = time.time() + INTERVAL_1
# refresh for fritz actors
refreshTime2 = time.time()

refreshTime4Radio = time.time()
refreshTime5Bew = time.time()
# refresh for Queue
INTERVAL_3 = 10
# if vVerbose.startswith('test'):
#     INTERVAL_3 = 3   
refreshTime3 = time.time() + INTERVAL_3
# FAInProgress = False
# qFA = Queue.LifoQueue(maxsize=1)


# loop ------------------------------------------------------------------------
#LedR.off()
if vVerbose.startswith('test1'):
    print 'Config loaded'
    print str(refreshTime1) + '##' + str(time.time())
    
while time.strftime('%H%M') < MAXTIME:  # timeDuration <= MAXTIME: 
    # Check NDD Queue every INTERVAL_3 secs
    if time.time() > refreshTime5Bew:
        if modules_motiondetector:
            if BMelder.status() == 1:
                motion_detected = True
                motion_detected_report = True
            else:
                motion_detected = False
        
        if modules_surveillance and modules_motiondetector:
            if not LANDevices_Present:
                if motion_detected:
                    threadPICAM2('surveillance')
                    sH_Log.Add(' surveillance take picset ')
            else:
                threadPICAM2('low')
                sH_Log.Add(' surveillance take pic low ')
                
        refreshTime5Bew = time.time() + 1
        
    if time.time() > refreshTime3:
        if modules_LANDevices:
            LANDevices_Present = threadNetDiscovery2()
            sH_Log.Add(' LANDevices present ')
        refreshTime3 = time.time() + INTERVAL_3

    # get fritz actor data
    if time.time() > refreshTime2:
        if modules_fritzactors:
            dictActors = threadFritzActors2()
                
            # On Startup stop running radiators
            if vBoolLC:# and not FAInProgress:
                dictActors[str(dictSensors[iControlSensor].GetFritzActor())].SetActor(False)
        refreshTime2 = time.time() + INTERVAL_2
    
    # Check if there is a webradio setting change
    if time.time() > refreshTime4Radio:       
        if modules_webradio:
            (webradio_active1, webradio_changed, webradio_result) = threadWebradioService('/var/sensorTool/www/webradio.station', webradio_active)
            if webradio_changed:
                if webradio_active <> webradio_active1:
                    webradio_active = webradio_active1
                sH_Log.Add(' Webradio change: ' + str(webradio_result))       
        elif not modules_webradio and webradio_active:
            webradio_active = threadWebradioService('/var/sensorTool/www/webradio.station', webradio_active, True)
            sH_Log.Add(' Webradio stopped')
        refreshTime4Radio = time.time() + INTERVAL4Radio

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
        
            DeviceMotion.SetSensorData(motion_detected_report)
            motion_detected_report = False
            DeviceNetworkDetector.SetSensorData(LANDevices_Present)
            DeviceRadiator.SetSensorData(RadiatorStarted)
        
        except Exception as e:
            print e 
            # pass

        # ############### Dynamic Config  Start ###################
        # Dynamische Config einlesen #soll ueber http request gesteuert werden.
        dynamicConf = ConfigParser.ConfigParser()
        dynamicConf.read('/var/sensorTool/www/dynamic.conf')
        # Try to change the Relais Status 
        try:
            if dynamicConf.getboolean('modules', 'modules_radiators') != modules_radiators:
                modules_radiators = dynamicConf.getboolean('modules', 'modules_radiators')
                sH_Log.Add(' modules_radiators set to ' + str(modules_radiators))

            if dynamicConf.getboolean('modules', 'modules_motiondetector') != modules_motiondetector:
                modules_motiondetector = dynamicConf.getboolean('modules', 'modules_motiondetector')
                sH_Log.Add(' modules_motiondetector set to ' + str(modules_motiondetector))
                if not modules_motiondetector and motion_detected:
                    motion_detected = False
                    motion_detected_report = False

            if dynamicConf.getboolean('modules', 'modules_surveillance') != modules_surveillance:
                modules_surveillance = dynamicConf.getboolean('modules', 'modules_surveillance')
                sH_Log.Add(' modules_surveillance set to ' + str(modules_surveillance))
                if not modules_surveillance and motion_detected:
                    motion_detected = False
                if modules_surveillance and not modules_motiondetector:
                    sH_Log.Add(' modules_motiondetector set to ' + str(modules_motiondetector))
                    modules_motiondetector = True

            if dynamicConf.getboolean('modules', 'modules_relais') != modules_relais:
                modules_relais = dynamicConf.getboolean('modules', 'modules_relais')
                sH_Log.Add(' modules_relais set to ' + str(modules_relais))

            if dynamicConf.getboolean('modules', 'modules_fritzactors') != modules_fritzactors:
                modules_fritzactors = dynamicConf.getboolean('modules', 'modules_fritzactors')
                sH_Log.Add(' modules_fritzactors set to ' + str(modules_fritzactors))

            if dynamicConf.getboolean('modules', 'modules_LANDevices') != modules_LANDevices:
                modules_LANDevices = dynamicConf.getboolean('modules', 'modules_LANDevices')
                sH_Log.Add(' modules_LANDevices set to ' + str(modules_LANDevices))
                if not modules_LANDevices and LANDevices_Present:
                    LANDevices_Present = False

        except Exception as e:
            print e
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
            #LedY.off()
            vBoolLC = False

        # ############### Check for Radiator interval  start ##################
        vBoolInterval = dictInterval.isNowInInterval()
        # ############### Check for Radiator interval  Ende ##################

        if vVerbose.startswith('test1'):
            print( 'Threshold: ' + str(dictSensors[iControlSensor].GetThreshold()) + ' RadiatorStarted: ' + str(RadiatorStarted) + ' vBoolInterval: ' + str(vBoolInterval) +' modules_radiators: ' + str(modules_radiators))
            
        if dictSensors[iControlSensor].GetThreshold() and RadiatorStarted == False and vBoolInterval and modules_radiators:
            counterHigh = counterHigh + 1
            #if LedY.isOn == False:
            #    LedY.on()
            #    sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (H)!')
        else:
            counterHigh = 0
            
        if dictSensors[iControlSensor].GetThreshold() == False and RadiatorStarted and vBoolInterval and modules_radiators:
            counterLow = counterLow + 1
            #if LedY.isOn == False:
            #    LedY.on()
            #    sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (L)!')
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
                
        if counterHigh == TriggerCountA and RadiatorStarted == False and vBoolInterval and modules_radiators:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(True)
            #LedR.on()
            #LedY.off()
            RadiatorStarted = True
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Started"))
            sH_Log.Add('Radiator activated')
        elif (counterLow == TriggerCountB or vBoolInterval == False or modules_radiators == False) and RadiatorStarted:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)
            #LedR.off()
            #LedY.off()
            RadiatorStarted = False
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
        
        if modules_motiondetector:
            dictPlotS = {}
            sName = DeviceMotion.GetName()
            dictPlotS['ListTime'] = DeviceMotion.GetListTime()
            dictPlotS['ListT'] = DeviceMotion.GetListT()
            dictPlotS['ListRH'] = list()
            dictPlotSens[sName] = dictPlotS

        if modules_LANDevices:
            dictPlotS = {}
            sName = DeviceNetworkDetector.GetName()
            dictPlotS['ListTime'] = DeviceNetworkDetector.GetListTime()
            dictPlotS['ListT'] = DeviceNetworkDetector.GetListT()
            dictPlotS['ListRH'] = list()
            dictPlotSens[sName] = dictPlotS
          
        if modules_radiators:
            dictPlotS = {}
            sName = DeviceRadiator.GetName()
            dictPlotS['ListTime'] = DeviceRadiator.GetListTime()
            dictPlotS['ListT'] = DeviceRadiator.GetListT()
            dictPlotS['ListRH'] = list()
            dictPlotSens[sName] = dictPlotS  
 
        plotting(dictPlotSens, dictPlotAussen, vVerbose)
#        thread.start_new_thread(plotting, (dictPlotSens, dictPlotAussen, vVerbose,))
          
        threadCreatePHPFile('/var/sensorTool/www/sensor.php', getHTML())
#        thread.start_new_thread(threadCreatePHPFile, ('/var/sensorTool/www/sensor.php', getHTML(),))
        
        refreshTime1 = time.time() + INTERVAL_1
    sleep(1) # 0.1

if RadiatorStarted:
    dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)

sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Inactive - going down"))
if vVerbose.startswith('test'):
    print 'GPIO Down'
#LedY.off()
#LedR.off()
#LedG.off()
if boolLeuchte:
    Leuchte.deactivate(boolLeuchte)

if not vVerbose.startswith('test'):
    os.system("sudo init 0")
else:
    print ' - Ende - '

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
