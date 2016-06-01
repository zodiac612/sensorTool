#!/usr/bin/python
# -*- coding: latin-1 -*-

from sensorLight import sensorLight
from time import sleep

Leuchte = sensorLight(26)

print(Leuchte.activate())
sleep(5)
print(Leuchte.deactivate())
