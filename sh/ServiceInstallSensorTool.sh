###############################################################################
#### Startskript
###############################################################################
#############
# test and install start script
#
ln -s /home/pi/sensorTool/sensorTool /etc/init.d/sensorTool
sudo update-rc.d sensorTool defaults

#sudo update-rc.d sensorTool remove

