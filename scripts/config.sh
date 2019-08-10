#!/bin/bash
echo "Change config file"
sudo cp ./config.txt /boot/

echo "Daemonize gpio listener"
sudo cp ./gpint.sh /etc/init.d/
cd ..
sudo chmod +x ./gpio.py
sudo chmod +x ./run_cron.sh
sudo chmod +x /etc/init.d/gpint.sh
sudo update-rc.d gpint.sh defaults

echo "Setup mass storage"
sudo dd if=/dev/zero of=/piusb.bin bs=8M count=15000
sudo mkdosfs /piusb.bin
cd scripts
sudo cp ./rc.local /etc/

echo "Setup cron"
crontab -l > mycron
echo "*/10 * * * * sudo /home/pi/rpi_ftp_synchronizer/scripts/run_cron.sh" >> mycron
crontab mycron
rm mycron

echo "Rebooting"
sudo reboot
