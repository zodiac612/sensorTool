#!/bin/bash
# originally by https://github.com/fbartels/scripts/tree/master/avm-fritzbox/fritzbox-smarthome.sh
# API definition: http://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AHA-HTTP-Interface.pdf
#source $HOME/bin/fritzbox-login.sh
source /home/pi/sensorTool/sh/fritzbox-login.sh
CURLCMD="curl -s http://$avmfbip/webservices/homeautoswitch.lua"

# fritzbox-smarthome.sh 24:65:11:C7:80:BF
# fritzbox-smarthome.sh 087610154253

# only get ainlist if no first argument was given
if [ -z $1 ]; then
	echo "Run without parameters the script will iterate over all AVM Smarthome devices and ask to toggle them."
	echo "Usage: $0 [AIN-of-device[,secound-AIN] [on/off]}"
	ainlist=$($CURLCMD"?sid=$avmsid&switchcmd=getswitchlist")
elif [[ $1 == "list" ]]; then
	echo "Listing known switches and their states:"
	ainlist=$($CURLCMD"?sid=$avmsid&switchcmd=getswitchlist")
elif [[ $1 == "csvlist" ]]; then
	ainlist=$($CURLCMD"?sid=$avmsid&switchcmd=getswitchlist")
else
	ainlist=$1
fi
ainlist=$(echo $ainlist | sed -e "s/,/ /g")

for ain in $ainlist; do
	# get current state of the switche. will skip to the next if the given ain cannot be reached (invalid or other error)
	ainstate=$($CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=getswitchstate")
	case $ainstate in
		1) ainstate2=on;;
		0) ainstate2=off;;
		*)
			echo "cannot find switch with AIN $ain"
			continue
		;;
	esac

	# get labeled name (e.g. FRITZ!Powerline 546E or Livingroom)
	ainname=$($CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=getswitchname")
	# additional infos for list
	ainpower=$($CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=getswitchpower")
	aintemperature=$($CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=gettemperature")

	if [ ! -z $2 ]; then
		# force switchcmd if explicitly given (non-interactive mode)
		case $2 in
			on) $CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=setswitchon" > /dev/null;;
			off) $CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=setswitchoff" > /dev/null;;
			*)
				echo "Error: Unknown option! Has to be 'on' or 'off'."
				exit 1
			;;
		esac
	elif [[ $1 == "list" ]]; then
		echo "Switch with AIN $ain ($ainname) ist currently $ainstate2 [$ainpower mW|$aintemperature °C]."
	elif [[ $1 == "csvlist" ]]; then
		#echo "$ain;$ainname;$ainstate2;$ainpower;$aintemperature;"
		echo "{\"id\": \"$ain\", \"name\": \"$ainname\", \"state\": \"$ainstate2\", \"mW\": $ainpower, \"T\": $aintemperature}"
	else
		# else ask interactively to toggle the switch (interactive mode)
		read -p "Do you want to toggle $ainname ($ain)? Switch is currently $ainstate2. (y/n) " -n 1 -r
		echo
		if [[ $REPLY =~ ^[YyJj]$ ]]; then
			switchtoggle=$($CURLCMD"?sid=$avmsid&ain=$ain&switchcmd=setswitchtoggle")
			if [ $switchtoggle -eq 1 ]; then
					echo "Switch $ainname is now: on."
			else
					echo "Switch $ainname is now: off."
			fi
		fi
	fi
done
