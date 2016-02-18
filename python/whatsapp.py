#coding: utf-8
import os

def sendWhatsApp(vMobile, vMessageText):
    try:
        os.system("sudo /home/pi/sensorTool/sh/whatsapp.sh "+vMobile+" \""+vMessageText+ "\"")
    #os.system("/root/yowsup/yowsup-cli demos -s "+vMobile+" \""+vMessageText+ "\" -c /root/yowsup/config")
    except:
        print str(time.time()) + ': SendWhatsApp failed {' + vMessageText + ')\n\n'
	    
def sendWhatsApps(vMobile, vMessageText):
    for iMobile in vMobile:
        sendWhatsApp(vMobile[iMobile], vMessageText)
