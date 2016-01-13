# sensorTool
Checks temperature and humidity and sends messages to mobile phones when reaching defined thresholds.

## TODO
  - Some Settings are made within the scripts, i want to shift these into the config file.
  - Within the code are language mixed descriptions (german and english)
  - The php part is still missing.
  - other topics

## Goal
Check temperature in bath to avoid freezing temperatures, when going to bed.
Check humidity in the cellar to avoid to much humidity by starting a fan.

## Hardware
- Raspberry PI
- bme280-breakout
  - The bme280 sensor, which detects temperature, humidity and pressure.
  - http://www.watterott.com/de/BME280-Breakout-Luftfeuchtigkeits-Druck-Tempertursensor
- Saintsmart 2-way Relay
  - needs its own power, i used a usb cable connected to the raspberry
  - switch the relays by using transistors
- radio sensors
  - lacrosse temperature sensors, i use three of the tx35dth (temperature, humidity, every 4s, 868MHz)
- radio sender and receiver
  - rfm69 (868MHz)
  - http://www.seegel-systeme.de/produkt/raspyrfm-ii/
- useable mobile number for whatsapp messages

## Software
- GPIO:
  - git clone git://git.drogon.net/wiringPi
- BME280:
  - git clone https://github.com/tisfablab/inmonitor
- whatsapp:
  - git clone git://github.com/tgalal/yowsup.git
- raspyrfm:
  - git clone https://github.com/Phunkafizer/RaspyRFM

## Detailed description
The sensorTool has two main components:
- sensorHttpService.py
  - reads the bme280 and lacrosse sensors values 
  - provides values via httpservice
- sensorLogic.py
  - gets the sensor data via httprequests
  - checks the values against the defined thresholds
  - sends whatsapp messages when the thresholds are reached
