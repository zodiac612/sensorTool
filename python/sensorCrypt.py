import hashlib
import base64
import datetime

class sensorCrypt(object):
        def __init__(self, vCryptKey):
            self.__key = hashlib.sha512(str(vCryptKey+'salt')).hexdigest()
            self.__lenKey = len(self.__key)
            self.__crypt_position = self.__GetCryptPosition()
            print self.__crypt_position
            

        def Encrypt(self, vString):
            # print'######'
            # print vString
            encrypted1 = base64.b64encode(vString)
            encrypted = encrypted1[0:self.__crypt_position] + self.__key + encrypted1[self.__crypt_position:]
            # print encrypted
            # print'######'
            return str(encrypted)
                  
        def Decrypt(self, vString):
            ilenMesg = len(vString)
            vBase64 = vString[0:self.__crypt_position] + vString[self.__crypt_position+self.__lenKey:len(vString)]
            # print vBase64
            messageData = base64.b64decode(vBase64)
            # print messageData
#             ilenMesg = len(messageData)
#             message = messageData[self.__lenKey:(ilenMesg-self.__lenKey)]
#             print message
            return messageData
        
        def __GetCryptPosition(self):
            vDate1 = datetime.datetime.now().strftime('%d%m')
            vDate2 = datetime.datetime.now().strftime('%Y')
            # print str(vDate1) + '#' + str(vDate2)
            qs0 = self.__querSum(vDate1 + vDate2)
            qs1 = self.__querSum(vDate1)
            qs2 = self.__querSum(vDate2)
            qs3 = self.__querSum(self.__lenKey)
            # print str(qs0) + '#' + str(qs1) + '#' + str(qs2)
            variant1 = int(round(qs0/9))
            variant2 = int(round(int(vDate1)/qs1))
            variant3 = int(round(variant2/(variant1+qs1)))
            # print str(variant1) + '#' + str(variant2) + '#' + str(variant3)
            vResult = qs0 + variant1 + variant3 + qs3
            if vResult > 100:
                vResult = str(vResult)[-2:]
            return vResult
        
        def __querSum(self, vZahl):
            zahlString=str(vZahl)
            querSumme=0
            for zifferBuchstabe in zahlString:
                    querSumme=querSumme+int(zifferBuchstabe)
            return querSumme
                           
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4