#!/usr/bin/python3
import os
import ftplib
import _thread
import time
import RPi.GPIO as GPIO
import yaml

ftp_path = '/mnt'
ftp_username=''
ftp_password=''
ftp_server=''
username=""
files = []

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

R=13
G=12
B=6

GPIO.setup(R, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(G, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(B, GPIO.OUT,initial=GPIO.HIGH)

ftp=ftplib.FTP()

def CopyConfig(path):
    if (os.path.isfile(path)==True):
        os.system("mv "+path+" /home/pi/rpi_ftp_synchronizer/config.yaml")
        
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
            print("Read config")
            f.close()

def WriteLog():
    total_size=os.popen("du -sb /mnt | awk '{printf $1}'").read()
    global username
    print("size is: ")
    print(total_size)
    log=dict(
        size='%.1f%%'%((float(total_size)/124514435072)*100),
        signal='100%',
        username=username,
        )
    with open('log.yaml','w') as f:
        yaml.dump(log,f)

def ProgressCallback(self):
    GPIO.output(B,not GPIO.input(B))

def UploadFTP(file,filename):
    f=open(file,'rb')
    ftp.storbinary('STOR '+filename,f,8192,ProgressCallback)
    f.close()

def LED_blink(text,delay):
    count=0    
    while count < 2:
        time.sleep(delay)
        count+=1
        print('%s: %d' % (text,count))
        
def connect_FTP(username,password,server):     
    GPIO.output(G,GPIO.LOW)
    try:
        ftp.connect(server)
    except:
        print("Failed to connect server!")
        GPIO.output(G,GPIO.HIGH)
        GPIO.output(R,GPIO.LOW)
#    choice=input()
#    while choice!="b":
#        choice=input()
#        time.sleep(0.001)
        
    try:
        ftp.login(username,password)
    except:
        print("Failed to login!")
        GPIO.output(G,GPIO.HIGH)
        GPIO.output(R,GPIO.LOW)
        os.system("sudo umount /piusb.bin")               
         
def move_to_FTP():
    lFileSet=set(os.listdir(ftp_path))
    rFileSet=set(ftp.nlst())
    transferList=list(lFileSet-rFileSet)
    print("Missing: "+str((transferList)))
    
    for fl in transferList:
        if fl!='System Volume Information' and fl!='BOOTEX.LOG' and fl!='icon.ico' and fl!='autorun.inf':
            UploadFTP(ftp_path+'/'+fl,fl)
            print("Uploaded\n")
    UploadFTP('./log.yaml','log.yaml')
  
os.system("sudo mount /piusb.bin /mnt")
CopyConfig("/mnt/config.yaml")
ReadConfig('/home/pi/rpi_ftp_synchronizer/config.yaml')
WriteLog()
connect_FTP(ftp_username,ftp_password,ftp_server)
GPIO.output(G,GPIO.HIGH)
move_to_FTP()
ftp.quit()
GPIO.output(B,GPIO.HIGH)
GPIO.output(G,GPIO.LOW)
time.sleep(5)
os.system("sudo umount /piusb.bin")
GPIO.cleanup()
