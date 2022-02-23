#!/bin/bash
## Back up
cp /home/pi/macro_stand/GetPhoto.desktop /home/pi/Desktop/GetPhoto.desktop
cp /home/pi/macro_stand/UpdateStand.desktop /home/pi/Desktop/UpdateStand.desktop
cp /home/pi/macro_stand/update.sh /home/pi/update.sh
## Rm old version
rm -rf /home/pi/macro_stand
## Clone new version
git clone https://github.com/BlacRazor/macro_stand.git
## Update 
cp /home/pi/macro_stand/GetPhoto.desktop /home/pi/Desktop/GetPhoto.desktop
cp /home/pi/macro_stand/UpdateStand.desktop /home/pi/Desktop/UpdateStand.desktop
cp /home/pi/macro_stand/update.sh /home/pi/update.sh