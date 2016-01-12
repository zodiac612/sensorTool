#!/usr/bin/env python2.7
# testskript für 433MHz

from rfm69 import Rfm69
import rfm69
import sys
import time
import sensors
from sensors import rawsensor


#if len(sys.argv) != 2:
#    print "usage: intertechno <CODE>" #12-digit code 12 * ['0', '1', 'f']
#   sys.exit(1)

rfm = Rfm69()
rfm.SetParams(
    Freq = 433.92,
    Datarate = 2.666666,
    TXPower = 13,
    ModulationType = rfm69.OOK,
    SyncPattern = [0x80, 0x00, 0x00, 0x00]
    )

print hex(rfm.ReadReg(0x07))
print hex(rfm.ReadReg(0x08))
print hex(rfm.ReadReg(0x09))
    
data = []

while 1:
    data = rfm.ReceivePacket(7)
    obj = rawsensor.CreateSensor(data)
    print(str(obj))
    
