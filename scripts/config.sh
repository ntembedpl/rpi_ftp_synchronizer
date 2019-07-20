#!/bin/bash
cd rpi_ftp_synchronizer

echo "Change config file"
echo "uart_init=115200" | sudo tee -a /boot/config.txt
echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
echo "dtparam=act_led_trigger=none" | sudo tee -a /boot/config.txt
echo "dtparam=act_led_activelow=on" | sudo tee -a /boot/config.txt

echo "Daemonize gpio listener"
sudo cp ./gpint.sh /etc/init.d/
cd ..
sudo chmod +x ./gpio.py
sudo chmod +x /etc/init.d/gpint.sh
sudo update-rc.d gpint.sh defaults

echo "Setup mass storage"
sudo dd if=/dev/zero of=/piusb.bin bs=1M count=512
sudo mkdosfs /piusb.bin
echo "sleep 2" | sudo tee -a /etc/rc.local
echo "sudo modprobe g_mass_storage file=/piusb.bin stall=0 removable=1 idVendor=0x0781 idProduct=0x5572 bcdDevice=0x011a iManufacturer="SanDisk" iProduct="pendrive" iSerialNumber="1234567890" iDescription="pendrive"
" | sudo tee -a /etc/rc.local

echo "Rebooting"
sudo reboot
