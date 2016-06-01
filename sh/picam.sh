#!/bin/bash
#/home/pi/yowsup/yowsup-cli demos -s $1 "$2" -c /home/pi/yowsup/config
#echo "$2"

vPicRes=$1
vAction=""
case $vPicRes in
	"low") vAction="-w 320 -h 240 -q 10";;
	"med") vAction="-w 1024 -h 768 -q 25";;
    "high") vAction="-q 25";;    
    "full") vAction="-q 100";;
	*)
		echo "cannot find action for switch"
	;;
esac

if [ ! -z "$vAction" ]
then
    strTime=$(date +%H%M)
    echo "[strTime]: ".$strTime." Take Picture with ". $vPicRes." Quality "
    raspistill $vAction -o /var/sensorTool/www/picam$strTime$vPicRes.jpg
else
    echo "No Quality Set"
fi
