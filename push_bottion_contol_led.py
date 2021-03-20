#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2019, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# push_button_control_led.py
# Turn on the led when push button is pressed with interrupt way, and 
# de-bounces by software
#
# Original author : sosorry
# Date   : 06/22/2014
# Modifier : Yenting
# Date : 03/20/2021

import RPi.GPIO as GPIO                 
import time
import requests
import json


GPIO.setmode(GPIO.BOARD)                
WAIT_TIME = 200
status1 = GPIO.LOW
BTN_PIN1 = 12
LED_PIN1 = 11

status2 = GPIO.LOW
BTN_PIN2 = 22
LED_PIN2 = 18

def gpio_setup(btn_pin, led_pin, status):
	GPIO.setup(btn_pin, GPIO.IN,  pull_up_down=GPIO.PUD_UP)
	GPIO.setup(led_pin, GPIO.OUT, initial=status) 
   
def mycallback1(channel):
	print( "----------" )                                                 
	print("Button pressed @" + str(channel), time.ctime())
	global status1
	if status1 == GPIO.LOW:
		status1 = GPIO.HIGH
		print ("Send http request 'ON' @ " + str(channel) )
		#payload = {'Yenting':'Done!'}
		#r = requests.post('http://192.168.1.102:4567/post', data = json.dumps(payload))
		r = requests.get('http://192.168.1.102:4567/Yenting/done')
		
		### 
	else:
		status1 = GPIO.LOW
		print ("Send http request 'OFF' @ " + str(channel) )
		#payload = {'Yenting':'Not yet...'}
		#r = requests.post('http://192.168.1.102:4567/post', data = json.dumps(payload))
		r = requests.get('http://192.168.1.102:4567/Yenting/working')
	GPIO.output(LED_PIN1, status1)
    
    
def mycallback2(channel):                     
	print( "----------" )                             
	print("Button pressed @" + str(channel), time.ctime())
	global status2
	if status2 == GPIO.LOW:
		status2 = GPIO.HIGH
		print ("Send http request 'ON' @ " + str(channel) )
		r = requests.get('http://192.168.1.102:4567/Li/done')
		### 
	else:
		status2 = GPIO.LOW
		print ("Send http request 'OFF' @ " + str(channel) )
		r = requests.get('http://192.168.1.102:4567/Li/working')
	GPIO.output(LED_PIN2, status2)



gpio_setup(BTN_PIN1, LED_PIN1, status1) 
gpio_setup(BTN_PIN2, LED_PIN2, status2) 

try:
	GPIO.add_event_detect(BTN_PIN1, GPIO.FALLING, callback=mycallback1, bouncetime=WAIT_TIME)
	GPIO.add_event_detect(BTN_PIN2, GPIO.FALLING, callback=mycallback2, bouncetime=WAIT_TIME)

	while True:
		time.sleep(10)

except KeyboardInterrupt:
	print("Exception: KeyboardInterrupt")

finally:
	GPIO.cleanup()          
