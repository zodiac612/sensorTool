#!/bin/bash
# originally by https://github.com/fbartels/scripts/tree/master/avm-fritzbox/fritzbox-login.sh
## ip, idfile, password and username can optionally be specified as global variables
## Example:
## to get sid of fritz.powerline and store it in /tmp/avmsidpowerine use the following
# commands before calling fritzbox-login.sh
# export tempip=fritz.powerline
# export tempid=/tmp/avmsidpowerline
# 

source /home/pi/sensorTool/sh/fritzbox-login.conf
avmfbip=${tempip:-fritz.box}

challenge=$(curl -s http://$avmfbip/login_sid.lua |  grep -o "<Challenge>[a-z0-9]\{8\}" | cut -d'>' -f 2)
hash=$(echo -n "$challenge-$avmfbpwd" |sed -e 's,.,&\n,g' | tr '\n' '\0' | md5sum | grep -o "[0-9a-z]\{32\}")
avmsid=$(curl -s "http://$avmfbip/login_sid.lua" -d "response=$challenge-$hash" -d 'username='${avmfbuser} \
	| grep -o "<SID>[a-z0-9]\{16\}" |  cut -d'>' -f 2 )

#echo $avmsid

# end of login function
