#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO
import os
import time
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)  
  
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(9, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(10, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT,initial=GPIO.HIGH)

  
def my_callback2(channel):  
    print("falling edge detected on 24")
    os.system("/home/pi/Desktop/USG/blink.py")    
  
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback2, bouncetime=300)  
  
try:  
    print("Waiting for rising edge on port 24")  
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

           # clean up GPIO on normal exit 
while True:
    time.sleep(1e6)