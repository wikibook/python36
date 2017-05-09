#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO  # GPIO 임포트
import time
 
pinNum = 5
GPIO.setmode(GPIO.BCM) #GPIO num으로 사용
GPIO.setup(pinNum, GPIO.OUT) #GPIO 5번 핀을 출력용으로 선언
 
cnt = 10
flag = True
while cnt > 0 :
    if flag :
        print ("LED is ON")
    else :
        print ("LED is OFF")
    GPIO.output(pinNum, flag) # flag가 True이면 LED가 켜지고 False이면 LED가 꺼진다
    cnt-=1
    flag = not flag
    time.sleep(0.5) # 0.5초 동안 sleep
GPIO.cleanup() #GPIO를 초기화
