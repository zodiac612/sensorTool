#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
import ast
import datetime
import ConfigParser
from fritzActor import fritzActor

def threadPICAM(qPIC):
    #print 'threadPICAM start'
    os.system("/home/pi/sensorTool/sh/picam.sh")
    qPIC.get()
    qPIC.task_done()
    qPIC.put(True)
    #print 'threadPICAM ende'

def threadPICAM2(picRes = 'low'):
    #print 'threadPICAM start'
    os.system("/home/pi/sensorTool/sh/picam.sh " + picRes)
    #print 'threadPICAM ende'

    
def threadNetDiscovery(qNDD):
    command = "/home/pi/sensorTool/sh/ScanNetworkDevices.sh"
    dictNDDs = {}
    handle = os.popen(command)
    line = " "
    boolDevicePresent = False
    while line:
        line = handle.readline()
        if len(line) > 0:
            dictNDD= {}
            dictNDD = ast.literal_eval(line)
            if 'IP' in dictNDD:
                dictNDDs[dictNDD['IP']] = dictNDD
                if dictNDD['hostname']  == 'Nexus5X.fritz.box' and dictNDD['status'] == 'Up':
                    #print dictNDD
                    boolDevicePresent = True
                if dictNDD['hostname']  == 'Windows-Phone.fritz.box' and dictNDD['status'] == 'Up':
                    boolDevicePresent = True                    
    handle.close()
    if not qNDD.empty():
        qNDD.get()
        qNDD.task_done()
    #if you need more info in logic part than use the dictNDDs dictonary and not the boolDevicePesent boolean
    qNDD.put(boolDevicePresent)
    #pass

def threadNetDiscovery2():
    command = "/home/pi/sensorTool/sh/ScanNetworkDevices.sh"
    dictNDDs = {}
    handle = os.popen(command)
    line = " "
    boolDevicePresent = False
    while line:
        line = handle.readline()
        if len(line) > 0:
            dictNDD= {}
            dictNDD = ast.literal_eval(line)
            if 'IP' in dictNDD:
                dictNDDs[dictNDD['IP']] = dictNDD
                if dictNDD['hostname']  == 'Nexus5X.fritz.box' and dictNDD['status'] == 'Up':
                    #print dictNDD
                    boolDevicePresent = True
                if dictNDD['hostname']  == 'Windows-Phone.fritz.box' and dictNDD['status'] == 'Up':
                    boolDevicePresent = True                    
    handle.close()
    #if you need more info in logic part than use the dictNDDs dictonary and not the boolDevicePesent boolean
    return boolDevicePresent
    #pass

def threadFritzActors(qFA):
    dictActors = {}
    command = "/home/pi/sensorTool/sh/fritzbox-smarthome.sh csvlist"  # raw_input("Kommando: ")
    try:
        handle = os.popen(command)
        line = " "
        while line:
            line = handle.readline()
            if len(line) > 0:
                if line.startswith('{"id":'):
                    dictActor = {}
                    dictActor = ast.literal_eval(line)
                    if 'id' in dictActor:
                        dictActor['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if dictActor['id'] in dictActors:
                            dictActors[dictActor['id']].UpdateActorData(dictActor)
                        else:
                            dictActors[dictActor['id']] = fritzActor(dictActor)
        handle.close()
        if not qFA.empty():
            qFA.get()
            qFA.task_done()
        #print dictActors
        qFA.put(dictActors)
        #pass
    except:
        print str(datetime.time()) + ': Get fritz actor info failed'
#        sH_Log.Add('Get fritz actor info failed')

def threadFritzActors2():
    dictActors = {}
    command = "/home/pi/sensorTool/sh/fritzbox-smarthome.sh csvlist"  # raw_input("Kommando: ")
    try:
        handle = os.popen(command)
        line = " "
        while line:
            line = handle.readline()
            if len(line) > 0:
                if line.startswith('{"id":'):
                    dictActor = {}
                    dictActor = ast.literal_eval(line)
                    if 'id' in dictActor:
                        dictActor['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if dictActor['id'] in dictActors:
                            dictActors[dictActor['id']].UpdateActorData(dictActor)
                        else:
                            dictActors[dictActor['id']] = fritzActor(dictActor)
        handle.close()
        
        return dictActors
        #pass
    except:
#        print str(datetime.time()) + ': Get fritz actor info failed'
        return {}
#        sH_Log.Add('Get fritz actor info failed')

def threadPilightService(sArg):
    os.system("sudo service pilight " + sArg)

def threadCreatePHPFile(sFileName,  sArg):
    try:  
        filecontent = '<?php\n'
        filecontent += sArg
        filecontent += '\n?>'
        fileHandle = open (sFileName, 'w')
        fileHandle.write (filecontent)
        fileHandle.close()
    except:
        pass

def threadWebradioService(sPathToConfig = '/var/sensorTool/www/webradio.station', webradio_active = False, boolStop = False):
    configRadio = ConfigParser.RawConfigParser()
    configRadio.read(sPathToConfig)
    result = None 
    webradio_changed = False
    if not boolStop:
        if configRadio.getboolean('running', 'changed'):
            sArg = configRadio.get('running',  'action') + ' ' + configRadio.get('running',  'stream')+' '+configRadio.get('running',  'volume')
            result = 'Action: ' + configRadio.get('running',  'action') + ', Stream: ' + configRadio.get('running',  'stream')+', Volume: '+configRadio.get('running',  'volume')
            #print sArg
            os.system("/home/pi/webradio/webradio.sh " + sArg +" &")
            webradio_changed = True
            #os.system("echo \""+sArg+"\"")
            if configRadio.get('running', 'action') == 'start':
                webradio_active = True
            else:
                webradio_active = False
                
            configRadio.set('running', 'changed', False)
            with open(str(sPathToConfig), 'wb') as configRadioFile:
                configRadio.write(configRadioFile)
    else:
        os.system("/home/pi/webradio/webradio.sh stop &")
        webradio_changed = True
        webradio_active = False
    
    if not webradio_active:
        result = None 
    return (webradio_active, webradio_changed, result)  

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
