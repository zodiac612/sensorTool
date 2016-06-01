#!/usr/bin/python
# -*- coding: latin-1 -*-

import hashlib
import base64
import datetime
from string import count

class sensorCrypt(object):
        def __init__(self, vPassword):
            vSalt = 'Qr1#Y'
            vManualKey = vPassword+vSalt
            #self.__lenManKey = len(vManualKey)
            self.__crypt_position  = 0
            self.__crypt_position1 = 0
            self.__crypt_position2 = 0
            (self.__crypt_position, self.__crypt_position1, self.__crypt_position2) = self.__GetCryptPosition(len(vManualKey))
            
            print('0: '+ str(self.__crypt_position) + ' # 1: ' + str(self.__crypt_position1) + ' # 2: ' + str(self.__crypt_position2))
            
            self.__key1 = ''
            self.__key2 = ''
            
            (self.__key1, self.__key2) = self.__EncryptKey(vManualKey+str(self.__crypt_position))            

            self.__lenKey1 = len(self.__key1)
            self.__lenKey2 = len(self.__key2)

        def Encrypt(self, vString):
            # print'######'
            #print vString
            encrypted1 = base64.b64encode(vString)
            encrypted = encrypted1[:self.__crypt_position1] + self.__key1 + encrypted1[self.__crypt_position1:self.__crypt_position2]  + self.__key2 + encrypted1[self.__crypt_position2:]
            #print encrypted
            # print'######'
            return str(encrypted)
                  
        def Decrypt(self, vString):
            ilenMesg = len(vString)
            vBase64a = vString[:self.__crypt_position1] + vString[self.__crypt_position1+self.__lenKey1:]
            vBase64 = vBase64a[:self.__crypt_position2] + vBase64a[self.__crypt_position2+self.__lenKey2:-1]
            #print vBase64
            messageData = base64.b64decode(vBase64)
            # print messageData
#             ilenMesg = len(messageData)
#             message = messageData[self.__lenCryptKey:(ilenMesg-self.__lenCryptKey)]
#             print message
            return messageData
        
        def __GetCryptPosition(self, lenKey):
            vDate1 = datetime.datetime.now().strftime('%d%m')
            vDate2 = datetime.datetime.now().strftime('%Y')
            # print str(vDate1) + '#' + str(vDate2)
            qs0 = self.__querSum(vDate1 + vDate2)
            qs1 = self.__querSum(vDate1)
            qs2 = self.__querSum(vDate2)
            qs3 = self.__querSum(lenKey)
            # print str(qs0) + '#' + str(qs1) + '#' + str(qs2) + '#' + str(qs3)
            variant1 = int(round(qs0/9))
            variant2 = int(round(int(vDate1)/qs1))
            variant3 = int(round(variant2/(variant1+qs1)))
            # print str(variant1) + '#' + str(variant2) + '#' + str(variant3)
            vResult = qs0 + variant1 + variant3 + qs3
            # print vResult
            if vResult > 150:
                vResult = str(vResult)[-2:]
                # print vResult
            vResult = int(vResult)+7
            vPos1 = int(round(vResult/3))
            vPos2 = int(round(vPos1*2))
            return (vResult, vPos1, vPos2)
        
        def __EncryptKey(self, vManKey):
            # Hash Key
            vEncryptedKey = hashlib.sha512(vManKey).hexdigest()
            # base64 key
            vEncryptedKey = base64.b64encode(vEncryptedKey)
            # Count =
            vCountParts = count(vEncryptedKey,'=')
            # Cut =
            vEncryptedKey = vEncryptedKey[:len(vEncryptedKey)-vCountParts]
            # If needed add filling
            if vCountParts == 1:
                vEncryptedKey += 'A'
            elif vCountParts == 2:
                vEncryptedKey += 'AC'
            elif vCountParts == 3:
                vEncryptedKey += 'iAC'
            
            # Split Key 
            viDivider = int(round(len(vEncryptedKey)/3))
            vKeyPart1 = vEncryptedKey[:viDivider]
            vKeyPart2 = vEncryptedKey[viDivider:]
            
            return (vKeyPart1, vKeyPart2)
            
        
        def __querSum(self, vZahl):
            zahlString=str(vZahl)
            querSumme=0
            for zifferBuchstabe in zahlString:
                    querSumme=querSumme+int(zifferBuchstabe)
            return querSumme
                           
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
