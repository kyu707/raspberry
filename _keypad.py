import concurrent.futures
import json
import logging
import os
import os.path
import pathlib2 as pathlib
import sys
import time
import uuid

import click
import grpc
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import RPi.GPIO as GPIO
import aiy.device._buzzer as BUZZER
from time import sleep
import GPIO_EX

BUZZER_PIN  = 17
ON = 1
OFF = 0

scale = [ 261, 294, 329, 349, 392, 440, 493, 523 ]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm = GPIO.PWM(BUZZER_PIN, 100)


ROW0_PIN = 0
ROW1_PIN = 1
ROW2_PIN = 2
ROW3_PIN = 3
COL0_PIN = 4
COL1_PIN = 5
COL2_PIN = 6

#COL0_PIN = 6
#COL1_PIN = 12
#COL2_PIN = 13
#ROW0_PIN = 19
#ROW1_PIN = 26
#ROW2_PIN = 20
#ROW3_PIN = 21

COL_NUM = 3
ROW_NUM = 4

keyData = 0
g_preData = 0
g_counter = 0

inputPasswd = []
passwd = ['2','5','8','0']

colTable = [COL0_PIN, COL1_PIN, COL2_PIN]
rowTable = [ROW0_PIN, ROW1_PIN, ROW2_PIN, ROW3_PIN]

def initKeypad():
    for i in range(0, COL_NUM):
        GPIO_EX.setup(colTable[i], GPIO_EX.IN)
#        GPIO.setup(colTable[i], GPIO.IN)
    for i in range(0, ROW_NUM):
        GPIO_EX.setup(rowTable[i], GPIO_EX.OUT)
#        GPIO.setup(rowTable[i], GPIO.OUT, initial=False)

def selectRow(rowNum):
    for i in range(0, ROW_NUM):
        if rowNum == (i+1):
            GPIO_EX.output(rowTable[i], GPIO_EX.HIGH)
#            GPIO.output(rowTable[i], GPIO.HIGH)
#            sleep(0.001)
        else:
            GPIO_EX.output(rowTable[i], GPIO_EX.LOW)
#            GPIO.output(rowTable[i], GPIO.LOW)
            sleep(0.001)

def readCol():
    keypadstate = -1
    for i in range(0, COL_NUM):
        inputKey = GPIO_EX.input(colTable[i])
        if inputKey:
            keypadstate += (i+2)
#            print("key : %d"%keypadstate)
    return keypadstate

def verifyPasswd():
    if passwd == inputPasswd:
        print("passwd correct!!")
        return 0
    else:
        return -1

def inputText(keyData):
    global g_counter
    
    if keyData == 0:
        inputPasswd.append('0')
        g_counter += 1
    elif keyData == 1:
        inputPasswd.append('1')
        g_counter += 1
    elif keyData == 2:
        inputPasswd.append('2')
        g_counter += 1
    elif keyData == 3:
        inputPasswd.append('3')
        g_counter += 1
    elif keyData == 4:
        inputPasswd.append('4')
        g_counter += 1
    elif keyData == 5:
        inputPasswd.append('5')
        g_counter += 1
    elif keyData == 6:
        inputPasswd.append('6')
        g_counter += 1
    elif keyData == 7:
        inputPasswd.append('7')
        g_counter += 1
    elif keyData == 8:
        inputPasswd.append('8')
        g_counter += 1
    elif keyData == 9:
        inputPasswd.append('9')
        g_counter += 1

'''
    GPIO.output(ROW0_PIN, GPIO.HIGH)
    GPIO.output(ROW1_PIN, GPIO.HIGH)
    GPIO.output(ROW2_PIN, GPIO.HIGH)
    GPIO.output(ROW3_PIN, GPIO.HIGH)
    sleep(0.001)
    col0 = GPIO.input(COL0_PIN)
    col1 = GPIO.input(COL1_PIN)
    col2 = GPIO.input(COL2_PIN)
    print("col0 : %d"%col0)
    print("col1 : %d"%col1)
    print("col2 : %d"%col2)
    sleep(0.01)
'''
def readKeypad():
#    global keyData
    global g_preData
    keyData = -1
    
    selectRow(1)
    row1Data = readCol()
    if (row1Data != -1):
        keyData = row1Data
#        print("Key1 Data : %d"%keyData)
#        print("Key1 Data : %d"%keyData)

    if keyData == -1:
        selectRow(2)
        row2Data = readCol()
        if (row2Data != -1):
            keyData = row2Data + 3
            row2Data = -1
#        print("Key2 Data : %d"%keyData)
        
    if keyData == -1:
        selectRow(3)
        row3Data = readCol()
        if (row3Data != -1):
            keyData = row3Data + 6
            row3Data = -1
#        print("Key3 Data : %d"%keyData)
        
    if keyData == -1:
        selectRow(4)
        row4Data = readCol()
        if (row4Data != -1):
            if row4Data == 2:
                keyData = 0
            row4Data = -1
#        print("Key4 Data : %d"%keyData)

#    print("Key Data : %d"%keyData)
#    print("Pre Data : %d"%g_preData)

    if keyData == -1:
        return -1

    '''
    if g_preData == keyData:
        return -1

    g_preData = keyData
    '''

    print("Keypad Data : %d"%keyData)
#    sleep(3)
    sleep(0.5)
    return keyData

def threadReadKeypad():
    while True:
        readKeypad()


def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    
    global g_counter
    global inputPasswd

    initKeypad()
    print("setup keypad pin")
    try:
        while True:
            keyData = readKeypad()

            '''
            inputText(keyData)

            if g_counter == 4:
                print("counter : %d"%g_counter)
                print("passwd : %s"%inputPasswd)
                
                if verifyPasswd() == 0:
                    print("door is opened!!")
                
                g_counter = 0
                del inputPasswd[0:4]
            '''

    except KeyboardInterrupt:
        GPIO.cleanup()
        

def keybuz():
    global keyData
    #readKeypad()
    initKeypad()
    print("start")
    
    if(keyData == 0):
        pwm.ChangeDutyCycle(90)
        pwm.ChangeFrequency(scale[0])
        
    elif(keyData == 1):
        pwm.ChangeDutyCycle(90)
        pwm.ChangeFrequency(scale[1])
        
        

if __name__ == '__main__':
    main()
