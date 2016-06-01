#!/usr/bin/python
# -*- coding: latin-1 -*-
#testskript fuer httpservice

# include libraries -----------------------------------------------------------

import time, datetime # time functions
import requests # library for sending data over http
import httpservice # for rt service
import ast
import ConfigParser
import base64 
from string import replace
from sensorCrypt import sensorCrypt

# constants -------------------------------------------------------------------
config = ConfigParser.ConfigParser()
config.read('/home/pi/sensorTool/sensorTool.conf')

sCrypt = sensorCrypt(config.get('global', 'cryptkey'))
INTERVAL = 5                     # secs
SERVER = "localhost"    # cloud server ip/dns name
DEVICE_ID = "1"                    # my cloud user name
PASSWORD = "x"                    # my cloud password
HTTP_TIMEOUT = 1                # secs

# init  -----------------------------------------------------------------------

refreshTime = time.time() + INTERVAL;

# loop ------------------------------------------------------------------------

while True: 

    # every 10 seconds, try to send data to servers
    if time.time() > refreshTime:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        refreshTime = time.time() + INTERVAL;
        
        #try:
        r=requests.get( "http://"+SERVER+":6666")
        rtext = r.text[1:len(r.text)-1]
        print '######'
        print rtext
        print '######'
        vR = sCrypt.Decrypt(rtext)
        print vR
        dictResponse = {}
        dictResponse = ast.literal_eval(str(vR))
        for vKey in dictResponse:
            print str(vKey) + ': ' + str(dictResponse[vKey])
            
        #except: 
            #pass

    # sleep 100ms
    time.sleep(0.1)
