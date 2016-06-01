#!/usr/bin/python
# -*- coding: latin-1 -*-
# gpio.py
# originally by https://github.com/tisfablab/inmonitor
# no adjustments necessary to original file

import time
import RPi.GPIO as GPIO

DEBUG = 0
	
class GPIOout:
	isOn = 0
	
	def __init__(self, pin):
		self.PIN = pin
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.PIN, GPIO.OUT)
		self.off()
		
	def on(self):
		if not GPIO.input(self.PIN): 
			if DEBUG: print("PIN", self.PIN, "ON")
			GPIO.output(self.PIN, 1)		
		self.isOn = 1

	def off(self):
		if GPIO.input(self.PIN):
			if DEBUG: print("PIN", self.PIN, "OFF")
			GPIO.output(self.PIN, 0)
		self.isOn = 0

	def status(self):
		return GPIO.input(self.PIN)
			
	def pulse(self, secs=0.2):
		self.on()
		time.sleep(secs)
		self.off()

class GPIOin:
	def __init__(self, pin):
		self.PIN = pin
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.PIN, GPIO.IN)

	def status(self):
		return GPIO.input(self.PIN)
