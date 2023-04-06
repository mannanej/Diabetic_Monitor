#!/bin/sh
# File Name: autorun.sh
# Author: Eddie Mannan, David Mattingly
# Date Created: 13FEB2023
# Topic: ECE434 Embedded Linux, Dr. Yoder
# Project: Diabetic Monitor
# Description: Called by crontab, runs the main code

cd /home/debian/Diabetic_Monitor

python3 main.py