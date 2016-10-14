#!/usr/bin/python
# -*- coding: latin-1 -*-
import datetime  # time functions
import thread 
from sensorThreads import threadCreateFile

class sensorHistory(object):
        def __init__(self, sPathToExport1='',   sPathToExport2='',  sPathToExport3=''):
            self.__dictLog = {}
            self.__counterLog = 0
            self.__sPathToExport3 = sPathToExport3
            self.__sPathToExport2 = sPathToExport2
            self.__sPathToExport1 = sPathToExport1

        def Add(self, vLine):
            # print vLine
            self.__counterLog = self.__counterLog + 1
            vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dictLine = {}
            dictLine['time'] = vNow
            dictLine['text'] = vLine
            self.__dictLog[self.__counterLog] = dictLine
            if self.__sPathToExport1 <> '':
                try:  
                    thread.start_new_thread(threadCreateFile, (self.__sPathToExport1, self.GetHttpLastMessage(),))
                except:
                    pass
            
            if self.__sPathToExport2 <> '':
                try:  
                    thread.start_new_thread(threadCreateFile, (self.__sPathToExport2,  self.GetHttpTable(),))
                except:
                    pass

            if self.__sPathToExport3 <> '':
                try:  
                    thread.start_new_thread(threadCreateFile, (self.__sPathToExport3,  self.GetCSVLastMessage(), 'csv'))
                except:
                    pass
                   
        def GetHttpTable(self):
            result = 'echo "'
            result += '<DIV class=\\"history\\"><TABLE class=\\"history\\"><TR>'
            result += '<TD class=\\"historynr\\"><BR /></TD>'
            result += '<TD class=\\"historylabel\\"><strong>History</strong></TD>'
            result += '<TD class=\\"history\\"><BR /></TD>'
            result += '</TR>'
            for vKey in self.__dictLog:
                result += '<TR>'
                result += '<TD class=\\"historynr\\">' + str(vKey) + '</TD>'
                result += '<TD class=\\"historylabel\\">' + str(self.__dictLog[vKey]['time']) + '</TD>'
                result += '<TD class=\\"history\\">' + str(self.__dictLog[vKey]['text']) + '</TD>'
                result += '</TR>'
            result += '</TABLE></DIV>' 
            result += '\\n";\n'
            return result
        
        def GetHttpLastMessage(self):
            result = 'echo "'
            result += '<DIV class=\\"history\\"><TABLE class=\\"history\\"><TR>'
            result += '<TD class=\\"historynr\\"><BR /></TD>'
            result += '<TD class=\\"historylabel\\"><strong>History</strong></TD>'
            result += '<TD class=\\"history\\"><BR /></TD>'
            result += '</TR><TR>'
            result += '<TD class=\\"historynr\\">' + str(self.__counterLog) + '</TD>'
            result += '<TD class=\\"historylabel\\">' + str(self.__dictLog[self.__counterLog]['time']) + '</TD>'
            result += '<TD class=\\"history\\">' + str(self.__dictLog[self.__counterLog]['text']) + '</TD>'
            result += '</TR></TABLE></DIV>' 
            result += '\\n";\n'
            return result

        def GetCSVLastMessage(self):
            result = str(self.__counterLog) + ';'
            result += str(self.__dictLog[self.__counterLog]['time'])[11:19] + ';'
            result += str(self.__dictLog[self.__counterLog]['text'])[0:80] + ';'
            return result

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
