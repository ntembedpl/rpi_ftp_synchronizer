#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(9, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(10, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT,initial=GPIO.HIGH)
counter=0
  
while counter<6:
    GPIO.output(10,not GPIO.input(10))
    time.sleep(0.1)
    counter+=1
