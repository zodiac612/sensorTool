#!/usr/bin/python
# -*- coding: latin-1 -*-
import math
class tx35dth(object):
        def __init__(self, dictSensor):
            self.__hexCode = dictSensor['hex']
            self.__bme280 = dictSensor['bme280']
            self.__name = dictSensor['name']
            self.__message = ''
            self.__message_org = dictSensor['message']
            self.__delta_message = ''
            self.__delta_message_org = dictSensor['delta_message']            

            self.__bool_delta_RH = False
            if 'delta_humidity' in dictSensor:
                self.__delta_humidity = dictSensor['delta_humidity']
                self.__bool_delta_RH = True

            self.__bool_delta_T = False
            if 'delta_temperature' in dictSensor:
                self.__delta_temperature = dictSensor['delta_temperature']
                self.__bool_delta_T = True            
            
            self.__bool_low_RH = False
            if 'threshold_low_humidity' in dictSensor:
                self.__threshold_low_humidity = dictSensor['threshold_low_humidity']
                self.__bool_low_RH = True

            self.__bool_low_T = False
            if 'threshold_low_temperature' in dictSensor:
                self.__threshold_low_temperature = dictSensor['threshold_low_temperature']
                self.__bool_low_T = True

            self.__bool_high_RH = False
            if 'threshold_high_humidity' in dictSensor:
                self.__threshold_high_humidity = dictSensor['threshold_high_humidity']
                self.__bool_high_RH = True

            self.__bool_high_T = False
            if 'threshold_high_temperature' in dictSensor:
                self.__threshold_high_temperature = dictSensor['threshold_high_temperature']
                self.__bool_high_T = True
                
            if 'fritzactor' in dictSensor:
                self.__fritzactor = dictSensor['fritzactor']
            else:
                self.__fritzactor = None
                
            self.__trigger_count = dictSensor['trigger_count']
            self.__ActTriggerLow = 0
            self.__ActTriggerHigh = 0
            self.__delta_counter = 0
            self.__temperature = None
            self.__humidity = None
            self.__pressure = None
            self.__time = None
            self.__valueT = False
            self.__valueRH = False
            self.__valuePA = False
            self.__sendMessage = True
            self.__mobiles = dictSensor['mobiles']
            self.__taupunkt = None
            self.__absolutefeuchte = None

            self.__delta_stop_trigger = 2
            self.__delta_stop_counter = 0
            self.__last_T_exists = False               
            self.__last_temperature = 0.0
            self.__last_RH_exists = False
            self.__last_humidity = 0.0
            self.__last_time = ''
            self.__humidity_count = None
            self.__temperature_count = None
            self.__humidity_avg = None
            self.__temperature_avg = None            
