#!/bin/bash
# 
#echo "$1" #> /var/sensorTool/www/tempbase.txt

vBase64=$1
python /home/pi/sensorTool/python/bosestControl.py $vBase64
#vPARAMS=$(echo "$1" | base64 -d)
#echo $vPARAMS
#/home/pi/webradio/webradio.sh $vPARAMS

