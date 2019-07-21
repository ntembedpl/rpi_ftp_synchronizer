#!/bin/bash
echo "Change config file"
sudo cp ./config.txt /boot/

echo "Daemonize gpio listener"
sudo cp ./gpint.sh /etc/init.d/
cd ..
sudo chmod +x ./gpio.py
sudo chmod +x /etc/init.d/gpint.sh
sudo update-rc.d gpint.sh defaults

echo "Setup mass storage"
sudo dd if=/dev/zero of=/piusb.bin bs=1M count=512
sudo mkdosfs /piusb.bin
cd scripts
sudo cp ./rc.local /etc/

echo "Rebooting"
sudo reboot