#                self.__CompareValuesPresent = false
            self.__StateThreshold = 'g' # y, r
            self.__StateDelta = 'g' # y, r
            self.__ListTime = list()
            self.__ListT = list()
            self.__ListRH = list()
            self.__ListPa = list()

        def __setTemperatureAvg(self, vT):
            if self.__temperature_count is None:
                self.__temperature_count = 1
                self.__temperature_avg = vT
            else:
                vCalVal = self.__temperature_avg * self.__temperature_count
                self.__temperature_count = self.__temperature_count + 1
                self.__temperature_avg = ((vCalVal + vT) / self.__temperature_count) 
                
        def __setHumidityAvg(self, vRH):
            if self.__humidity_count is None:
                self.__humidity_count = 1
                self.__humidity_avg = vRH
            else:
                vCalVal = self.__humidity_avg * self.__humidity_count
                self.__humidity_count = self.__humidity_count + 1
                self.__humidity_avg = ((vCalVal + vRH) / self.__humidity_count)
                
        def SetSensorData(self, vLine, vTypeBME280=False):
            #print 'SetSensorData'
            #print vLine
            
            boolGo = False
            if 'ID' in vLine:
                if vLine['ID'] == self.__hexCode:
                    boolGo = True
            elif vTypeBME280:
                boolGo = True
                
            if boolGo:
                if 'T' in vLine:
                    if self.__valueT == False:
                        self.__valueT = True
                    else:
                        self.__last_T_exists = True
                        self.__last_temperature = self.__temperature
                    self.__temperature = vLine['T']
                    self.__setTemperatureAvg(vLine['T'])
                    self.__ListT.append(self.__temperature)     
                    #print 'ListT: ' + str(self.__ListT)
                
                if 'RH' in vLine:
                    if vLine['RH'] > 0:
                        if self.__valueRH == False :
                            self.__valueRH = True
                        else:
                            self.__last_RH_exists = True
                            self.__last_humidity = self.__humidity
                        self.__humidity = vLine['RH']
                        self.__setHumidityAvg(vLine['RH'])
                        self.__ListRH.append(self.__humidity)
                        #print 'ListRH: ' + str(self.__ListRH)
                
                if 'Time' in vLine:
                    self.__last_time = self.__time
                    self.__time = vLine['Time']
                    self.__ListTime.append(self.__time)
                    #print 'ListTime: ' + str(self.__ListTime)

                if 'hPa' in vLine:
                    self.__pressure = vLine['hPa']
                    self.__valuePA = True   
                
                self.__CalculateAbsoluteHumidity()
                                
                return True
            else:
                return False

        def __CalculateAbsoluteHumidity(self):
            # http://www.wetterochs.de/wetter/feuchte.html
            vAbsoluteFeuchte = False
            
            if self.__valueT and self.__valueRH:
                
                vT = float(self.__temperature)
                vRH = float(self.__humidity)

                # print str(self.__name) + ' # ' + str(vT) + ' # ' + str(vRH) 
            
                # Temperatur in Kelvin
                vTK = vT + 273.15
                
                # Universelle Gaskonstante J/(kmol*K)
                vRStar = 8314.3
                # Molekulargewicht des Wasserdampfes kg/kmol
                vMw = 18.016
                
                # ???
                vConstX = 6.1078
                
                # Variablen fuer Taupunkt ueber Wasser, Temperatur groesser gleich und unter 0 
                vA = 7.5
                vB = 237.3
                if vT < 0.0:
                    vA = 7.6
                    vB = 240.7
                
                #vExp1 = (vA + vT) / (vB + vT)
                # Saettigungsdampfdruck in hPa                
                vSDD = vConstX * (10 ** ((vA * vT) / (vB + vT)))
                # Dampfdruck in hPa
                vDD = vRH / 100 * vSDD
                # Taupunkttemperatur in grad Celsius
                vV = math.log10((vDD / vConstX))
                vTauPunkt = (vB * vV) / (vA - vV)
                self.__taupunkt = vTauPunkt
                vAbsoluteFeuchte = (10 ** 5) * (vMw / vRStar) * (vDD / vTK)
                self.__absolutefeuchte = vAbsoluteFeuchte 
