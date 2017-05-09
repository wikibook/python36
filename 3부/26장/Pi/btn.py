#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
 
LedPinNum = 5 # LED 제어 핀번호
BtnPinNum = 6 # 버튼 입력 핀번호
GPIO.setmode(GPIO.BCM)
GPIO.setup(LedPinNum, GPIO.OUT)
# 내부 풀업 저항을 이용
GPIO.setup(BtnPinNum, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        #플업 회로에서는 버튼을 누르면 LOW 상태가 됨.
        if GPIO.input(BtnPinNum)==0:
            GPIO.output(LedPinNum, True)
        else:
            GPIO.output(LedPinNum, False)
        time.sleep(0.25)

finally:
    GPIO.cleanup()