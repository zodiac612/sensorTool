### BEGIN INIT INFO
# Provides:          sensorTool
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts up the sensorTool scripts.
# Description:       This service is used to gather data from different sources and send them to the cloud server/database. Furthermore, it adds an URL link to the local IP.
### END INIT INFO

MYPATH="/home/pi/sensorTool/python"
SCRIPT1="sensorHttpService.py"
SCRIPT2="sensorLogic.py"
SCRIPT3="/home/pi/sensorTool/sh/checkSensorTool.sh"

WIFIRECONNECT="/home/pi/sensorTool/wifi-reconnect.sh"

case "$1" in 
    start)
#	value=$( ps ax | grep -c "$WIFIRECONNECT" )
#	if [ $value -lt 2 ]
#	then
#		echo "Starting wifi reconnect script"
#		$WIFIRECONNECT > /dev/null 2>&1 &
#	fi
	ntpd -q -g -x -n
	sleep 2
	service ntp start
	sleep 2
	echo "Starting sensorTool"
#	$MYPATH/$SCRIPT1 start >/dev/null 2>&1 &
	echo '' > /home/pi/sensorService.log	
	$MYPATH/$SCRIPT1 start >/home/pi/sensorService.log 2>&1 &
	$MYPATH/$SCRIPT2 start >/dev/null 2>&1 &
#	$MYPATH/$SCRIPT3 start >/dev/null 2>&1 &
        ;;
    testService)
        echo "(Re)Starting ".$SCRIPT1." in verbose mode"
	killall $SCRIPT1 >/dev/null 2>&1
        $MYPATH/$SCRIPT1 test
        ;;
    testLogic)
        echo "(Re)Starting ".$SCRIPT2." in verbose mode"
	killall $SCRIPT2 >/dev/null 2>&1
        $MYPATH/$SCRIPT2 test
        ;;
    check)
        echo "(Re)Starting ".$SCRIPT3." in verbose mode"
        $SCRIPT3
        ;;
    stop)
        echo "Stopping sensorTool"
        killall $SCRIPT1 >/dev/null 2>&1
	sleep 1
        killall $SCRIPT2 >/dev/null 2>&1
	sleep 1
        killall $SCRIPT3 >/dev/null 2>&1
	sleep 1
	/home/pi/RelaisSchalten aus
	/home/pi/LedSchalten aus
        ;;
    *)
        echo "Usage: service sensorTool start|stop|testService|testLogic|testPCheck"
        exit 1
        ;;
esac

exit 0
