#!/bin/bash
SERVICE="FTP.py"
if pgrep -x "$SERVICE" >/dev/null
then
    echo "$SERVICE is running"
else
    /home/pi/rpi_ftp_synchronizer/FTP.py
fi
