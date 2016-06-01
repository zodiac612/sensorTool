sudo nmap -sP 192.168.1.0/24 -oG /var/sensorTool/NetScan.txt > /dev/null
cat /var/sensorTool/NetScan.txt | awk '$1 ~ /^Host/ {print $2 $3 $5}' | 
                                                    awk -F'(' '{print $1";"$2}' | 
                                                    awk -F')' '{print $1";"$2}' | 
                                                    awk -F';' '{print "{\"IP\": \""$1"\", \"hostname\": \""$2"\", \"status\": \""$3"\"}"}'
