#!/usr/bin/python
# -*- coding: latin-1 -*-

import gpio
from time import sleep

class sensorLight:
    def __init__(self, gpio_int = 26):
        self.__Leuchte =  gpio.GPIOout(gpio_int)

    def activate(self, boolLeuchte):
        return self.SetLeuchte(True, boolLeuchte)

    def deactivate(self, boolLeuchte):
        return self.SetLeuchte(False, boolLeuchte)
    
    def SetLeuchte(self, LeuchteAn, boolLeuchte):
        boolL = boolLeuchte
        if LeuchteAn:
            iI = 0
            while iI < 3:
                # print 'an' + str(iI)
                self.__Leuchte.on()
                sleep(0.1)
                self.__Leuchte.off()
                sleep(0.1)
                iI = iI + 1
            # 1 Konstant an
            # 2 Pulse schnell
            # 3 Pulse langsam
            boolL = True
        else:
            iI = 0
            while iI < 5:
                # print 'aus' + str(iI)
                self.__Leuchte.on()
                sleep(0.1)
                self.__Leuchte.off()
                sleep(0.1)
                iI = iI + 1
            # 4 Lauf links langsam
            # 5 Lauf rechts langsam
            # 6 Lauf links schnell
            # 7 Lauf links rechts
            # 8 Aus
            boolL = False
        return boolL
                           
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
