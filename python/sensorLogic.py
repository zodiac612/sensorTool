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
from time import sleep
from plotting import plotting_DeviceValues
from sensorCrypt import sensorCrypt
from sensorLight import sensorLight #ok
from sensorInterval import sensorInterval #ok
from sensorConfig import sensorConfig #ok
from sensorThreads import threadPICAM2
from sensorThreads import threadFritzActors2 #ok
from sensorThreads import threadNetDiscovery #ok
from sensorThreads import threadCreatePHPFile #ok
from sensorThreads import threadWebradioService
from sensorSwitches import sensorSwitches
from sensorDevice import moduleDevice
#from sensorService import threadSensors

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
MAXTIME = sConfig.getMaxTime() 
MINTIME = sConfig.getMinTime() 
INTERVAL_SENSORS = sConfig.getIntervalSensors()
INTERVAL_FRITZACTORS = sConfig.getIntervalActors()
INTERVAL_WEBRADIO = sConfig.getIntervalWebradio()
INTERVAL_LANDEVICES = sConfig.getIntervalLANDevices()
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
iOutdoorSensor = sConfig.getiOutdoorSensor()
boolOutdoorSensor = False
if iOutdoorSensor is not None:
   boolOutdoorSensor = True
sH_Log = sensorHistory('/var/sensorTool/www/loglatestentry.php', '/var/sensorTool/www/logdata.php')
iLog = 0

modules_webradio = sConfig.getModuleWebradio() # ok
webradio_active = False 
modules_webradiomotion = sConfig.getModuleWebradiomotion() # ok
webradio_motionTimeOut = sConfig.getIntervalWebradiomotion()
webradio_motionActive = True
modules_surveillance = sConfig.getModuleSurveillance() # ok
modules_motiondetector = sConfig.getModuleMotiondetector() 
motion_detected = False
motion_detected_report = False
ledalarm = False

modules_radiators = sConfig.getModuleRadiators() # ok
RadiatorStarted = False
modules_relais = sConfig.getModuleRelais()
modules_fritzactors = sConfig.getModuleFritzActors() # ok
modules_LANDevices = sConfig.getModuleLANDevices() # ok
LANDevices_Present = False
LANNetwork = sConfig.getLANNetwork()
dictMobileHosts = sConfig.getdictMobileHosts()

sConfig.SetupDynamicConfig('/var/sensorTool/www/dynamic.conf')

dictActiveModules = {}
dictActiveModules['time'] = list()
dictActiveModules['Motiondetector']  = moduleDevice(20)
dictActiveModules['NetworkDeviceDetector'] = moduleDevice(30)
dictActiveModules['Webradio']  = moduleDevice(40)
dictActiveModules['Radiators']  = moduleDevice(60)
dictActiveModules['ledalarm']  = moduleDevice(90)

dictTemperature = {}
dictTemperature['time'] = list()
dictRelativeHumidity = {}
dictRelativeHumidity['time'] = list()
dictAbsoluteHumidity = {}
dictAbsoluteHumidity['time'] = list()
dictPressure = {}
dictPressure['time'] = list()

for vKey in dictSensors:
    sSensorName = dictSensors[vKey].GetSensor()
    dictTemperature[sSensorName] = moduleDevice(0)
    dictRelativeHumidity[sSensorName] = moduleDevice(0)
    dictAbsoluteHumidity[sSensorName] = moduleDevice(0)
    if dictSensors[vKey].GetBME():
        dictPressure[sSensorName] = moduleDevice(0)

if vVerbose == 'test':
    print 'MAXTIME' + str(MAXTIME)
    print 'MINTIME' + str(MINTIME)
    print 'INTERVAL_SENSORS' + str(INTERVAL_SENSORS)
    print 'INTERVAL_FRITZACTORS' + str(INTERVAL_FRITZACTORS)
    print 'INTERVAL_WEBRADIO' + str(INTERVAL_WEBRADIO)
    print 'INTERVAL_LANDEVICES' + str(INTERVAL_LANDEVICES)
    print 'webradio_motionTimeOut' + str(webradio_motionTimeOut)
    sleep(1)

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
   
   for vKey in dictActiveModules:
       if vKey <> 'time':
           vhttpResult += dictActiveModules[vKey].GetHttpTable(vKey)

   if modules_fritzactors:
       for vAKey in dictActors:
           vhttpResult += dictActors[vAKey].GetHttpTable()
       
   vhttpResult += 'echo "</TD></TR></TABLE></DIV>\\n";\n'
   return vhttpResult

