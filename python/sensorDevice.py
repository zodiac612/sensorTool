#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime

class moduleDevice(object):
    def __init__(self,   iActiveValue):
        self.__ListValue = list()
        self.__Value = None
        self.__iActiveValue = iActiveValue
            
    def SetModuleStatus(self, sActive):
        self.__Value = sActive
        iValue = 0
        if self.__Value:
            iValue = self.__iActiveValue
        self.__ListValue.append(iValue)
        
    def SetModuleValue(self, fValue):
        self.__Value = fValue
        self.__ListValue.append(self.__Value)        
    
    def IsActive(self):
        if self.__Value is None:
            return False
        else:
            return self.__Value 

    def GetActualValue(self):
        return self.__Value
        
    def GetListValue(self):
        return self.__ListValue     

    def GetCSVInfo(self,  sName):
        result = str(sName) + ';';
        result += str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[11:16] + ';';
        result += str(str(self.__Value)) + ';';
        return result

    def GetHttpTable(self,  sName):
        result = 'echo "'   
        result += '<DIV class=\\"sensor\\"><TABLE class=\\"sensor\\">'
        result += '<TR>'
        result += '<TD class=\\"sensorlabel\\"><strong>' + sName + '</strong></TD>'
        result += '<TD class=\\"sensor\\">' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))[11:19] + '</TD>'
        if self.__Value is not None:
            classAddOn = ''
            if self.__Value:
                classAddOn = 'Green'
            result += '<TD class=\\"sensor'+classAddOn+'\\">' + str(self.__Value) + '</TD>'
        else:
            result += '<TD class=\\"leer\\"><BR /></TD>'   
        result += '</TR>' 
        
        result += '</TABLE></DIV>' 
        result += '\\n";\n' 
          
        return result

#class sensorDevice(object):
#    def __init__(self,  sName):
#        self.__name = sName
#        self.__ListTime = list()
#        self.__ListT = list()
#        self.__ListActive = list()
#        self.__time = None
#        self.__Active = None
#        self.__T = None
#            
#    def SetSensorData(self, sActive):
#        #print 'SetSensorData'
#        #print vLine
#        self.__Active = sActive
#        sValue = 0
#        if sActive:
#            sValue = 40
#        self.__T = sValue
#        self.__ListT.append(self.__T)
#        self.__time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#        self.__ListTime.append(self.__time)
#
#    def GetName(self):
#        return self.__name
#
#    def GetListT(self):
#        return self.__ListT
#
#    def GetListTime(self):
#        return self.__ListTime
#        
#    def GetListActive(self):
#        return self.__ListActive     
#
#    def GetHttpTable(self, bheader=True):
#        result = 'echo "'   
#        result += '<DIV class=\\"sensor\\"><TABLE class=\\"sensor\\">'
#        result += '<TR>'
#        result += '<TD class=\\"sensorlabel\\"><strong>' + self.__name + '</strong></TD>'
#        result += '<TD class=\\"sensor\\">' + str(self.__time)[11:19] + '</TD>'
#        if self.__Active is not None:
#            classAddOn = ''
#            if self.__Active:
#                classAddOn = 'Green'
#            result += '<TD class=\\"sensor'+classAddOn+'\\">' + str(self.__Active) + '</TD>'
#        else:
#            result += '<TD class=\\"leer\\"><BR /></TD>'   
##        if self.__T is not None:
##            result += '<TD class=\\"tx35dth\\">' + str(self.__T) + '%</TD>'
##        else:
##            result += '<TD class=\\"leer\\"><BR /></TD>'
#        result += '</TR>' 
#        
#        result += '</TABLE></DIV>' 
#        result += '\\n";\n' 
#          
#        return result

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