#            return vAbsoluteFeuchte
        
        def GetListT(self):
            return self.__ListT

        def GetListTime(self):
            return self.__ListTime

        def GetListRH(self):
            return self.__ListRH

        def GetListPa(self):
            return self.__ListPa
       
        def GetHex(self):
            return self.__hexCode

        def GetBME(self):
            return self.__bme280  #
        
        def GetT(self):
            return self.__temperature
        
        def GetRH(self):
            return self.__humidity
        
        def GetPA(self):
            return self.__pressure
        
        def GetTAvg(self):
            return self.__temperature_avg            
        
        def GetRHAvg(self):
            return self.__humidity_avg
        
        def GetTime(self):
            return self.__time

        def GetFritzActor(self):
            return self.__fritzactor
        
        def GetTriggerCount(self):
            return self.__trigger_count 
        
        def GetSensor(self):
            return self.__name
        
        def GetMessage(self):
            return self.__message
        
        def SetSendMessage(self, vBool=True):
            self.__sendMessage = vBool
            
        def GetSendMessage(self):
            return self.__sendMessage 
        
        def GetDeltaCounter(self):
            return self.__delta_counter
        
        def SetDeltaCounter(self, iValue):
            self.__delta_counter = iValue
            
        def SetThresholdHighHumidity(self, fValue):
            # print 'tx35dth: ' + str(fValue)
            self.__threshold_high_humidity = fValue
            self.__bool_high_RH = True
            
        def GetThresholdHighHumidity(self):
            if self.__bool_high_RH: 
                return self.__threshold_high_humidity
            else:
                return False
        
        def SetThresholdLowTemperature(self, fValue):
            # print 'tx35dth: ' + str(fValue)
            self.__threshold_low_temperature = fValue
            self.__bool_low_T = True
            
        def GetThresholdLowTemperature(self):
            if self.__bool_low_T: 
                return self.__threshold_low_temperature
            else:
                return False        
        
        def GetDelta(self):
            result = False
            Tmsg = ''
            RHmsg = ''
            if self.__last_T_exists:
                if self.__bool_delta_T:
                    vDeltaT = self.__temperature - self.__last_temperature
                    # print str(self.__temperature) +' - ' + str(self.__last_temperature) + ' = ' +str(vDeltaT)
                    if abs(vDeltaT) >= self.__delta_temperature:
                        Tmsg += '\n['
                        Tmsg += str(self.__time)[-8:-3]
                        Tmsg += '] '
                        Tmsg += str(self.__temperature)
                        Tmsg += 'C - '
                        Tmsg += str(self.__last_temperature)
                        Tmsg += 'C ['
                        Tmsg += str(self.__last_time)[-8:-3]
                        Tmsg += '] = '
                        Tmsg += str(vDeltaT)
                        result = True
            
            # print str(self.__last_RH_exists) +'#'+ str(self.__bool_delta_RH)            
            if self.__last_RH_exists:
                if self.__bool_delta_RH:
                    vDeltaRH = self.__humidity - self.__last_humidity
                    # print self.__name + str(vDeltaRH) + '#' +str(self.__delta_humidity)+ '#' + str(self.__humidity)+ ' - ' + str(self.__last_humidity)
                    if self.__delta_humidity < 0:
                        if vDeltaRH <= self.__delta_humidity:
                            result = True
                    else:
                        if vDeltaRH >= self.__delta_humidity:
                            result = True
                    
                    RHmsg += '\n['
                    RHmsg += str(self.__time)[-8:-3]
                    RHmsg += '] '
                    RHmsg += str(self.__humidity)
                    RHmsg += '% - '
                    RHmsg += str(self.__last_humidity)
                    RHmsg += '% ['
                    RHmsg += str(self.__last_time)[-8:-3]
                    RHmsg += '] = '
                    RHmsg += str(vDeltaRH)
                        
            if result:
                self.__delta_message = ''
                self.__delta_message += self.__delta_message_org 
                self.__delta_message += Tmsg
                self.__delta_message += RHmsg
                         
            return result
        
        def GetDeltaMessage(self):
            self.__delta_message += '\n['
            self.__delta_message += str(self.__time)[-8:-3]
            self.__delta_message += '] '
            self.__delta_message += str(self.__temperature)
            self.__delta_message += 'C; '                
            self.__delta_message += str(self.__humidity)
            self.__delta_message += '%'
            return self.__delta_message
                
