#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime

class sensorDevice(object):
    def __init__(self,  sName):
        self.__name = sName
        self.__ListTime = list()
        self.__ListT = list()
        self.__ListActive = list()
        self.__time = None
        self.__Active = None
        self.__T = None
            
    def SetSensorData(self, sActive):
        #print 'SetSensorData'
        #print vLine
        self.__Active = sActive
        sValue = 0
        if sActive:
            sValue = 40
        self.__T = sValue
        self.__ListT.append(self.__T)
        self.__time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__ListTime.append(self.__time)

    def GetName(self):
        return self.__name

    def GetListT(self):
        return self.__ListT

    def GetListTime(self):
        return self.__ListTime
        
    def GetListActive(self):
        return self.__ListActive     

    def GetHttpTable(self, bheader=True):
        result = 'echo "'   
        result += '<DIV class=\\"sensor\\"><TABLE class=\\"sensor\\">'
        result += '<TR>'
        result += '<TD class=\\"sensorlabel\\"><strong>' + self.__name + '</strong></TD>'
        result += '<TD class=\\"sensor\\">' + str(self.__time)[11:19] + '</TD>'
        if self.__Active is not None:
            classAddOn = ''
            if self.__Active:
                classAddOn = 'Green'
            result += '<TD class=\\"sensor'+classAddOn+'\\">' + str(self.__Active) + '</TD>'
        else:
            result += '<TD class=\\"leer\\"><BR /></TD>'   
#        if self.__T is not None:
#            result += '<TD class=\\"tx35dth\\">' + str(self.__T) + '%</TD>'
#        else:
#            result += '<TD class=\\"leer\\"><BR /></TD>'
        result += '</TR>' 
        
        result += '</TABLE></DIV>' 
        result += '\\n";\n' 
          
        return result

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
