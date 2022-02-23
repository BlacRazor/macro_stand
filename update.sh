#!/bin/bash
cp /home/pi/macro_stand/UpdateStand /home/pi/Desktop/UpdateStand
cp /home/pi/macro_stand/update.sh /home/pi/update.sh
rm -rF /home/pi/macro_stand
git clone https://github.com/BlacRazor/macro_stand.git