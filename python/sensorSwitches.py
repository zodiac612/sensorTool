#!/usr/bin/python
# -*- coding: latin-1 -*-

import ConfigParser
from sensorThreads import threadCreateFile #ok

def sensorSwitches(PathToConfig='/home/pi/sensorTool/switches.conf', vVerbose='start'):
    config = ConfigParser.ConfigParser()
    config.read(PathToConfig)
    #print(config.sections() ) 

    dictGroups = {}
    GroupCount = 0
    for vSec in config.sections():
	if vSec[:6] == 'Switch':
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
	  if vSec[:6] == 'Switch':
            vGroup = config.get(vSec,  'group')
            if dictGroups[vKGroup]['name'] == vGroup:
                CountSwitch = CountSwitch + 1
                dictSwitch = {}
                dictSwitch['protocol'] = config.get(vSec,  'protocol')
                dictSwitch['id'] =  config.get(vSec,  'id') 
                try:    dictSwitch['unit'] = config.get(vSec, 'unit')
                except: dictSwitch['unit'] = None
                dictSwitch['name'] =  config.get(vSec,  'name')
                dictSwitches[CountSwitch] = dictSwitch
        dictGroups[vKGroup]['switches'] = dictSwitches
     
    #for vGroup in dictGroups:
        #print str(vGroup) + ": " + str(dictGroups[vGroup]['name'])
            
        #for vDictSwitch in dictGroups[vGroup]['switches']:
            #print "  " + str(dictGroups[vGroup]['switches'][vDictSwitch]['name'])
            
    vhttpResult = ''
    for vGroup in dictGroups:
        #print str(vGroup) + ": " + str(dictGroups[vGroup]['name'])
        vhttpResult += 'echo "  <table class=\\"switch\\">\\n";\n'
        vhttpResult += 'echo "    <th>' + str(dictGroups[vGroup]['name']) + '</th>\\n";\n'
        for vDictSwitch in dictGroups[vGroup]['switches']:
            #print "  " + str(dictGroups[vGroup]['switches'][vDictSwitch])
            vhttpResult += 'echo "    <tr>\\n";\n'
            vhttpResult += 'echo "      <td class=\\"switchlabel\\">'+str(dictGroups[vGroup]['switches'][vDictSwitch]['name'])+'</td>\\n";\n'
            vhttpResult += 'echo "      <td class=\\"switch\\">\\n";\n'
            vhttpResult += 'echo "        <form class=\\"switch\\" method=\\"post\\">\\n";\n'
            vhttpResult += 'echo "          <input type=\\"hidden\\" name=\\"SwitchID\\" value=\\"'+str(dictGroups[vGroup]['switches'][vDictSwitch]['id'])+'\\">\\n";\n'
            #if 'unit' in dictGroups[vGroup]['switches'][vDictSwitch] and not dictGroups[vGroup]['switches'][vDictSwitch]['unit'] is None:
            if not (dictGroups[vGroup]['switches'][vDictSwitch]['unit'] is None):
                vhttpResult += 'echo "          <input type=\\"hidden\\" name=\\"SwitchUnit\\" value=\\"'+str(dictGroups[vGroup]['switches'][vDictSwitch]['unit'])+'\\">\\n";\n'
            vhttpResult += 'echo "          <input type=\\"hidden\\" name=\\"SwitchProtocol\\" value=\\"'+str(dictGroups[vGroup]['switches'][vDictSwitch]['protocol'])+'\\">\\n";\n'
            vhttpResult += 'echo "	        <button class=\\"switch\\" type=\\"submit\\" name=\\"SwitchAction\\" value=\\"1\\">An</button>\\n";\n'
            vhttpResult += 'echo "          <button class=\\"switch\\" type=\\"submit\\" name=\\"SwitchAction\\" value=\\"0\\">Aus</button>\\n";\n'
            vhttpResult += 'echo "        </form>\\n";\n'
            vhttpResult += 'echo "      </td>\\n";\n'
        vhttpResult += 'echo "	  </tr>\\n";\n'
        vhttpResult += 'echo "	</table>\n";\n'
        vhttpResult += 'echo "	<br />\n";\n'
        
    #print vhttpResult
    threadCreateFile('/var/sensorTool/www/preswitch.php', vhttpResult) 

#sensorSwitches()
 
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
