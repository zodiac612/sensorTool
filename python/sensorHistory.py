import time, datetime  # time functions
class sensorHistory(object):
        def __init__(self):
            self.__dictLog = {}
            self.__counterLog = 0

        def Add(self, vLine):
            # print vLine
            self.__counterLog = self.__counterLog + 1
            vNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dictLine = {}
            dictLine['time'] = vNow
            dictLine['text'] = vLine
            self.__dictLog[self.__counterLog] = dictLine
                   
        def GetHttpTable(self, bheader=True):
            result = '<DIV MARGIN=5><TABLE BORDER=1><TR>'
            result += '<TD width=20><BR /></TD>'
            result += '<TD width=100><strong>History</strong></TD>'
            result += '<TD width=200><BR /></TD>'
            result += '</TR>'
            for vKey in self.__dictLog:
                result += '<TR>'
                result += '<TD>' + str(vKey) + '</TD>'
                result += '<TD>' + str(self.__dictLog[vKey]['time']) + '</TD>'
                result += '<TD>' + str(self.__dictLog[vKey]['text']) + '</TD>'
                result += '</TR>'
          
            result += '</TABLE></DIV>' 
            return result

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4