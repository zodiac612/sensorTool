# sensorTool
Checks temperature and humidity and sends messages to mobile phones when reaching defined thresholds.

## Actual functionality
 - Lacrosse Sensors (TX35 & TX29)
 - BME280 Sensors
 - fritz dect 200
 - webradio
 - LED alarm light
 - motion detector
 - Network device detector
 - picam
 - 433 MHZ Switches (intertechno/gt-7000/gt-9000)
 - no whatsapp support because of at the moment unkown problems
 
 Usecases:
    1) Sensor RoomX Value(Temperature and or Humidity) below threshold => alarm triggerd (LED alarm light)
    2) One RoomSensor above relative humidity threshold and absolute humidity is below Outdoor Sensor, 
        than Switch with radiators is started. And stopped if threshold is reached
    3) Toggle of Switches(dect!200 & 433MHz) via web gui 
    4) Tracking of Sensor values over the day
    5) dect!200 showing of actual power consumption
    6) Running webradio if motion is and if webradio running than if no motion and no named mobile is alive webradio is stopped. 
    
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
- spi:
  - http://www.100randomtasks.com/simple-spi-on-raspberry-pi 

## Detailed description
The sensorTool has two main components:
- sensorHttpService.py
  - reads the bme280 and lacrosse sensors values 
  - provides values via httpservice
- sensorLogic.py
  - gets the sensor data via httprequests
  - checks the values against the defined thresholds
  - sends whatsapp messages when the thresholds are reached
