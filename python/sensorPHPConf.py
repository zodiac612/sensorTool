#!/usr/bin/python
# -*- coding: latin-1 -*-

import ConfigParser
from sensorThreads import threadCreateFile #ok

def sensorPHPConf(vVerbose='start'):
    PathToSwitchesConfig='/home/pi/sensorTool/switches.conf'
    PathToWebradioConfig='/home/pi/sensorTool/webradio.conf'
    
    config = ConfigParser.ConfigParser()
    config.read(PathToSwitchesConfig)

    dictSwitches = {}
    dictGroups = {}
    dictGroups2 = {}
    countGroups2 = 0
    countSwitches = 0
    countSwitchGroups = 0
    for vSec in config.sections():
        if vSec[:5] == 'Group':
            dictGroup = {}
            dictGroup['group'] = vSec
            dictGroup['switchgroup'] = config.get(vSec,  'switchgroup')
            try: dictGroup['slideshow'] =  config.getboolean(vSec,  'slideshow')
            except: dictGroup['slideshow'] =  False       
            try: dictGroup['OnAndOff'] =  config.getboolean(vSec,  'OnAndOff')
            except: dictGroup['OnAndOff'] =  True 
            dictGroups[countSwitchGroups] = dictGroup
            countSwitchGroups = countSwitchGroups + 1
        elif vSec[:6] == 'Switch':
            dictSwitch = {}
            dictSwitch['switch'] = vSec
            dictSwitch['protocol'] =  config.get(vSec,  'protocol')
            dictSwitch['name'] =  config.get(vSec,  'name')
            dictSwitch['id'] =  config.getint(vSec,  'id')
            try: dictSwitch['unit'] =  config.getint(vSec,  'unit')
            except:  dictSwitch['unit'] =  None
            dictSwitch['group'] =  config.get(vSec,  'group')
            if not config.get(vSec,  'group') in dictGroups2 :
                dictGroups2[config.get(vSec,  'group')] = countGroups2
                countGroups2 = countGroups2 + 1
            try: dictSwitch['switchgroup'] = config.get(vSec,  'switchgroup')
            except: dictSwitch['switchgroup'] = None
            try: dictSwitch['alarm'] =  config.getboolean(vSec,  'alarm')
            except: dictSwitch['alarm'] =  False
            try: dictSwitch['slideshow'] =  config.getboolean(vSec,  'slideshow')
            except: dictSwitch['slideshow'] =  False
            try: dictSwitch['OnAndOff'] =  config.getboolean(vSec,  'OnAndOff')
            except: dictSwitch['OnAndOff'] =  True      
            dictSwitches[countSwitches] = dictSwitch
            countSwitches = countSwitches + 1
            
    config = None
    
    config = ConfigParser.ConfigParser()
    config.read(PathToWebradioConfig)
    
    dictWebradios = {}
    countWR = 0
    for vSec in config.sections():
        dictWebradio = {}
        dictWebradio['sender'] = vSec
        dictWebradio['name'] =  config.get(vSec,  'name')
        dictWebradio['preset'] =  config.get(vSec,  'preset')
        dictWebradio['volumeM'] =  config.getint(vSec,  'volumeM')
        dictWebradio['volumeS'] =  config.getint(vSec,  'volumeS')
        try: dictWebradio['slideshow'] =  config.getboolean(vSec,  'slideshow')
        except: dictWebradio['slideshow'] =  False
        try: dictWebradio['index'] =  config.getboolean(vSec,  'index')
        except: dictWebradio['index'] =  False            
        dictWebradios[countWR] = dictWebradio
        countWR = countWR + 1
    
    vhttpResult = ''
