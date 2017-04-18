from Tkinter import *
from PIL import ImageTk, Image
import glob
import os
import random
#import time
from bosestControl import * 
from functools import partial
import RPi.GPIO as GPIO
import csv
#import gpio

class App:
    def __init__(self, master):
        self.master=master
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(27, GPIO.BOTH, callback=self.Interrupt_event)
        
        self.boolBackLight = False
        self.Wait20sec = False
        self.fadebacklight('on')
        os.system("sudo service pilight stop")
        
        self.boolFirstStart=True
        self.PicH=465
        
        #self.buttonFont='Monospace 12'
        self.buttonFont='Roboto 11'
        #self.buttonWidth=7
        self.buttonWidth=7
        self.buttonPady=8
        self.bgBase='#000000'
        self.bgHighlight='#111111'
        self.dividerFont='Arial 2'
        
        self.framePic=Frame(master, bg=self.bgBase )
        frameMenu1=Frame(master, bg=self.bgBase)
        self.frameMenu2=Frame(master, bg=self.bgBase)
        frameFooter=Frame(master, bg=self.bgHighlight)
        
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(1, weight=1)
        
        self.framePic.grid(row=0, column=0, rowspan=2)
        frameMenu1.grid(row=0, column=1,  sticky=NE)
        #frameMenu1.configure(highlightbackground='#000000', highlightthickness=3)
        self.frameMenu2.grid(row=1, column=1,  sticky=SE)
        frameFooter.grid(row=2, column=0, columnspan=2)
    
        self.Picture=Label(self.framePic, text='Bild', bg=self.bgBase)
        self.Picture.grid(row=0, column=0)
        self.setPicture()
        
        self.frameInFrameMenu2=Frame(self.frameMenu2, bg=self.bgBase)
        self.frameInFrameMenu2.grid(row=0,  column=0)
        Label(self.frameInFrameMenu2,text='sensors', bg=self.bgBase,  fg='green').grid(row=1,column=1)
        self.setSensors()
        
        Footer=Label(frameFooter, text='footer', bg=self.bgBase,  fg='green', font=self.dividerFont)
        Footer.grid(row=0, column=0)
                
        buttonHome = Button (
            frameMenu1,text='Quit',pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=master.quit)
        buttonHome.configure(highlightbackground='#000000', highlightthickness=3)    
        buttonHome.grid(row=0, column=0)

        buttonChange = Button (
            frameMenu1,text="Refresh",fg="green",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=self.DoRefresh)#bg="#333333"
        buttonChange.configure(highlightbackground='#000000', highlightthickness=3)            
        buttonChange.grid(row=0, column=1)

        #dividerline1 = Label(buttonFrameL,bg=self.bgBase,font=self.dividerFont)
        #dividerline1.pack(side=TOP, fill=X)
        #dividerline2 = Label(buttonFrameR,bg=self.bgBase,font=self.dividerFont)
        #dividerline2.pack(side=TOP, fill=X)

        bose1 = Button (
            frameMenu1,text="Radio 8",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=partial(self.webradioControl, "change8"))
        bose1.configure(highlightbackground='#000000', highlightthickness=3)            
        bose1.grid(row=1, column=0)
        bose2 = Button (
            frameMenu1,text="Bayern 3",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=partial(self.webradioControl, "change3"))
        bose2.configure(highlightbackground='#000000', highlightthickness=3)            
        bose2.grid(row=1, column=1)
        
        bose3 = Button (
            frameMenu1,text="Star FM",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=partial(self.webradioControl, "changeStar"))
        bose3.grid(row=2, column=0)
        bose3.configure(highlightbackground='#000000', highlightthickness=3)           
        bose4 = Button (
            frameMenu1,text="Stop",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=partial(self.webradioControl, "stop"))
        bose4.configure(highlightbackground='#000000', highlightthickness=3)            
        bose4.grid(row=2, column=1)
        
        dividerline1 = Label(frameMenu1,bg=self.bgBase,font=self.dividerFont)
        dividerline1.grid(row=3, column=1)
        dividerline2 = Label(frameMenu1,bg=self.bgBase,font=self.dividerFont)
        dividerline2.grid(row=3, column=1)
        
        switch1 = Button (
            frameMenu1,text="Wozi aus",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=partial(self.switchControl, "Woziaus"))
        switch1.configure(highlightbackground='#000000', highlightthickness=3)            
        switch1.grid(row=4, column=0)
        switch2 = Button (
            frameMenu1,text="TV an",pady=self.buttonPady,width=self.buttonWidth,
            font=self.buttonFont,
            command=partial(self.switchControl, "TVan"))
        switch2.configure(highlightbackground='#000000', highlightthickness=3)            
        switch2.grid(row=4, column=1)

        #button = Button (buttonFrameL,text="QUIT",pady=8,fg="red",command=mainFrame.quit)
        #button.pack(side=TOP, fill=X) 

        #hi_there = Button (buttonFrameR,text="Hello",width=7,pady=8,command=self.say_hi)
        #hi_there.pack(side=TOP, fill=X)
        #sleep(2)
        self.boolFirstStart=False

    def DoRefresh(self):
        #print 'pics'
        self.setPicture()
        #print 'sensor'
        self.setSensors()
    
    def say_hi(self):
        print('hi there, everyone!')

    def webradioControl(self, params):
        #print (params)
        #rint (self.boolFirstStart)
        if not self.boolFirstStart:
            #print (params)
            boseControlGUI(params)
        #pass

    def switchControl(self, params):
        bX = False
        switch_list=[]
        if ( params == 'TVan'):
            x = ''
            vProtocol = 'intertechno_switch'
            vID = 12345678
            vUnit = 0
            #vName = TV
            vState = 1
            bX = True
            x = ' ' + vProtocol + ' ' + vID + ' ' + vUnit + ' ' + vState
            switch_list.append(x)
        if( params == 'Woziaus'):
            #vName = TV
            switch_list.append(' intertechno_switch 12345678 0 0') 
            #TV LED
            switch_list.append(' intertechno_switch 12345678 1 0') 
            # Schrank LED
            switch_list.append(' intertechno_switch 12345678 2 0') 
            # AFTV
            switch_list.append(' quigg_gt9000 123456 1 0') 
            #wii
            switch_list.append(' quigg_gt9000 123456 2 0') 
            bX = True

        #print (params)
        #print (x)
        
        
        if bX:
            for vParam in switch_list:
                os.system("sudo /home/pi/sensorTool/sh/pilightservice.sh " + str(vParam))
                sleep(1)
        pass

    def setPicture(self):
        image_list=[]
        for filename in glob.glob('/home/pi/pics/*.JPG'):
            image_list.append(filename)
        listentry=random.randint(0, len(image_list)-1)
        #print listentry
        #print len(image_list)
        image_list[listentry]

        self.imageOrg=Image.open(image_list[listentry])
        [imageWS,imageHS]=self.imageOrg.size
        iFaktor=imageHS/self.PicH
        newImageHS=self.PicH
        newImageWS=int(imageWS/iFaktor)
        self.imageOrg=self.imageOrg.resize((newImageWS,newImageHS), Image.ANTIALIAS)
        self.image1=ImageTk.PhotoImage(self.imageOrg)
        self.Picture.destroy()
        self.Picture=Label(self.framePic, image=self.image1)
        self.Picture.grid(row=0, column=0, rowspan=2)
        #self.Picture.pack(fill=X, expand=YES)

    def setSensors(self):
        framebg='black'
        textfg='green'
        frameline=3
        #tFont='arial-narrow 9'
        tFont='RobotoCondensed 11'
        self.frameInFrameMenu2.destroy()
        self.frameInFrameMenu2=Frame(self.frameMenu2, bg=self.bgBase,  highlightbackground=framebg, highlightthickness=frameline)
        self.frameInFrameMenu2.grid(row=0,  column=0,  sticky=SE)
        #self.frameInFrameMenu2.grid_columnconfigure(0,weight=1)
        sleep (3)

        with open('/var/sensorTool/www/sensor.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')#, quotechar='|')
             
            iRow=0
            iCol=0
            #Label(self.frameInFrameMenu2,text=row[0], bg=self.bgBase,  fg=textfg,  highlightbackground=framebg, highlightthickness=frameline).grid(row=iRow,column=iCol,  sticky=W)
            Label(self.frameInFrameMenu2,text='Name', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=W)
            iCol = iCol + 1
            Label(self.frameInFrameMenu2,text='Zeit|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
            iCol = iCol + 1
            Label(self.frameInFrameMenu2,text='T|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
            iCol = iCol + 1
            Label(self.frameInFrameMenu2,text='RH ', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
            iRow = iRow + 1
            for row in spamreader:
                if row[0]=='Vorgarten' or row[0]=='Terrasse' or row[0]=='Keller':
                    iCol=0
                    #Label(self.frameInFrameMenu2,text=row[0], bg=self.bgBase,  fg=textfg,  highlightbackground=framebg, highlightthickness=frameline).grid(row=iRow,column=iCol,  sticky=W)
                    Label(self.frameInFrameMenu2,text=row[0], bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=W)
                    iCol = iCol + 1
                    Label(self.frameInFrameMenu2,text='|'+row[1]+'|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
                    iCol = iCol + 1
                    Label(self.frameInFrameMenu2,text=row[2]+'|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
                    iCol = iCol + 1
                    Label(self.frameInFrameMenu2,text=row[3]+' ', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
                iRow = iRow + 1

        Label(self.frameInFrameMenu2,text='', bg=self.bgBase,  fg=textfg, font=self.dividerFont).grid(row=iRow,column=0,  columnspan=4)
        iRow = iRow + 1
        iCol=0
        #Label(self.frameInFrameMenu2,text=row[0], bg=self.bgBase,  fg=textfg,  highlightbackground=framebg, highlightthickness=frameline).grid(row=iRow,column=iCol,  sticky=W)
        Label(self.frameInFrameMenu2,text='', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=W)
        iCol = iCol + 1
        Label(self.frameInFrameMenu2,text='', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
        iCol = iCol + 1
        Label(self.frameInFrameMenu2,text='W|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
        iCol = iCol + 1
        Label(self.frameInFrameMenu2,text='x ', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,  sticky=E)
        iRow = iRow + 1
        with open('/var/sensorTool/www/fa.csv', 'rb') as csvfile:
             spamreader = csv.reader(csvfile, delimiter=';')#, quotechar='|')
             #iRow=0
             for row in spamreader:
                iCol=0
                Label(self.frameInFrameMenu2,text=row[0], bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,sticky=W)
                iCol = iCol + 1
                Label(self.frameInFrameMenu2,text='|'+row[1]+'|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,sticky=E)
                iCol = iCol + 1
                Label(self.frameInFrameMenu2,text=row[4]+'|', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,sticky=E)
                iCol = iCol + 1               
                Label(self.frameInFrameMenu2,text=row[2]+' ', bg=self.bgBase,  fg=textfg, font=tFont).grid(row=iRow,column=iCol,sticky=E)
                iRow = iRow + 1
        #self.Picture.pack(fill=X, expand=YES) 
 
    def Interrupt_event(self, pin):
        #global MyLabel1
        if GPIO.input(27): # if 27 == 1
            #Motion Detected
            if (not self.boolBackLight and not self.Wait20sec ):
                self.boolBackLight=True
                self.switchBL(0)
                self.fadebacklight('on')
                self.setPicture()
                self.setSensors()
                self.Wait20sec=True
                self.master.after(20000, self.setWait20sec)
                #print("Motion")
        else: # if 27 != 1
            if (self.boolBackLight and not self.Wait20sec ):
                self.boolBackLight=False
                self.fadebacklight('off')
                self.switchBL(1)
                #print("No Motion")
    
    def setWait20sec(self):
        if (self.Wait20sec):
            self.Wait20sec=False
        
    def switchBL(self,  trigger = 0):
        os.system("sudo /home/pi/dev/pi-box/SwitchBacklight.sh " + str(trigger))

    def fadebacklight(self,  trigger = 'on', vBrightness=128):
        if trigger == 'off':
    #        x = 255
            x = vBrightness

            while x >= 0:
                os.system("sudo /home/pi/dev/pi-box/fadeBacklight.sh " + str(x))
                x = x - 25
        elif trigger == 'on':
            os.system("xte -x :0 \"key F5\"")
            x = 0       
    #        while x < 256:
            while x < vBrightness:
                os.system("sudo /home/pi/dev/pi-box/fadeBacklight.sh " + str(x))
                x = x + 10


root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg = '#000000')
#root.overrideredirect(True)
#root.overrideredirect(False)
app = App(root)
root.mainloop()
#root.destroy()
      
#rootwindow = Tk()
#w = Label(rootwindow, text="Hello, world!")
#w.pack()
#rootwindow.mainloop()
