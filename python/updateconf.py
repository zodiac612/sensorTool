#!/usr/bin/python
import ConfigParser, sys, ast
from string import find
import base64
import hashlib

sPathToConfig = '/var/sensorTool/www/dynamic.conf'
config = ConfigParser.RawConfigParser()
config.read(sPathToConfig)

#print '######'
#print sys.argv[1]
dictResponse = ast.literal_eval(str(base64.b64decode(sys.argv[1])))
#print dictResponse 
#print '######'
#print config
vSave = False

for vName in dictResponse:
    vSection = vName[0:(find(vName,  '_'))]
    #vName = vName
    vValue= dictResponse[vName]
    
    if vValue == 'True' or vValue == 'False':
        if config.getboolean(vSection, vName):
            if vValue == 'False':
                #print config.get(vSection, vName) + ' => False'
                config.set(vSection, vName, False)
                vSave = True
        else:
            if vValue == 'True':
                #print config.get(vSection, vName,) + ' => True'
                config.set(vSection, vName, True)
                vSave = True
    
#try:
#    if relais_config.getfloat('Sensor0', 'threshold_high_humidity') != float(vValues):
#        print relais_config.get('Sensor0', 'threshold_high_humidity') + ' => ' + str(float(vValues))
#        relais_config.set('Sensor0', 'threshold_high_humidity', vValues)
#        vSave = True
#except:
#    relais_config.set('Sensor0', 'threshold_high_humidity', vValues)
#    vSave = True
            
# The config-file needs to be chmod 777 if a php skript starts this operation
if vSave:
    with open(str(sPathToConfig), 'wb') as configfile:
        config.write(configfile) 
    
