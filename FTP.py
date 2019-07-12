#!/usr/bin/env python3
import os
import ftplib
import _thread
import time
import progressbar

ftp_path = '/home/robert/Desktop/lftp_test/USG'
ftp_username='fnapierala@3rstudio.com'
ftp_password='7lxCWEh5DB'
files = []

ftp=ftplib.FTP()

def ProgressCallback(self):
    print('.')

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
    #LED zielona
    try:
        ftp.connect('s5.zenbox.pl')
    except:
        print("Failed to connect server!")
        #LED czerwona - błąd
    choice=input()
    while choice!="b":
        choice=input()
        time.sleep(0.001)
        
    try:
        ftp.login(username,password)
    except:
        print("Failed to login!")
        #LED czerwona - błąd
        
def move_to_FTP():
    lFileSet=set(os.listdir(ftp_path))
    rFileSet=set(ftp.nlst())
    transferList=list(lFileSet-rFileSet)
    print("Missing: "+str((transferList)))
    
    for fl in transferList:
        UploadFTP(fl)
        print("Uploaded\n")
  
connect_FTP(ftp_username,ftp_password)

#migaj LED niebieską
move_to_FTP()
#jeśli błąd to czerwona
ftp.quit()
#LED zgaszona

