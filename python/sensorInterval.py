#!/usr/bin/python
# -*- coding: latin-1 -*-

import time

class sensorInterval:
    def __init__(self, dictIntervalle = {}):
        self.__dictIntervalle =  {}
        self.__dictIntervalle =  dictIntervalle

    def isNowInInterval(self):
        vStunde = time.strftime('%H%M')
        vBoolTimeToCount = False
        for vIv in self.__dictIntervalle:
            # print vStunde + '>' + dictIntervalle[vIv]['start'] + ' and ' + vStunde + ' < ' + dictIntervalle[vIv]['stop']
            if vStunde > self.__dictIntervalle[vIv]['start'] and vStunde < self.__dictIntervalle[vIv]['stop'] and time.strftime('%w') != '0':
                vBoolTimeToCount = True
        return vBoolTimeToCount
                           
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
