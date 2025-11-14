#!/bin/sh
# File Name: install.sh
# Author: Eddie Mannan, David Mattingly
# Date Created: 07FEB2023
# Topic: ECE434 Embedded Linux, Dr. Yoder
# Project: Diabetic Monitor
# Description: Sets the program to run every 5 minutes

# Install modules/packages
apt install fbi
apt install imagemagick

# Add device tree to uEnv.txt
line=$(grep "uboot_overlay_addr4" /boot/uEnv.txt)
sed -i "s|$line|uboot_overlay_addr4=/lib/firmware/BB-LCD-ADAFRUIT-24-SPI1-00A0.dtbo|g" /boot/uEnv.txt

# Configure git
git config pull.rebase false
git config --global --add safe.directory /home/debian/Diabetic_Monitor

# Make autorun.sh executable
chmod +x /home/debian/Diabetic_Monitor/autorun.sh

# Configure autorun in crontab
if ! grep -q "Diabetic_Monitor" /etc/crontab; then
    echo "*/5 * * * * root /home/debian/Diabetic_Monitor/autorun.sh 2>&1 | logger" >> /etc/crontab
fi

echo "Reboot device to enable device overlay"