#         def SetActTrigger(self, iInt):
#             self.__ActTriggerLow = iInt
#             
#         def GetActTrigger(self): 
#             return self.__ActTriggerLow
        
        def GetMobiles(self):
            return self.__mobiles       

        def GetThreshold(self):
            result = False
            #Tmsg = ''
            #RHmsg = ''
            
            vBoolHigh = False
            if self.__bool_high_RH and self.__bool_high_T and self.__temperature is not None and self.__humidity is not None:
                if self.__temperature > self.__threshold_high_temperature and self.__humidity > self.__threshold_high_humidity:
                    self.__ActTriggerHigh = self.__ActTriggerHigh + 1
            elif self.__bool_high_RH and self.__bool_high_T == False and self.__humidity is not None:
                if self.__humidity > self.__threshold_high_humidity:
                    self.__ActTriggerHigh = self.__ActTriggerHigh + 1
            elif self.__bool_high_RH == False and self.__bool_high_T and self.__temperature is not None:
                if self.__temperature > self.__threshold_high_temperature:
                    self.__ActTriggerHigh = self.__ActTriggerHigh + 1
                    
            vBoolLow = False
            if self.__bool_low_RH and self.__bool_low_T and self.__temperature is not None and self.__humidity is not None:
                if self.__temperature < self.__threshold_low_temperature and self.__humidity < self.__threshold_low_humidity:
                    self.__ActTriggerLow = self.__ActTriggerLow + 1
            elif self.__bool_low_RH and self.__bool_low_T == False and self.__humidity is not None:
                if self.__humidity < self.__threshold_low_humidity:
                    self.__ActTriggerLow = self.__ActTriggerLow + 1
            elif self.__bool_low_RH == False and self.__bool_low_T and self.__temperature is not None:
                if self.__temperature < self.__threshold_low_temperature:
                    self.__ActTriggerLow = self.__ActTriggerLow + 1

            if self.__ActTriggerHigh == 0 and self.__ActTriggerLow == 0:
                self.__StateThreshold = 'g'
            elif self.__ActTriggerHigh <= self.__trigger_count or self.__ActTriggerLow <= self.__trigger_count:
                self.__StateThreshold = 'y'
            else:
                self.__StateThreshold = 'r'
            
            if self.__ActTriggerHigh > self.__trigger_count:
                vBoolHigh = True
                self.__ActTriggerHigh = 0
            
            if self.__ActTriggerLow > self.__trigger_count:
                vBoolLow = True
                self.__ActTriggerLow = 0

            if vBoolHigh or vBoolLow:
                result = True
            
            if result:
                self.__message = ''
                self.__message += self.__message_org
                self.__message += '\n['
                self.__message += str(self.__time)[-8:-3]
                self.__message += '] '
                self.__message += str(self.__temperature)
                self.__message += 'C; '                
                self.__message += str(self.__humidity)
                self.__message += '%'
                
            # print str(self.__name) + ' High:' + str(self.__ActTriggerHigh) + ' Low:' + str(self.__ActTriggerLow) + ' result: ' + str(result)
            return result

        def GetInfo(self, csv=True, lacrosse=False):
            result = ''
            if csv:
                if lacrosse:
                    vSensor = {}
                    vSensor['Sensor'] = self.__name
                    vSensor['Time'] = self.__time
                    vSensor['RH'] = self.__humidity
                    vSensor['ID'] = self.__hexCode
                    vSensor['T'] = self.__temperature
                    if self.__bme280:
                        vSensor['HPA'] = self.__pressure

                    result = vSensor
                else:
                    result = str(self.__name) + ';'
                    result = result + str(self.__time)[11:16] + ';'
                    result = result + str(self.__temperature) + ';'
                    result = result + str(self.__humidity) + ';'
                    if self.__bme280:
                        result = result + str(self.__pressure) + ';'
            else:
                result = str(self.__name) + ': '
                result += str(self.__temperature) + 'C; '
            if self.__temperature_avg is not None:
                result += str(round(float(self.__temperature_avg), 2)) + 'Cavg; '
                if self.__humidity is not None:
                    result += str(self.__humidity) + '%; '
                    result += str(round(float(self.__humidity_avg), 2)) + ' %avg; '
                
                if self.__bme280:
                    result = result + str(self.__pressure) + 'hPa; '
                
                result = result + '[' + str(self.__time)[11:16] + ']'
               
            return result
        
        def GetDebugInfo(self):
            result = ''
            if self.__bme280:
                result += str(self.__name) + ' [bme280]:\n'
            else:
                result += str(self.__name) + ' [' + str(self.__hexCode) + ']:\n'

                # DELTA
                if self.__bool_delta_T:
                    result += ' self.__delta_temperature: ' + str(self.__delta_temperature) + '\n'
                else:
                    result += ' self.__delta_temperature: ' + str(self.__bool_delta_T) + '\n'
                
                if self.__bool_delta_RH:
                    result += ' self.__delta_humidity: ' + str(self.__delta_humidity) + '\n'
                else:
                    result += ' self.__delta_humidity: ' + str(self.__bool_delta_RH) + '\n'
                result += ' self.__delta_message: ' + str(self.__delta_message) + '\n'
                result += ' self.__delta_message_org: ' + str(self.__delta_message_org) + '\n'                    
                    
                # Threshold
                if self.__bool_low_T:
                    result += ' self.__threshold_low_temperature: ' + str(self.__threshold_low_temperature) + '\n'
                else:
                    result += ' self.__threshold_low_temperature: ' + str(self.__bool_low_T) + '\n'

                if self.__bool_high_T:
                    result += ' self.__threshold_high_temperature: ' + str(self.__threshold_high_temperature) + '\n'
                else:
                    result += ' self.__threshold_high_temperature: ' + str(self.__bool_high_T) + '\n'                    

                if self.__bool_low_RH:
                    result += ' self.__threshold_low_humidity: ' + str(self.__threshold_low_humidity) + '\n'
                else:
                    result += ' self.__threshold_low_humidity: ' + str(self.__bool_low_RH) + '\n'

                if self.__bool_high_RH:
                    result += ' self.__threshold_high_humidity: ' + str(self.__threshold_high_humidity) + '\n'
                else:
                    result += ' self.__threshold_high_humidity: ' + str(self.__bool_high_RH) + '\n' 
                result += ' self.__message: ' + str(self.__message) + '\n'
                result += ' self.__message_org: ' + str(self.__message_org) + '\n'                           
                
                result += ' self.__trigger_count: ' + str(self.__trigger_count) + '\n'
                result += ' self.__ActTriggerLow: ' + str(self.__ActTriggerLow) + '\n'
                result += ' self.__ActTriggerHigh: ' + str(self.__ActTriggerHigh) + '\n'
                result += ' self.__delta_counter: ' + str(self.__delta_counter) + '\n'
                result += ' self.__temperature: ' + str(self.__temperature) + '\n'
                result += ' self.__humidity: ' + str(self.__humidity) + '\n'
                result += ' self.__pressure: ' + str(self.__pressure) + '\n'
                result += ' self.__time: ' + str(self.__time) + '\n'
                result += ' self.__valueT: ' + str(self.__valueT) + '\n'
                result += ' self.__valueRH: ' + str(self.__valueRH) + '\n'
                result += ' self.__valuePA: ' + str(self.__valuePA) + '\n'
                result += ' self.__sendMessage: ' + str(self.__sendMessage) + '\n'
                result += ' self.__mobiles: ' + str(self.__mobiles) + '\n'
                result += ' self.__taupunkt: ' + str(self.__taupunkt) + '\n'
                result += ' self.__absolutefeuchte: ' + str(self.__absolutefeuchte) + '\n'
                result += ' self.__delta_stop_trigger: ' + str(self.__delta_stop_trigger) + '\n'
                result += ' self.__delta_stop_counter: ' + str(self.__delta_stop_counter) + '\n'
                result += ' self.__last_T_exists: ' + str(self.__last_T_exists) + '\n'
                result += ' self.__last_temperature: ' + str(self.__last_temperature) + '\n'
                result += ' self.__last_RH_exists: ' + str(self.__last_RH_exists) + '\n'
                result += ' self.__last_humidity: ' + str(self.__last_humidity) + '\n'
                result += ' self.__last_time: ' + str(self.__last_time) + '\n'
                result += ' self.__temperature_count: ' + str(self.__temperature_count) + '\n'
                result += ' self.__humidity_count: ' + str(self.__humidity_count) + '\n'
                result += ' self.__temperature_avg: ' + str(self.__temperature_avg) + '\n'
                result += ' self.__humidity_avg: ' + str(self.__humidity_avg) + '\n'
                # result += ' : ' + str() + '\n'
                    
            return result

        def GetHttpTable(self, bheader=True):
            result = 'echo "'   
            result += '<DIV class=\\"tx35dth\\"><TABLE class=\\"tx35dth\\">'
            if bheader:
                result += '<TR>'
                result += '<TD class=\\"tx35dthlabel\\"><strong>' + self.__name + '</strong></TD>'
                if self.__temperature is not None:
                    result += '<TD class=\\"tx35dth\\">T</TD>'
                else:
                    result += '<TD class=\\"leer\\"><BR /></TD>'
                if self.__humidity is not None:
                    result += '<TD class=\\"tx35dth\\">RH</TD>'
                else:
                    result += '<TD class=\\"leer\\"><BR /></TD>'
                if self.__bme280:            
                    result += '<TD class=\\"tx35dth\\">pa</TD>'
                else:
                    result += '<TD class=\\"leer\\"><BR /></TD>'
                result += '</TR>'
            
            result += '<TR>'
            result += '<TD class=\\"tx35dth\\">' + str(self.__time)[11:19] + '</TD>'
            if self.__temperature is not None:
                result += '<TD class=\\"tx35dth\\">' + str(self.__temperature) + 'C</TD>'
            else:
                result += '<TD class=\\"leer\\"><BR /></TD>'                
            if self.__humidity is not None:
                result += '<TD class=\\"tx35dth\\">' + str(self.__humidity) + '%</TD>'
            else:
                result += '<TD class=\\"leer\\"><BR /></TD>'
            if self.__bme280:            
                result += '<TD class=\\"tx35dth\\">' + str(self.__pressure) + '</TD>'
            else:
                result += '<TD class=\\"leer\\"><BR /></TD>'
            result += '</TR>' 
            
            result += '<TR>'
            result += '<TD class=\\"tx35dth\\">AVG</TD>'
            if self.__temperature is not None:
                result += '<TD class=\\"tx35dth\\">' + str(round(self.__temperature_avg, 2)) + 'C</TD>'
            else:
                result += '<TD class=\\"leer\\"><BR /></TD>'                
            if self.__humidity is not None:
                result += '<TD class=\\"tx35dth\\">' + str(round(self.__humidity_avg, 2)) + '%</TD>'
            else:
                result += '<TD class=\\"leer\\"><BR /></TD>'                
            if self.__bme280:            
                result += '<TD class=\\"tx35dth\\"><BR /></TD>'
            else:
                result += '<TD class=\\"leer\\"><BR /></TD>'
            result += '</TR>'
            result += '</TABLE></DIV>' 
            result += '\\n";\n' 
              
            return result

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
