#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
class fritzActor(object):
        def __init__(self, dictActor):
            self.__id = dictActor['id']
            self.__name = dictActor['name']
            self.__temperature = float(dictActor['T']) / 10
            self.__power = dictActor['mW']
            self.__state = dictActor['state']
            self.__time = dictActor['time']
            self.__temperature_avg = None
            self.__temperature_avg_count = None
            self.__power_avg = None
            self.__power_avg_count = None

        def SetActor(self, vOn):
            command = "/home/pi/sensorTool/sh/fritzbox-smarthome.sh "
            command += str(self.__id)
            if vOn:
                command += " on"  # raw_input("Kommando: ")
            else:
                command += " off"  # raw_input("Kommando: ")
                
#            try:
            handle = os.popen(command)
    #             line = " "
    #             while line:
    #                 line = handle.readline()
    #                 if len(line) > 0:
    #                     dictActor = {}
    #                     dictActor = ast.literal_eval(line)
    #                     if 'id' in dictActor:
    #                         dictActor['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #                         if dictActor['id'] in dictActors:
    #                             dictActors[dictActor['id']].UpdateActorData(dictActor)
    #                         else:
    #                             dictActors[dictActor['id']] = fritzActor(dictActor)
            handle.close()
 #           except:
                #print str(time.time()) + ': Get fritz actor info failed'
                #sH_Log.Add('Get fritz actor info failed')
  #              pass

        def UpdateActorData(self, vLine, vTypeBME280=False):
            # print vLine
            
            boolGo = False
            if 'id' in vLine:
                if vLine['id'] == self.__id:
                    boolGo = True

            if boolGo:
                if 'T' in vLine:
                    vTt = float(vLine['T']) / 10
                    self.__temperature = vTt
                    self.__setTemperatureAvg(vTt)    
                                        
                if 'mW' in vLine:
                    self.__power = vLine['mW']
                    self.__setPowerAvg(vLine['mW'])
                
                if 'time' in vLine:
                    self.__time = vLine['time']
                    
                if 'state' in vLine:
                    self.__state = vLine['state']

                return True
            else:
                return False

        def __setTemperatureAvg(self, vT):
            if self.__temperature_avg_count is None:
                self.__temperature_avg_count = 1
                self.__temperature_avg = vT
            else:
                vCalVal = self.__temperature_avg * self.__temperature_avg_count
                self.__temperature_avg_count = self.__temperature_avg_count + 1
                self.__temperature_avg = ((vCalVal + vT) / self.__temperature_avg_count) 
                
        def __setPowerAvg(self, vmW):
            if self.__power_avg_count is None:
                self.__power_avg_count = 1
                self.__power_avg = vmW
            else:
                vCalVal = self.__power_avg * self.__power_avg_count
                self.__power_avg_count = self.__power_avg_count + 1
                self.__power_avg = ((vCalVal + vmW) / self.__power_avg_count)

        def GetID(self):
            return self.__id

        def GetName(self):
            return self.__name
        
        def GetT(self):
            return self.__temperature
        
        def GetTAvg(self):
            vResult = self.__temperature_avg
            if self.__temperature_avg is not None:
                vResult = round(self.__temperature_avg, 2)
            return vResult          
        
        def GetPower(self):
            return (float(self.__power) / 1000)
          
        def GetPowerAvg(self):
            vResult = self.__power_avg
            if self.__power_avg is not None:
                vResult = round(float(self.__power_avg) / 1000, 3)
            return vResult         
        
        def GetTime(self):
            return self.__time
        
        def GetMessage(self):
            return self.__message
        
        def GetInfo(self, csv=True, lacrosse=False):
            result = ''
            if csv:
                if lacrosse:
                    vDict = {}
                    vDict['name'] = self.__name
                    vDict['time'] = self.__time
                    vDict['state'] = self.__state
                    vDict['mW'] = self.__power
                    vDict['T'] = self.__temperature
                    vDict['id'] = self.__id
                    result = vDict
                else:
                    result = str(self.__name) + ';'
                    result += str(self.__state) + ';'
                    result += str(self.__time)[11:19] + ';'
                    result += str(self.__temperature) + ';'
                    result += str(self.GetTAvg()) + ';'
                    result += str(self.GetPower()) + ';'
                    result += str(self.GetPowerAvg()()) + ';'

            else:
                result = str(self.__name) + ': '
                result += str(self.__state) + ': '
                result += str(self.__temperature) + 'C; '
                if self.__temperature_avg is not None:
                    result += str(self.GetTAvg()) + 'Cavg; '
                result += str(self.GetPower()) + 'W; '
                if self.__power_avg is not None:
                    result += str(self.GetPowerAvg()) + 'Wavg '
                result += '[' + str(self.__time)[11:19] + ']'
               
            return result
        
        def GetHttpTable(self, bheader=True):
            result = 'echo "'
            result += '<DIV class=\\"fritzactor\\"><TABLE class=\\"fritzactor\\"><TR>'
            result += '<TD class=\\"fritzactorlabel\\"><strong>' + str(self.__name) + '</strong></TD>'
            result += '<TD class=\\"fritzactor\\">state</TD>'
            result += '<TD class=\\"fritzactor\\">T</TD>'
            result += '<TD class=\\"fritzactor\\">W</TD>'
            result += '</TR><TR>'
            result += '<TD class=\\"fritzactor\\">' + str(self.__time)[11:19] + '</TD>'
            result += '<TD class=\\"fritzactor\\">' + str(self.__state) + '</TD>'
            result += '<TD class=\\"fritzactor\\">' + str(self.__temperature) + '</TD>'
            result += '<TD class=\\"fritzactor\\">' + str(self.GetPower()) + '</TD>'
            result += '</TR><TR>'
            result += '<TD class=\\"fritzactor\\">avg</TD>'
            result += '<TD class=\\"leer\\"><BR /></TD>'
            result += '<TD class=\\"fritzactor\\">' + str(self.GetTAvg()) + '</TD>'
            result += '<TD class=\\"fritzactor\\">' + str(self.GetPowerAvg()) + '</TD>'
            result += '</TR></TABLE></DIV>'
            result += '\\n";\n'
            return result

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
