#!/bin/bash
# 
#echo "$1" > /home/pi/sensorTool/sh/tempbase.txt

vBase64=$1
python /home/pi/sensorTool/python/updateconf.py $vBase64
