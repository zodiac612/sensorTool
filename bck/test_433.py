#!/usr/bin/env python2.7
# testskript fuer 433MHz
import ConfigParser
#print "start"
PathToConfig='/home/pi/sensorTool/switches.conf'
vVerbose='start'
config = ConfigParser.ConfigParser()
config.read(PathToConfig)
#print(config.sections() ) 

dictGroups = {}
GroupCount = 0
for vSec in config.sections():
    vGroup = config.get(vSec,  'group')
    boolDings = False
    for vGi in dictGroups:
        if dictGroups[vGi]['name'] == vGroup:
            boolDings = True
        
    if not boolDings:
        GroupCount = GroupCount + 1
        dictGroup = {}
        dictGroup['name'] = vGroup
        dictGroup['switches'] = None
        dictGroups[GroupCount] = dictGroup
#print dictGroups

for vKGroup in dictGroups:
    #print str(vKGroup) + " " + str(dictGroups[vKGroup]['name'])
    dictSwitches = {}
    CountSwitch = 0
    for vSec in config.sections():
        vGroup = config.get(vSec,  'group')
        if dictGroups[vKGroup]['name'] == vGroup:
            CountSwitch = CountSwitch + 1
            dictSwitch = {}
            dictSwitch['protocol]'] = config.get(vSec,  'protocol')
            dictSwitch['id'] =  config.get(vSec,  'id') 
            try:    dictSwitch['unit'] = config.get(vSec, 'unit')
            except: dictSwitch['unit'] = None
            dictSwitch['name'] =  config.get(vSec,  'name')
            dictSwitches[CountSwitch] = dictSwitch
    dictGroups[vKGroup]['switches'] = dictSwitches
 
for vGroup in dictGroups:
    print str(vGroup) + ": " + str(dictGroups[vGroup]['name'])
        
    for vDictSwitch in dictGroups[vGroup]['switches']:
        print "  " + str(dictGroups[vGroup]['switches'][vDictSwitch]['name'])
#print dictGroups
