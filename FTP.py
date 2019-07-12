#!/usr/bin/env python3
import os
import ftplib
import _thread
import time
import RPi.GPIO as GPIO

ftp_path = '/mnt'
ftp_username='fnapierala@3rstudio.com'
ftp_password='7lxCWEh5DB'
files = []

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(9, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(10, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT,initial=GPIO.HIGH)

ftp=ftplib.FTP()

def ProgressCallback(self):
    GPIO.output(25,not GPIO.input(25))

def UploadFTP(file):
    f=open(ftp_path+'/'+file,'rb')
    ftp.storbinary('STOR '+file,f,8192,ProgressCallback)
    f.close()

def LED_blink(text,delay):
    count=0    
    while count < 2:
        time.sleep(delay)
        count+=1
        print('%s: %d' % (text,count))
        
def connect_FTP(username,password):     
    GPIO.output(9,GPIO.LOW)
    try:
        ftp.connect('s5.zenbox.pl')
    except:
        print("Failed to connect server!")
        GPIO.output(9,GPIO.HIGH)
        GPIO.output(10,GPIO.LOW)
#    choice=input()
#    while choice!="b":
#        choice=input()
#        time.sleep(0.001)
        
    try:
        ftp.login(username,password)
    except:
        print("Failed to login!")
        GPIO.output(9,GPIO.HIGH)
        GPIO.output(10,GPIO.LOW)
        
def move_to_FTP():
    lFileSet=set(os.listdir(ftp_path))
    rFileSet=set(ftp.nlst())
    transferList=list(lFileSet-rFileSet)
    print("Missing: "+str((transferList)))
    
    for fl in transferList:
        if fl!='System Volume Information':
            UploadFTP(fl)
            print("Uploaded\n")
  
os.system("sudo mount /piusb.bin /mnt")
connect_FTP(ftp_username,ftp_password)
GPIO.output(9,GPIO.HIGH)
move_to_FTP()
ftp.quit()
GPIO.output(25,GPIO.HIGH)
GPIO.output(9,GPIO.LOW)
time.sleep(5)
os.system("sudo umount /piusb.bin")
GPIO.cleanup()
