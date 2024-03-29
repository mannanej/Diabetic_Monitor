
# Diabetic Monitor

Embedded Linux Final Project

Eddie Mannan and David Mattingly

## Install

Clone this repository under the name Diabetic_Monitor and run:

  sudo install.sh
  reboot

It will configure the crontab to run autorun.sh every five minutes, which in turn runs the primary python script. It also installs the library for the LCD and configures /boot/uEnv.txt to add the device tree on uboot_overlay_addr4.

There should be no need to re-run install.sh at reboot, unless something else has changes the few things that install.sh configures.

### Pinout

The LCD is configured on SPI1.

| Pin   | Connection |
| --- |  --- |
| P9_11 | Red LED    |
| P9_15 | Green LED  |
| P9_21 | Blue LED   |
| P9_23 | Yellow LED |
| P9_04 | LCD VCC    |
| P9_02 | LCD GND    |
| P9_28 | LCD CS     |
| P9_25 | LCD RESET  |
| P9_27 | LCD D/C    |
| P9_30 | LCD MOSI   |
| P9_31 | LCD SCK    |
| P9_16 | LCD LED    |
| P9_29 | LCD MISO   |

## Project Discription

This project is meant to make handling Type 1 Diabetes easier. The project will take a Dexcom .csv file full of blood sugar data, pull the values from this file, and output various data points to the user such as:

Eddie Mannan Dexcom Monitor  
Date: XX-XX-XXXX  
Time: XX:XX:XX  
A1C: XXX  
Current Sugar: XXX  
Highest Sugar: XXX  
Lowest Sugar: XXX  
Computation Time: X.XX seconds  
  
The board will also turn on a different colored LED based on the Current Sugar value. If the blood sugar is HIGH (>170), it will turn on the Red, if the blood sugar is GOOD(<170, >70) it will turn Green, and if it is LOW(<70) it will turn Blue. Also, while the project is running and doing its calculations, it will light up the Yellow LED as an assurance that the project is doing something.

## eLinux Page

https://elinux.org/ECE434_Project_-_Diabetic_Monitor

## Hackster.io page

https://www.hackster.io/eddiemannan/dexcom-g6-diabetic-monitor-3f7af7