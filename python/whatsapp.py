#coding: utf-8
import os

def sendWhatsApp(vMobile, vMessageText):
    os.system("/home/pi/yowsup/yowsup-cli demos -s "+vMobile+" \""+vMessageText+ "\" -c /home/pi/yowsup/config")
    
def sendWhatsApps(vMobile, vMessageText):
    for iMobile in vMobile:
        sendWhatsApp(vMobile[iMobile], vMessageText)