#!/bin/sh

PIDLA=`ps -ef | grep sensorHttpService.py | awk '$0!~/grep/ && $2~/[0-9]/{print $2}'`;
PIDIN=`ps -ef | grep sensorLogic.py | awk '$0!~/grep/ && $2~/[0-9]/{print $2}'`;

if [ -z "$PIDIN" ] ; then
    /home/pi/yowsup/yowsup-cli demos -s 4917634546625 "in3monitor.py stop unexpectly!" -c /home/pi/yowsup/config
    echo "sensorLogic.py stop unexpectly!"
else
    echo "sensorLogic.py PID" $PIDIN
fi
if [ -z "$PIDLA" ] ; then
    /home/pi/yowsup/yowsup-cli demos -s 4917634546625 "Lacrosse.py stop unexpectly!" -c /home/pi/yowsup/config
    echo "sensorHttpService.py stop unexpectly!" 
else
    echo "sensorHttpService.py PID" $PIDLA
fi