#    vhttpResult += '<?php\n'
    vhttpResult += 'define(\'SENSORTOOLSERVER\', \'raspberrypi3\');\n'
    vhttpResult += '$vtop_menue = \'rpidisplay\';\n'
    vhttpResult += '\n'
    for vW in dictWebradios:
        vhttpResult += '$arrWebradio[] = array ( \"'
        vhttpResult += str(vW)
        vhttpResult += '\", \"'
        vhttpResult += str(dictWebradios[vW]['sender'])
        vhttpResult += '\", \"'
        vhttpResult += str(dictWebradios[vW]['name'])
        vhttpResult += '\", \"'
        vhttpResult += str(dictWebradios[vW]['preset'])
        vhttpResult += '\", '
        vhttpResult += str(dictWebradios[vW]['volumeM'])
        vhttpResult += ', '
        vhttpResult += str(dictWebradios[vW]['volumeS'])
        vhttpResult +=', '
        vhttpResult += str(dictWebradios[vW]['index'])
        vhttpResult += ', '
        vhttpResult += str(dictWebradios[vW]['slideshow'])
        vhttpResult += ');\n'

    vhttpResult += '\n'
    for vS in dictGroups:
        vhttpResult += '$arrSwitchGroups[] = array ( \"'
        vhttpResult += str(vS)
        vhttpResult += '\", \"'
        vhttpResult += str(dictSwitches[vS]['group'])
        vhttpResult += '\", \"'
        vhttpResult += str(dictGroups[vS]['switchgroup'])
        vhttpResult += '\", '
        vhttpResult += str(dictGroups[vS]['slideshow'])
        vhttpResult += ', '
        vhttpResult += str(dictGroups[vS]['OnAndOff'])        
        vhttpResult +=  ');\n'

    vhttpResult += '\n'
    iii = 0
    for iii in range(countGroups2):
        vhttpResult += '$arrSwitchTopicGroups[] = array ( \"'
        for vS2 in dictGroups2:
            if iii == dictGroups2[vS2]:
                vhttpResult += str(iii)
                vhttpResult += '\", \"'
                vhttpResult += str(vS2)
                vhttpResult +=  '\");\n'

    vhttpResult += '\n'
    vCSVResult = ''
    for vS in dictSwitches:
        vhttpResult += '$arrSwitches[] = array ( \"'
        vhttpResult += str(vS)
        vhttpResult += '\", \"'
        vhttpResult += str(dictSwitches[vS]['switch']) 
        vhttpResult += '\", \"'
        vhttpResult += str(dictSwitches[vS]['name'])
        vhttpResult += '\", \"'
        vhttpResult += str(dictSwitches[vS]['protocol'])
        vhttpResult += '\", '
        vhttpResult += str(dictSwitches[vS]['id'])
        vhttpResult += ', '
        if dictSwitches[vS]['unit'] is not None:
            vhttpResult += str(dictSwitches[vS]['unit'])
        else:
            vhttpResult += '\"'
            vhttpResult += str(dictSwitches[vS]['unit'])
            vhttpResult += '\"'
        vhttpResult += ', \"'
        vhttpResult += str(dictSwitches[vS]['group'])
        vhttpResult += '\", \"'
        vhttpResult += str(dictSwitches[vS]['switchgroup'])
        vhttpResult += '\", '
        vhttpResult += str(dictSwitches[vS]['alarm'])
        vhttpResult += ', '
        vhttpResult += str(dictSwitches[vS]['slideshow'])
        vhttpResult += ', '
        vhttpResult += str(dictSwitches[vS]['OnAndOff'])        
        vhttpResult +=  ');\n'
        
        vCSVResult += str(vS)
        vCSVResult += ';'
        vCSVResult += str(dictSwitches[vS]['switch']) 
        vCSVResult += ';0;\n'
    vhttpResult += '\n'
#    vhttpResult += '?>\n'

    #print vhttpResult
    threadCreateFile('/var/sensorTool/www/conf.php', vhttpResult) 
    threadCreateFile('/var/sensorTool/www/switchstate.csv', vCSVResult,  'csv') 

#sensorPHPConf()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
