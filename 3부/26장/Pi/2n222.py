#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO  # GPIO 임포트
import time
 
pinNum = 12
GPIO.setmode(GPIO.BCM) #GPIO num으로 사용
GPIO.setup(pinNum, GPIO.OUT) #GPIO 12번 핀을 출력용으로 선언

try:
    while True:
        val = input("switch [on:1, off:0] :")
        GPIO.output(pinNum, val)
finally:
    GPIO.cleanup() #GPIO를 초기화