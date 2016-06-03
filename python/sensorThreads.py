#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
import ast
import datetime
from fritzActor import fritzActor

def threadPICAM(qPIC):
    #print 'threadPICAM start'
    os.system("/home/pi/sensorTool/sh/picam.sh")
    qPIC.get()
    qPIC.task_done()
    qPIC.put(True)
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

def threadWebradioService(sPathToConfig = '/var/sensorTool/www/webradio.station'):
    config = ConfigParser.RawConfigParser()
    config.read(sPathToConfig)
    
    if config.getboolean('running', 'changed'):
        sArg = config.get('running',  'action') + ' ' + config.get('running',  'stream')+' '+config.get('running',  'volume')
        print sArg
        os.system("/home/pi/webradio/webradio.sh " + sArg + " &")
        #os.system("echo \""+sArg+"\"")
        config.set('running', 'changed', False)
        with open(str(sPathToConfig), 'wb') as configfile:
            config.write(configfile) 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
