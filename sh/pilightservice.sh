#!/bin/bash
vProtocol=$1
vID=$2
vUNIT=$3 # is vZustand for fritzactor
vZustand=$4

if [ -z $vProtocol ]
then 
    echo "Switch protocol missing"
    exit 1
fi

if [ -z $vID ]
then 
    echo "Switch id missing"
    exit 1
fi

echo $vProtocol
if [ "$vProtocol" == "fritzactor" ]
then
    echo "Fritz"
    case $vUNIT in
        1) vAction="on";;
        0) vAction="off";;
        *)
            echo "cannot find action for switch"
            exit 1
        ;;
    esac
    echo "sudo /home/pi/sensorTool/sh/fritzbox-smarthome.sh $vID $vAction"
    sudo /home/pi/sensorTool/sh/fritzbox-smarthome.sh $vID $vAction
else
    echo "433Mhz"
    if [ -z "$vUNIT" ]
    then 
        echo "Switch unit missing"
        exit 1
    fi
    
    case $vZustand in
        1) vAction="-t";;
        0) vAction="-f";;
        *)
            echo "cannot find action for switch"
            exit 1
        ;;
    esac
    vPilightStatus=$(sudo service pilight status | awk -F' ' '{print $3}')
    
    #echo $vID
    #echo $vUNIT
    #echo $vZustand
    #echo $vPilightStatus
        
    if [ $vPilightStatus=="not" ]
    then
        echo "Start PILIGHT"
        sudo service pilight start
        #sleep 5
    fi
    
    echo "sudo pilight-send -p \"$vProtocol\" -i $vID -u $vUNIT $vAction"
    sudo pilight-send -p "$vProtocol" -i $vID -u $vUNIT $vAction
    #echo "Stop Pilight"
    sudo service pilight stop
fi
