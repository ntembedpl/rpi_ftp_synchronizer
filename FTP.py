import os
import ftplib
import _thread
import time

ftp_path = '/home/robert/Desktop/lftp_test/USG'
ftp_username='fnapierala@3rstudio.com'
ftp_password='7lxCWEh5DB'
files = []

ftp=ftplib.FTP()
ftp.connect('s5.zenbox.pl')

def UploadFTP(file):
    f=open(ftp_path+'/'+file,'rb')
    ftp.storbinary('STOR '+file,f)
    f.close()

def LED_blink(text,delay):
    count=0    
    while count < 2:
        time.sleep(delay)
        count+=1
        print('%s: %d' % (text,count))
        

def connect_FTP(username,password):       
    try:
        ftp.login(username,password)
    except:
        print("Failed to login")
            
def move_to_FTP():
    lFileSet=set(os.listdir(ftp_path))
    rFileSet=set(ftp.nlst())
    transferList=list(lFileSet-rFileSet)
    print("Missing: "+str((transferList)))
    
    for fl in transferList:
        UploadFTP(fl)
        print("Uploaded\n")
#print(ftplib.FTP('s22.zenbox.pl','tyma@ntembed.pl','malibu'))  
  
connect_FTP(ftp_username,ftp_password)

move_to_FTP()
#print(ftp.nlist())
ftp.quit()

