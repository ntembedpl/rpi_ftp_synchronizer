#!/usr/bin/env python2.7  
import RPi.GPIO as GPIO
import os
import time
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)  

switch=10
R=6
G=12
B=13
  
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(G, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(B, GPIO.OUT,initial=GPIO.HIGH)

  
def my_callback2(channel):  
    print("falling edge detected on 10")
    os.system("/home/pi/rpi_ftp_synchronizer/FTP.py")    
  
GPIO.add_event_detect(switch, GPIO.FALLING, callback=my_callback2, bouncetime=300)  
  
try:  
    print("Waiting for rising edge on port 10")  
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  

           # clean up GPIO on normal exit 
while True:
    time.sleep(1e6)
