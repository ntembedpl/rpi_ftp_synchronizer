#!/usr/bin/env python3
import os
import ftplib
import _thread
import time
import RPi.GPIO as GPIO
import yaml

ftp_path = '/mnt'
ftp_username='fnapierala@3rstudio.com'
ftp_password='7lxCWEh5DB'
ftp_server='s5.zenbox.pl'
username=""
files = []

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(9, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(10, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(25, GPIO.OUT,initial=GPIO.HIGH)

ftp=ftplib.FTP()

def CopyConfig(path):
    if (os.path.isfile(path)==True):
        os.system("mv "+path+" "+os.getcwd()+"/config.yaml")
        
def ReadConfig(path):
    if (os.path.isfile(path)==True):
        with open(path) as f:       
            config=yaml.safe_load(f)
            config=config['config']
            global username,ftp_username,ftp_server,ftp_password
            username=config['username']
            ftp_username=config['login']
            ftp_server=config['server']
            ftp_password=config['password']  
            f.close()

def WriteLog():
    total_size=sum(os.path.getsize(f) for f in os.listdir('/mnt') if os.path.isfile(f))
    log=dict(
        size='%.1f%%'%((total_size/10000)*100),
        signal='100%',
        username=username,
        )
    with open('log.yaml','w') as f:
        yaml.dump(log,f)

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
        
def connect_FTP(username,password,server):     
    GPIO.output(9,GPIO.LOW)
    try:
        ftp.connect(server)
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
        if fl!='System Volume Information' and fl!='BOOTEX.LOG':
            UploadFTP(fl)
            print("Uploaded\n")
    UploadFTP('./log.yaml')
  
os.system("sudo mount /piusb.bin /mnt")
CopyConfig("/mnt/config.yaml")
ReadConfig('./config.yaml')
WriteLog()
connect_FTP(ftp_username,ftp_password,ftp_server)
GPIO.output(9,GPIO.HIGH)
move_to_FTP()
ftp.quit()
GPIO.output(25,GPIO.HIGH)
GPIO.output(9,GPIO.LOW)
time.sleep(5)
os.system("sudo umount /piusb.bin")
GPIO.cleanup()
