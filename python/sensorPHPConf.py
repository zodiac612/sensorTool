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
    countSwitches = 0
    for vSec in config.sections():
        dictSwitch = {}
        dictSwitch['switch'] = vSec
        dictSwitch['protocol'] =  config.get(vSec,  'protocol')
        dictSwitch['name'] =  config.get(vSec,  'name')
        dictSwitch['id'] =  config.getint(vSec,  'id')
        try: dictSwitch['unit'] =  config.getint(vSec,  'unit')
        except:  dictSwitch['unit'] =  None
        dictSwitch['group'] =  config.get(vSec,  'group')
        try: dictSwitch['switchgroup'] = config.get(vSec,  'switchgroup')
        except: dictSwitch['switchgroup'] = None
        try: dictSwitch['alarm'] =  config.getboolean(vSec,  'alarm')
        except: dictSwitch['alarm'] =  False
        try: dictSwitch['slideshow'] =  config.getboolean(vSec,  'slideshow')
        except: dictSwitch['slideshow'] =  False        
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
        dictWebradio['volume'] =  config.getint(vSec,  'volume')
        dictWebradio['url'] =  config.get(vSec,  'url')
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
        vhttpResult += '\", '
        vhttpResult += str(dictWebradios[vW]['volume'])
        vhttpResult += ', \"'+ str(dictWebradios[vW]['url'])
        vhttpResult +='\", '
        vhttpResult += str(dictWebradios[vW]['index'])
        vhttpResult += ', '
        vhttpResult += str(dictWebradios[vW]['slideshow'])
        vhttpResult += ');\n'

    vhttpResult += '\n'
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
        vhttpResult +=  ');\n'

    vhttpResult += '\n'
#    vhttpResult += '?>\n'

    #print vhttpResult
    threadCreateFile('/var/sensorTool/www/conf.php', vhttpResult) 

sensorPHPConf()
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
