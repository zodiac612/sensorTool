#!/usr/bin/python
import ConfigParser, ast
import base64
import requests
from time import sleep
#import hashlib

def boseControlWeb(base64data):
    dictResponse = ast.literal_eval(str(base64.b64decode(base64data)))
    boseControl(dictResponse)
    
def boseControlGUI(changeOrder):
    #Test
    dictResponse={}
    #print changeOrder
    #base64r8="eyJuYW1lIjogIlJhZGlvIDgiLCAicHJlc2V0IjogIlBSRVNFVF8xIiwgInZvbHVtZU0iOiAiMTAiLCAidm9sdW1lUyI6ICI1IiwgImFjdGlvbiI6ICJSYWRpbyA4IiwgfQ=="
    #base64stop="eyJhY3Rpb24iOiAic3RvcCIsIH0="
    #dictResponse1 = ast.literal_eval(str(base64.b64decode(base64r8)))
    #dictResponse2 = ast.literal_eval(str(base64.b64decode(base64stop)))
    if changeOrder=='change8':
        dictResponse={'volumeM': '10', 'action': 'Radio 8', 'preset': 'PRESET_1', 'name': 'Radio 8', 'volumeS': '5'}
    elif changeOrder=='change3':
        dictResponse={'volumeM': '13', 'action': 'Bayern 3', 'preset': 'PRESET_2', 'name': 'Bayern 3', 'volumeS': '8'}
    elif changeOrder=='changeStar':
        dictResponse={'volumeM': '10', 'action': 'Star FM', 'preset': 'PRESET_3', 'name': 'Star FM', 'volumeS': '5'}
    elif changeOrder=='stop':
        dictResponse={'action': 'stop'}
    else:
        print ('nothing toDo')
    
    #print(dictResponse)

    boseControl(dictResponse)
    
def boseControl(dictResponse):
    sPathToConfig = '/home/pi/sensorTool/bosest.conf'
    config = ConfigParser.RawConfigParser()
    config.read(sPathToConfig)
    MasterIP=config.get('bosest1','IP')
    MasterMAC=config.get('bosest1','MAC')
    Slave1IP=config.get('bosest2','IP')
    Slave1MAC=config.get('bosest2','MAC')
#    strKeyPreset1='<key state="release" sender="Gabbo">PRESET_1</key>'
 #   strKeyPreset2='<key state="release" sender="Gabbo">PRESET_2</key>'
 #   strKeyPreset3='<key state="release" sender="Gabbo">PRESET_3</key>'
    strKeyPower='<key state="press" sender="Gabbo">POWER</key>'
    strZone='<zone master="'+MasterMAC+'"><member ipaddress="'+MasterIP+'">'+MasterMAC+'</member><member ipaddress="'+Slave1IP+'">'+Slave1MAC+'</member></zone>'
    hostM=MasterIP+':8090'
    hostS1=Slave1IP+':8090'

    # Is Master up and running or in Standby
    MasterActive = False
    r=requests.get("http://" + hostM + "/now_playing")
    #print r.text
    try:
        r.text[0:100].index("STANDBY")
    except:
        #print "not found"
        MasterActive=True
    else:
        #print "found"
        pass
        
    print MasterActive    

    headers = {'content-type': 'text/xml'}
    urlVolumeM = 'http://' + hostM + '/volume'
    urlVolumeS = 'http://' + hostS1 + '/volume'
    urlKey = 'http://' + hostM + '/key'
    #urlSelect = 'http://' + hostM + '/select'
    urlSetZone = 'http://' + hostM + '/setZone'

    vStart=False
    vStop=False

    #vParams = ''
    if 'action' in dictResponse:
        if dictResponse['action'] == 'stop' and (MasterActive):# or not MasterNotActive):
            #print 'stop'
            vStop = True
            #Bose Master beenden
        
        elif dictResponse['action'] <> 'stop' and MasterActive:
            #Bose Master Aenderung 
            #print 'Change'
            pass
        
        elif dictResponse['action'] <> 'stop' and not MasterActive:
            #Bose Master start + Zone einrichten
            #print 'start'
            vStart = True

    if vStop:
        r = requests.post(urlKey, data=strKeyPower, headers=headers)
        #print r.text
    else:
        strVolumeM = '<volume>'+dictResponse['volumeM']+'</volume>'
        
        strVolumeS = '<volume>'+dictResponse['volumeS']+'</volume>'
        
        strKeyPreset='<key state="release" sender="Gabbo">'+dictResponse['preset']+'</key>'
         
        #print strKeyPreset
        r = requests.post(urlKey, data=strKeyPreset, headers=headers)
        #print r.text
        
        #print strVolumeM
        r = requests.post(urlVolumeM, data=strVolumeM, headers=headers)
        #print r.text
        
        #print strVolumeS
        r = requests.post(urlVolumeS, data=strVolumeS, headers=headers)
        #print r.text
            
        if vStart:
            #print 'Zone'
            sleep(2)
            r = requests.post(urlSetZone, data=strZone, headers=headers)
            #print r.text    

#boseControlWeb(sys.argv[1])
