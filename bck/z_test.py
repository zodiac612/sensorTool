#!/usr/bin/python
# -*- coding: latin-1 -*-
#coding: utf-8
import datetime

def GetCryptPosition():
    vDate1 = datetime.datetime.now().strftime('%d%m')
    vDate2 = datetime.datetime.now().strftime('%Y')
    # print str(vDate1) + '#' + str(vDate2)
    qs0 = querSum(vDate1 + vDate2)
    qs1 = querSum(vDate1)
    qs2 = querSum(vDate2)
    # print str(qs0) + '#' + str(qs1) + '#' + str(qs2)
    variant1 = int(round(qs0/9))
    variant2 = int(round(int(vDate1)/qs1))
    variant3 = int(round(variant2/(variant1+qs1)))
    # print str(variant1) + '#' + str(variant2) + '#' + str(variant3)
    vResult = qs0 + variant1 + variant3
    if vResult > 100:
        vResult = str(vResult)[-2:]
    return vResult

def querSum(vZahl):
    zahlString=str(vZahl)
    querSumme=0
    for zifferBuchstabe in zahlString:
            querSumme=querSumme+int(zifferBuchstabe)
    return querSumme


#command = "../sh/fritzbox-smarthome.sh"
#while (command != "exit"):
vDate1 = datetime.datetime.now().strftime('%d%m')
vDate2 = datetime.datetime.now().strftime('%Y')
print(vDate1 + '#' + vDate2)
print(str(GetCryptPosition()))
print("Ciao, that's it!")
