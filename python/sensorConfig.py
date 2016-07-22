#!/usr/bin/python
# -*- coding: latin-1 -*-

import ConfigParser
from tx35dth import tx35dth

class sensorConfig(object):
    def __init__(self, PathToConfig='/home/pi/sensorTool/sensorTool.conf', vVerbose='start'):
        config = ConfigParser.ConfigParser()
        config.read(PathToConfig)
        self.__vVerbose = vVerbose
        if vVerbose.startswith('test'):
            print(config.sections()) 
            
        self.__CryptKey = config.get('global', 'cryptkey')
        self.__MaxTime = config.get('global', 'maxtime') 
        self.__MinTime = config.get('global', 'mintime') 
        self.__Interval_fritzactors = config.getint('fritzactors', 'actinterval')
        self.__Interval_Sensors = config.getint('sensors', 'actinterval')        
        self.__webradio_interval = config.getint('webradio', 'actinterval')
        self.__LANDevices_interval = config.getint('LANDevices', 'actinterval')
        self.__webradio_intervalmotion = config.getint('webradio', 'motiontimeout')        
        self.__Server = 'localhost'

        if vVerbose.startswith('test'):
            self.__Interval_Sensors = config.getint('test', 'test_sensors_actinterval')
            self.__MaxTime = config.get('test', 'test_maxtime')
            self.__Interval_fritzactors = config.getint('test', 'test_fritzactors_actinterval')
            self.__webradio_interval = config.getint('test', 'test_webradio_actinterval')
            self.__LANDevices_interval = config.getint('test', 'test_LANDevices_actinterval')
            self.__webradio_intervalmotion = config.getint('test', 'test_webradio_motiontimeout') 
     
        self.__TriggerCountA = config.getint('sensors', 'trigger_start_count')
        self.__TriggerCountB = config.getint('sensors', 'trigger_end_count')

        self.__dictIntervalle = {}
        iIntervall = 1
        while iIntervall < 100:
            try:
                dictIntervall = {}
                dictIntervall['start'] = config.get('sensors', 'intervalstart_' + str(iIntervall))
                dictIntervall['stop'] = config.get('sensors', 'intervalstop_' + str(iIntervall))
                # print dictIntervall
                self.__dictIntervalle[iIntervall] = dictIntervall
                iIntervall = iIntervall + 1
            except: iIntervall = 100
        # print dictIntervalle
        
        self.__vTitel = config.get('sensors', 'titel')
        CountOfSensors = config.getint('sensors', 'count_of_sensors')

        self.__dictSensors = {}
        self.__iControlSensor = None
        self.__iOutdoorSensor = None
        if CountOfSensors > 0:
            iSensor = 0
            while iSensor < CountOfSensors:
                dictSensor = {}
                try:    dictSensor['bme280'] = config.getboolean('sensor' + str(iSensor), 'bme280')
                except: dictSensor['bme280'] = False
                try:    dictSensor['hex'] = config.get('sensor' + str(iSensor), 'hex')
                except:
                    if dictSensor['bme280']:
                        dictSensor['hex'] = 'bme280'
                    else:
                        dictSensor['hex'] = 'none'   
                             
                try:    dictSensor['name'] = config.get('sensor' + str(iSensor), 'name')
                except: dictSensor['name'] = 'unkown'
                try:    dictSensor['message'] = config.get('sensor' + str(iSensor), 'message')
                except: dictSensor['message'] = 'no message defined'
                try:    dictSensor['delta_message'] = config.get('sensor' + str(iSensor), 'delta_message')
                except: dictSensor['delta_message'] = 'no delta message defined'
                try:    dictSensor['delta_humidity'] = config.getfloat('sensor' + str(iSensor), 'delta_humidity')
                except: pass
                try:    dictSensor['delta_temperature'] = config.getfloat('sensor' + str(iSensor), 'delta_temperature')
                except: pass
                try:    dictSensor['threshold_low_humidity'] = config.getfloat('sensor' + str(iSensor), 'threshold_low_humidity')
                except: pass
                try:    dictSensor['threshold_low_temperature'] = config.getfloat('sensor' + str(iSensor), 'threshold_low_temperature')
                except: pass
                try:    dictSensor['threshold_high_humidity'] = config.getfloat('sensor' + str(iSensor), 'threshold_high_humidity')
                except: pass
                try:    dictSensor['threshold_high_temperature'] = config.getfloat('sensor' + str(iSensor), 'threshold_high_temperature')
                except: pass
                try:    dictSensor['trigger_count'] = config.getint('sensor' + str(iSensor), 'trigger_count')
                except: dictSensor['trigger_count'] = 0
                try:    dictSensor['fritzactor'] = config.get('sensor' + str(iSensor), 'fritzactor')
                except: pass
                try:
                    if config.getboolean('sensor' + str(iSensor), 'control_radiator'):
                        self.__iControlSensor = iSensor
                except: pass  
                try:
                    if config.getboolean('sensor' + str(iSensor),  'outdoor'):
                        self.__iOutdoorSensor = iSensor
                except: pass
                iMobile = 1
                dictMobile = {}
                while iMobile < 100:
                    try:    
                        dictMobile[iMobile] = config.get('sensor' + str(iSensor), 'mobile' + str(iMobile))
                        iMobile = iMobile + 1
                    except: iMobile = 100
                dictSensor['mobiles'] = dictMobile
                if dictSensor['hex'] is not None:
                    self.__dictSensors[iSensor] = tx35dth(dictSensor)
                iSensor = iSensor + 1
            # While iSensor < CountOfSensors:
        if vVerbose.startswith('test'):
            print('T2: Sensorcount: ' + str(iSensor))
            # print dictSensors
            print('T2: control_radiator = Sensor' + str(self.__iControlSensor))
        
        self.__httpdport = config.getint('lacrosse', 'httpdport')
 
        self.__RelayIN1 = config.getint('gpiopins', 'RelayIN1')
        self.__RelayIN2 = config.getint('gpiopins', 'RelayIN2')
        self.__LedGreen = config.getint('gpiopins', 'LedGreen')
        self.__LedYellow = config.getint('gpiopins', 'LedYellow')
        self.__LedRed = config.getint('gpiopins', 'LedRed')
        self.__motion = config.getint('gpiopins', 'motion')
        self.__light = config.getint('gpiopins', 'light')
        
        self.__modules_webradio = config.getboolean('modules', 'modules_webradio')
        self.__modules_webradiomotion = config.getboolean('modules', 'modules_webradiomotion')
        self.__modules_surveillance = config.getboolean('modules', 'modules_surveillance')
        self.__modules_radiators = config.getboolean('modules', 'modules_radiators')
        self.__modules_relais = config.getboolean('modules', 'modules_relais')
        self.__modules_fritzactors = config.getboolean('modules', 'modules_fritzactors')
        self.__modules_LANDevices = config.getboolean('modules', 'modules_LANDevices')
        self.__modules_motiondetector = config.getboolean('modules','modules_motiondetector')
        
        print('sensorService config')

    def getIntervalWebradio(self):
        return self.__webradio_interval

    def getIntervalLANDevices(self):
        return self.__LANDevices_interval

    def getIntervalWebradiomotion(self):
        return self.__webradio_intervalmotion

    def getModuleWebradiomotion(self):
        return self.__modules_webradiomotion
        
    def getWebradioTimeOut(self):
        return self.__webradio_timeout        

    def getModuleWebradio(self):
        return self.__modules_webradio
    
    def getModuleMotiondetector(self):
        return self.__modules_motiondetector
        
    def getModuleSurveillance(self):
        return self.__modules_surveillance
    
    def getModuleRadiators(self):
        return self.__modules_radiators
    
    def getModuleRelais(self):
        return self.__modules_relais

    def getModuleFritzActors(self):
        return self.__modules_fritzactors
    
    def getModuleLANDevices(self):
        return self.__modules_LANDevices

    def getHttpdPort (self):
        return self.__httpdport

    def getGPIORelayIN1 (self):
        return self.__RelayIN1

    def getGPIORelayIN2 (self):
        return self.__RelayIN2
    
    def getGPIOLedGreen (self):
        return self.__LedGreen

    def getGPIOLedYellow (self):
        return self.__LedYellow

    def getGPIOLedRed (self):
        return self.__LedRed

    def getGPIOmotion (self):
        return self.__motion

    def getGPIOlight (self):
        return self.__light

    def getCryptKey(self):
        return self.__CryptKey
    
    def getIntervalSensors(self):
        return self.__Interval_Sensors

    def getMaxTime(self):
        return self.__MaxTime
    
    def getMinTime(self):
        return self.__MinTime 
    
    def getIntervalActors(self):
        return self.__Interval_fritzactors

    def getServer(self):
        return self.__Server
    
    def getTriggerCountA(self):
        return self.__TriggerCountA

    def getTriggerCountB(self):
        return self.__TriggerCountB

    def getDictIntervalle(self):
        return self.__dictIntervalle

    def getTitel(self):
        return self.__vTitel

    def getDictSensors(self):
        return self.__dictSensors
        
    def getiControlSensor(self):
        return self.__iControlSensor

    def getiOutdoorSensor(self):
        return self.__iOutdoorSensor
               
    def SetupDynamicConfig(self,  sPathToConfig = '/var/sensorTool/www/dynamic.conf'):
        configDyn = ConfigParser.RawConfigParser()
        configDyn.read(sPathToConfig)

        vSection = 'modules'
        configDyn.set(vSection,  'modules_webradio', self.__modules_webradio)
        configDyn.set(vSection,  'modules_webradiomotion', self.__modules_webradiomotion)
        configDyn.set(vSection,  'modules_surveillance', self.__modules_surveillance)
        configDyn.set(vSection,  'modules_radiators', self.__modules_radiators)
        configDyn.set(vSection,  'modules_relais', self.__modules_relais)
        configDyn.set(vSection,  'modules_fritzactors', self.__modules_fritzactors)
        configDyn.set(vSection,  'modules_LANDevices', self.__modules_LANDevices)
        configDyn.set(vSection,  'modules_motiondetector', self.__modules_motiondetector)
        
        with open(str(sPathToConfig), 'wb') as configfile:
            configDyn.write(configfile) 
            
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
