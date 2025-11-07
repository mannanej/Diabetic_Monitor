#!/usr/bin/env python3
import os
import csv
import time
import shlex
import pickle
import subprocess
from pydexcom import Dexcom
from subprocess import call
from collections import deque
from datetime import datetime
# import Adafruit_BBIO.GPIO as GPIO
####################################################################################################################################
# File Name: main.py
# Author: Eddie Mannan
# Date Created: 06NOV2025
# Date last edited: 07NOV2025
# Topic: ECE434 Embedded Linux, Dr. Yoder
# Project: Diabetic Monitor
# Description: This program will look at an Excel sheet of blood sugar values, crunch some numbers, then display it in multiple ways
# To see the full project, visit my Hackster.io page: https://www.hackster.io/eddiemannan/dexcom-g6-diabetic-monitor-3f7af7
# Info on Dexcom API: https://gagebenne.github.io/pydexcom/pydexcom.html#Dexcom
# 129,600 minutes in 90 days | sugar reading every 5 minutes | 25,920 reading over a A1C period (90 days)
####################################################################################################################################
# For the LEDs with 220 Ohm resistors:
#     Red is P9_11
#     Green is P9_15
#     Blue is P9_21
#     Yellow is P9_23
# The LCD is connected to SPI 1:
#     VCC is P9_4
#     GND is P9_2
#     CS is P9_28
#     RESET is P9_25
#     D/C is P9_27
#     MOSI is P9_30
#     SCK is P9_31
#     LED is P9_16
#     MISO is P9_29
####################################################################################################################################
MAX_CAPACITY = 25920
SUGAR_Q = deque(maxlen = MAX_CAPACITY)
DEXCOM_USERNAME = ""
DEXCOM_PASSWORD = ""
####################################################################################################################################
class DexcomInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        return
####################################################################################################################################
class A1CInfo:
    def __init__(self, sugars):
        self.sugars = sugars
        return
####################################################################################################################################
def main():
    # This section will get the file we need with its path and open it with a csv reader
    systemRunningLED(True)
    startTime = time.perf_counter()
    
    dexcom = Dexcom(username = DEXCOM_USERNAME, password = DEXCOM_PASSWORD) # email address
    glucose_reading = dexcom.get_current_glucose_reading()
    
    # This section will get the current sugar
    currentSugar = glucose_reading.value
    SUGAR_Q.append(currentSugar)
    # This section will get the date
    currentDate = glucose_reading.datetime
    # This section will get the A1C value from these sugars
    a1c = getA1C(SUGAR_Q)
    # This section will get the Highest sugar
    highest = max(SUGAR_Q)
    # This section will get the lowest sugar
    lowest = min(SUGAR_Q)
    # This section will save the current Sugar array
    saveA1CInfo(SUGAR_Q)

    endTime = time.perf_counter()
    runTime = endTime - startTime
    # This section will display the info to the LCD screen
    # subprocess.call(shlex.split(f"./text.sh {currentDate.strftime('%m-%d-%Y')} {currentDate.strftime('%I:%M:%S %p')} {round(a1c, 1)} {currentSugar} {highest} {lowest} {round(runTime, 2)}"))
    # This section will handle the LEDs
    sugarLevelLED(currentSugar)
    systemRunningLED(False)
    ########## General print statements for debugging ##########
    print("Date: ", currentDate.strftime('%m-%d-%Y'))
    print("Time: ", currentDate.strftime('%I:%M:%S %p'))
    print("A1C: ", round(a1c, 1))
    print("Current: ", currentSugar)
    print("Highest: ", highest)
    print("Lowest: ", lowest)
    print("Runtime: ", round(runTime, 2), "seconds")
    return
####################################################################################################################################
def saveDexcomInfo(username, password):
    state = DexcomInfo(username, password)
    with open("bins/DexcomInfo.bin", "wb") as file:
        pickle.dump(state, file)
    return
####################################################################################################################################
def loadDexcomInfo():
    global DEXCOM_USERNAME
    global DEXCOM_PASSWORD
    
    with open("bins/DexcomInfo.bin", "rb") as file:
        state = pickle.load(file)
    DEXCOM_USERNAME = state.username
    DEXCOM_PASSWORD = state.password
    return
####################################################################################################################################
def saveA1CInfo(sugars):
    state = A1CInfo(sugars)
    with open("bins/A1CInfo.bin", "wb") as file:
        pickle.dump(state, file)
    return
####################################################################################################################################
def loadA1CInfo():
    global SUGAR_Q
    
    with open("bins/A1CInfo.bin", "rb") as file:
        state = pickle.load(file)
    SUGAR_Q = state.sugars
    return
####################################################################################################################################
def getA1C(sugars):
    averageSugar = sum(sugars) / len(sugars)
    # Plug in our average sugar value to calulate an A1C
    a1c = (41.6 + averageSugar) / 28.7
    return a1c
####################################################################################################################################
def sugarLevelLED(currentSugar):
#     # Control the different LEDs based on current sugar level
#     RED = "P9_11"
#     GREEN = "P9_15"
#     BLUE = "P9_21"
#     GPIO.setup(RED, GPIO.OUT)
#     GPIO.setup(GREEN, GPIO.OUT)
#     GPIO.setup(BLUE, GPIO.OUT)
#     # Sugar is HIGH
#     if (currentSugar >= 180):
#         GPIO.output(RED, GPIO.HIGH)
#         GPIO.output(GREEN, GPIO.LOW)
#         GPIO.output(BLUE, GPIO.LOW)
#     # Sugar is NORMAL
#     elif (currentSugar < 180 and currentSugar > 80):
#         GPIO.output(RED, GPIO.LOW)
#         GPIO.output(GREEN, GPIO.HIGH)
#         GPIO.output(BLUE, GPIO.LOW)
#     # Sugar is LOW
#     elif (currentSugar <= 80):
#         GPIO.output(RED, GPIO.LOW)
#         GPIO.output(GREEN, GPIO.LOW)
#         GPIO.output(BLUE, GPIO.HIGH)
#     # Error
#     else:
#         GPIO.output(RED, GPIO.HIGH)
#         GPIO.output(GREEN, GPIO.HIGH)
#         GPIO.output(BLUE, GPIO.HIGH)
    return
# ####################################################################################################################################
def systemRunningLED(running):
#     # Turn on/off the yellow LED when the system is calculating
#     YELLOW = "P9_23"
#     GPIO.setup(YELLOW, GPIO.OUT)
#     if (running):
#         GPIO.output(YELLOW, GPIO.HIGH)
#     else:
#         GPIO.output(YELLOW, GPIO.LOW)
    return
####################################################################################################################################
# This is a call to main to get the ball rolling
if __name__ == '__main__':
    # newExcelPull = call("./getNewExcel.sh", shell=True)
    loadDexcomInfo()
    loadA1CInfo()
    main()
####################################################################################################################################
# END FILE