# refresh for sensor data
refreshTime_sensors = time.time() + INTERVAL_SENSORS
# refresh for fritz actors
refreshTime_fritzactors = time.time()

refreshTime_webradio = time.time()
refreshTime_motiondetector = time.time()
# refresh for Queue

# if vVerbose.startswith('test'):
#     INTERVAL_LANDEVICES = 3   
refreshTime_LANDevices = time.time() + INTERVAL_LANDEVICES
qNDD = Queue.LifoQueue(maxsize=1)
DiscoveryInProgress = False
refreshTime_Queue = 5
INTERVAL_QUEUE = 5
refreshTime_webradioMotion = time.time() + webradio_motionTimeOut

# FAInProgress = False
# qFA = Queue.LifoQueue(maxsize=1)


# loop ------------------------------------------------------------------------
#LedR.off()
if vVerbose.startswith('test1'):
    print 'Config loaded'
    print str(refreshTime_sensors) + '##' + str(time.time())
    
while time.strftime('%H%M') < MAXTIME:  # timeDuration <= MAXTIME: 
    # Check NDD Queue every INTERVAL_LANDEVICES secs
    if time.time() > refreshTime_Queue:
        if vVerbose.startswith('test'):
            print str(time.time())+'while: refreshTime_Queue ('+str(refreshTime_Queue)+')'
        if not qNDD.empty():
            #dictNetDevs = {}
            #dictNetDevs = qNDD.get()
            boolNDD = qNDD.get()
            LANDevices_Present = boolNDD
            if vVerbose.startswith('test'):
                print str(time.time())+'while: refreshTime_Queue: NDD (True) : LANDevices_Present ('+str(LANDevices_Present)+')'
            qNDD.task_done()
            DiscoveryInProgress = False
            
        refreshTime_Queue = time.time() + INTERVAL_QUEUE
    
    if time.time() > refreshTime_motiondetector:
        if vVerbose.startswith('test1'):
            print str(time.time())+'while: refreshTime_motiondetector ('+str(refreshTime_motiondetector)+')'
        if modules_motiondetector:
            if vVerbose.startswith('test1'):
                print str(time.time())+'while: refreshTime_motiondetector: modules_motiondetector'
            if BMelder.status() == 1:
                motion_detected = True
                motion_detected_report = True
            else:
                motion_detected = False
            if vVerbose.startswith('test1'):
                print str(time.time())+'while: refreshTime_motiondetector: modules_motiondetector: motion_detected_report('+str(motion_detected_report)+')'
                
        if modules_surveillance and modules_motiondetector:
            if vVerbose.startswith('test1'):
                print str(time.time())+'while: refreshTime_motiondetector: modules_surveillance, modules_motiondetector'
            if not LANDevices_Present:
                if motion_detected:
                    threadPICAM2('surveillance')
                    sH_Log.Add(' surveillance take picset ')
            else:
                threadPICAM2('low')
                sH_Log.Add(' surveillance take pic low ')
                
        refreshTime_motiondetector = time.time() + 1
        
    if time.time() > refreshTime_LANDevices:
        if vVerbose.startswith('test1'):
            print str(time.time())+'while: refreshTime_LANDevices ('+str(refreshTime_LANDevices)+')'
        if modules_LANDevices:
            if vVerbose.startswith('test1'):
                print str(time.time())+'while: refreshTime_LANDevices: modules_LANDevices'
            #parallel with threading and queue
            if not DiscoveryInProgress:
                if vVerbose.startswith('test1'):
                    print str(time.time())+'while: refreshTime_LANDevices: modules_LANDevices: Start Network Device Discovery!'
                thread.start_new_thread(threadNetDiscovery,  (qNDD,  LANNetwork,  dictMobileHosts) )
                DiscoveryInProgress = True
            else:
                if vVerbose.startswith('test1'):
                    print 'Discovery running'
        
        refreshTime_LANDevices = time.time() + INTERVAL_LANDEVICES

    # get fritz actor data
    if time.time() > refreshTime_fritzactors:
        if vVerbose.startswith('test1'):
            print str(time.time())+'while: refreshTime_fritzactors ('+str(refreshTime_fritzactors)+')'        
        if modules_fritzactors:
            if vVerbose.startswith('test1'):
                print str(time.time())+'while: refreshTime_fritzactors: modules_fritzactors'        
            dictActors = threadFritzActors2()
                
            # On Startup stop running radiators
            if vBoolLC:# and not FAInProgress:
                dictActors[str(dictSensors[iControlSensor].GetFritzActor())].SetActor(False)
        refreshTime_fritzactors = time.time() + INTERVAL_FRITZACTORS
    
    # Check if there is a webradio setting change
    if time.time() > refreshTime_webradio: 
        if vVerbose.startswith('test'):
            print str(time.time())+'while: refreshTime_webradio ('+str(refreshTime_webradio)+')'    
  
        if modules_webradio:
            if vVerbose.startswith('test'):
                print str(time.time())+'while: refreshTime_webradio: modules_webradio'
            (webradio_active1, webradio_changed, webradio_result) = threadWebradioService('/var/sensorTool/www/webradio.station', webradio_active)
            if webradio_changed:
                if webradio_active <> webradio_active1:
                    webradio_active = webradio_active1
                sH_Log.Add(' Webradio change: ' + str(webradio_result))       
        elif not modules_webradio and webradio_active:
            if vVerbose.startswith('test'):
                print str(time.time())+'while: refreshTime_webradio: not modules_webradio, webradio_active'
            (webradio_active, webradio_changed, webradio_result) = threadWebradioService('/var/sensorTool/www/webradio.station', webradio_active, True)
            sH_Log.Add(' Webradio stopped')

        if webradio_motionActive and not webradio_active and modules_webradio and modules_webradiomotion:
            if vVerbose.startswith('test'):
                print str(time.time())+'while: refreshTime_webradio: webradio_motionActive, webradio_active, modules_webradio, modules_webradiomotion'    
            refreshTime_webradioMotion = time.time() + webradio_motionTimeOut
            (webradio_active, webradio_changed, webradio_result) = threadWebradioService('/var/sensorTool/www/webradio.station', webradio_active, False,  True)
            sH_Log.Add(' Webradio started')
        
        refreshTime_webradio = time.time() + INTERVAL_WEBRADIO

    #print 'time '+str(time.time())+'>'+str(refreshTime_webradioMotion)+' refreshTime_webradioMotion'
    # Timeout for webradio - stop when no motion is detected (active motioncontrol)
    if time.time() > refreshTime_webradioMotion:
        if vVerbose.startswith('test'):
            print str(time.time())+'while: refreshTime_webradioMotion ('+str(refreshTime_webradioMotion)+')'
            #print str(time.time())+'while: refreshTime_webradioMotion: modules_webradio ('+str(modules_webradio)+'), modules_webradiomotion ('+str(modules_webradiomotion)+'), not webradio_motionActive('+str(webradio_motionActive)+')'            
        if modules_webradio and modules_webradiomotion and not webradio_motionActive and webradio_active:
            if vVerbose.startswith('test'):
                print str(time.time())+'while: refreshTime_webradioMotion: modules_webradio ('+str(modules_webradio)+'), modules_webradiomotion ('+str(modules_webradiomotion)+'), not webradio_motionActive('+str(webradio_motionActive)+'), webradio_active ('+str(webradio_active)+')'            
            (webradio_active, webradio_changed, webradio_result) = threadWebradioService('/var/sensorTool/www/webradio.station', webradio_active, True)
            sH_Log.Add(' Webradio stopped, no motion') 
        refreshTime_webradioMotion = time.time() + INTERVAL_WEBRADIO

    # every refreshtime  seconds,  get data from SensorService
    if time.time() > refreshTime_sensors:
        if vVerbose.startswith('test'):
            print str(time.time())+'while: refreshTime_sensors ('+str(refreshTime_sensors)+')'
            print str(refreshTime_sensors) + '##' + str(time.time())
        # Werte holen per http request ::D
        try:
            dictResponse = {}
            
            vBoolUseSensorValueFile = False
            if vBoolUseSensorValueFile:
                try:
                    handle = open ('/var/sensorTool/sensorValues', 'r')
                    line = " "
                    while line:
                        line = handle.readline()
                        print line
                        if len(line) > 0:
                            dictResponse = ast.literal_eval(line)
                    handle.close()
                except Exception as e:
                    print str(e)
            else:
                # print 'Get HTTP Service'
                r = requests.get("http://" + SERVER + ":6666")
                # request enthaelt "
                # print r
                vR = sCrypt.Decrypt(r.text[1:len(r.text) - 1])
                # print vR
                dictResponse = ast.literal_eval(str(vR))

            print 'dictResponse: ' + str(dictResponse) 
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
        
            #DeviceMotion.SetSensorData(motion_detected_report)
            if modules_webradiomotion:
                
                if motion_detected_report:
                # if motion detected than increase refreshTime_webradioMotion by webradio_motionTimeOut
                    webradio_motionActive = True
                    refreshTime_webradioMotion = time.time() + webradio_motionTimeOut
                    print refreshTime_webradioMotion
                else:
                    
                    # no motion detected, but mobile device present, webradio must be acticve
                    if modules_LANDevices and LANDevices_Present:
                        webradio_motionActive = True
                        refreshTime_webradioMotion = time.time() + webradio_motionTimeOut
                        print refreshTime_webradioMotion                       
                    else:
                        webradio_motionActive = False
             
            # Values for Diagramm 
            
            sPlottingTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            dictTemperature['time'].append(sPlottingTime)
            dictRelativeHumidity['time'].append(sPlottingTime)
            dictAbsoluteHumidity['time'].append(sPlottingTime)
            dictPressure['time'].append(sPlottingTime)
            for vKey in dictSensors:
                sSensorName = dictSensors[vKey].GetSensor()
                dictTemperature[sSensorName].SetModuleValue(dictSensors[vKey].GetT())
                dictRelativeHumidity[sSensorName] .SetModuleValue(dictSensors[vKey].GetRH())
                dictAbsoluteHumidity[sSensorName].SetModuleValue(dictSensors[vKey].GetAH())
                if dictSensors[vKey].GetBME():
                    dictPressure[sSensorName].SetModuleValue(dictSensors[vKey].GetPA())
                
            dictActiveModules['time'].append(sPlottingTime)
            dictActiveModules['Motiondetector'].SetModuleStatus(motion_detected_report)
            dictActiveModules['NetworkDeviceDetector'].SetModuleStatus(LANDevices_Present)
            dictActiveModules['Webradio'].SetModuleStatus(webradio_active)
            dictActiveModules['Radiators'].SetModuleStatus(RadiatorStarted)
            dictActiveModules['ledalarm'].SetModuleStatus(ledalarm)
            motion_detected_report = False
            ledalarm = False
        
        except Exception as e:
            sH_Log.Add(str(e)) 
            print e
            # pass

        # ############### Dynamic Config  Start ###################
        # Dynamische Config einlesen #soll ueber http request gesteuert werden.
        dynamicConf = ConfigParser.ConfigParser()
        dynamicConf.read('/var/sensorTool/www/dynamic.conf')
        # Try to change the Relais Status 
        try:
            if vVerbose.startswith('test'):
                print str(time.time())+'while: refreshTime_sensors: dynamicConf'
            
            if dynamicConf.getboolean('modules', 'modules_radiators') != modules_radiators:
                modules_radiators = dynamicConf.getboolean('modules', 'modules_radiators')
                sH_Log.Add(' modules_radiators set to ' + str(modules_radiators))
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_radiators('+str(modules_radiators)+')'

            if dynamicConf.getboolean('modules', 'modules_motiondetector') != modules_motiondetector:
                modules_motiondetector = dynamicConf.getboolean('modules', 'modules_motiondetector')
                sH_Log.Add(' modules_motiondetector set to ' + str(modules_motiondetector))
                if not modules_motiondetector and motion_detected:
                    motion_detected = False
                    motion_detected_report = False
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_motiondetector('+str(modules_motiondetector)+')'

            if dynamicConf.getboolean('modules', 'modules_surveillance') != modules_surveillance:
                modules_surveillance = dynamicConf.getboolean('modules', 'modules_surveillance')
                sH_Log.Add(' modules_surveillance set to ' + str(modules_surveillance))
                if not modules_surveillance and motion_detected:
                    motion_detected = False
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_surveillance('+str(modules_surveillance)+')'
                if modules_surveillance and not modules_motiondetector:
                    sH_Log.Add(' modules_motiondetector set to ' + str(modules_motiondetector))
                    modules_motiondetector = True
                    if vVerbose.startswith('test'):
                        print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_surveillance: modules_motiondetector('+str(modules_motiondetector)+')'

            if dynamicConf.getboolean('modules', 'modules_relais') != modules_relais:
                modules_relais = dynamicConf.getboolean('modules', 'modules_relais')
                sH_Log.Add(' modules_relais set to ' + str(modules_relais))
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_relais('+str(modules_relais)+')'

            if dynamicConf.getboolean('modules', 'modules_fritzactors') != modules_fritzactors:
                modules_fritzactors = dynamicConf.getboolean('modules', 'modules_fritzactors')
                sH_Log.Add(' modules_fritzactors set to ' + str(modules_fritzactors))
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_fritzactors('+str(modules_fritzactors)+')'

            if dynamicConf.getboolean('modules', 'modules_LANDevices') != modules_LANDevices:
                modules_LANDevices = dynamicConf.getboolean('modules', 'modules_LANDevices')
                sH_Log.Add(' modules_LANDevices set to ' + str(modules_LANDevices))
                if not modules_LANDevices and LANDevices_Present:
                    LANDevices_Present = False
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_LANDevices('+str(modules_LANDevices)+')'
                        
            if dynamicConf.getboolean('modules', 'modules_webradio') != modules_webradio:
                modules_webradio = dynamicConf.getboolean('modules', 'modules_webradio')
                sH_Log.Add(' modules_webradio set to ' + str(modules_webradio))
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_webradio('+str(modules_webradio)+')'
                    
            if dynamicConf.getboolean('modules', 'modules_webradiomotion') != modules_webradiomotion:
                modules_webradiomotion = dynamicConf.getboolean('modules', 'modules_webradiomotion')
                sH_Log.Add(' modules_webradiomotion set to ' + str(modules_webradiomotion))
                if not modules_webradiomotion and not webradio_motionActive:
                    webradio_motionActive = True
                if vVerbose.startswith('test'):
                    print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_webradiomotion('+str(modules_webradiomotion)+')'
                if modules_webradiomotion and not modules_webradio:
                    sH_Log.Add(' modules_webradio set to ' + str(modules_webradio))
                    modules_webradio = True
                    if vVerbose.startswith('test'):
                        print str(time.time())+'while: refreshTime_sensors: dynamicConf: modules_webradiomotion: modules_webradio('+str(modules_webradio)+')'

        except Exception as e:
            sH_Log.Add(str(e)) 
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
         
        boolTriggerOutdoor = True
        if boolOutdoorSensor:
            deltaAH = 0.5
            if dictSensors[iControlSensor].GetAH() is not None and dictSensors[iOutdoorSensor].GetAH() is not None:
                if (float(dictSensors[iControlSensor].GetAH())) < (float(dictSensors[iOutdoorSensor].GetAH())+ deltaAH):
                    boolTriggerOutdoor = False
      
        if dictSensors[iControlSensor].GetThreshold() and RadiatorStarted == False and vBoolInterval and modules_radiators and boolTriggerOutdoor:
            counterHigh = counterHigh + 1
            #if LedY.isOn == False:
            #    LedY.on()
            #    sH_Log.Add(dictSensors[iControlSensor].GetSensor() + ' Yellow LED (H)!')
        else:
            counterHigh = 0
            
        if dictSensors[iControlSensor].GetThreshold() == False and RadiatorStarted and vBoolInterval and modules_radiators and boolTriggerOutdoor:
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
                ledalarm = True
        else:
            if boolLeuchte:
                boolLeuchte = Leuchte.deactivate(boolLeuchte)
                
        if counterHigh == TriggerCountA and RadiatorStarted == False and vBoolInterval and modules_radiators and boolTriggerOutdoor:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(True)
            #LedR.on()
            #LedY.off()
            RadiatorStarted = True
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Started"))
            sH_Log.Add('Radiator activated')
        elif (counterLow == TriggerCountB or vBoolInterval == False or modules_radiators == False or boolTriggerOutdoor == False) and RadiatorStarted:
            dictActors[dictSensors[iControlSensor].GetFritzActor()].SetActor(False)
            #LedR.off()
            #LedY.off()
            RadiatorStarted = False
            sendWhatsApps(dictSensors[iControlSensor].GetMobiles(), getInfoText("Stopped"))
            sH_Log.Add('Radiator deactivated')
            
        if vVerbose.startswith('test'):
            #print getInfoText("Status")
            print '##### - #####'

        threadCreatePHPFile('/var/sensorTool/www/sensor.php', getHTML())
#        thread.start_new_thread(threadCreatePHPFile, ('/var/sensorTool/www/sensor.php', getHTML(),))        

        plotting_DeviceValues(dictActiveModules,  '1_Modules',  vVerbose)
        plotting_DeviceValues(dictTemperature, '3_Temperature',  vVerbose,  -20,  50)
        plotting_DeviceValues(dictRelativeHumidity, '4_Relative_Humidity',  vVerbose)
        plotting_DeviceValues(dictAbsoluteHumidity, '2_Absolute_Humidity',  vVerbose,  0,  30)
        plotting_DeviceValues(dictPressure, '9_Pressure',  vVerbose,  700,  1100)
        
#        thread.start_new_thread(plotting, (dictPlotSens, dictPlotAussen, vVerbose,))
          
        refreshTime_sensors = time.time() + INTERVAL_SENSORS
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
