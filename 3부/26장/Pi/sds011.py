#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import time
import RPi.GPIO as GPIO  # GPIO 임포트

se = serial.Serial()
se.port = "/dev/serial0"  # 포트
se.baudrate = 9600  # 통신속도
bjtNum = 12 #트랜지스터를 제어할 때 사용할 핀번호
GPIO.setmode(GPIO.BCM) #GPIO num으로 사용
GPIO.setup(bjtNum, GPIO.OUT) #GPIO 12번 핀을 출력용으로 선언
isWork = False

def isWorkingMode():
    global isWork
    return isWork

def setSleep():
    global isWork
    isWork = False
    GPIO.output(bjtNum, GPIO.LOW)   # 트랜지스터 Base의 전압을 0V으로 설정

def setWork():
    # 220옴 저항 때문에 트랜지스터 Base핀의 전압이 1V가 된다.
    global isWork
    isWork = True
    GPIO.output(bjtNum, GPIO.HIGH)

def start():
    se.open()
    se.flushInput()

def end():
    se.close()
    GPIO.cleanup() #GPIO를 초기화
 
def getParticle():
    byte = 0
    # Message Header (0xAA)를 만날 때 까지 시리얼 버퍼에서 1바이트씩 읽어 옵니다.
    while byte != '\xaa':
        byte = se.read(size=1)
        
    data = se.read(size=9) # 패킷 사이즈 (9바이트)만큼 데이터를 가져옵니다.
    print(' '.join(x.encode('hex') for x in data)) # 디버깅을 위해 data를 HEX 형식으로 프린트 합니다.

    # Command ID가 0xC0, Message Tail이 0xAB인지 확인 합니다.
    if data[0] == '\xc0' and data[8] == '\xab' :
        # ord 함수를 이용해 data를 ascii (int)로 변환합니다.
        # DATA 1 부터 DATA 6을 더한 값의 low byte이 check-sum data입니다.
        # DATA 1부터 DATA 6 더한 값의 low byte만 사용합니다.
        checkSum = (ord(data[1]) + ord(data[2]) + ord(data[3]) + ord(data[4]) + ord(data[5]) +ord(data[6]))%256

        if checkSum == ord(data[7]) :
            pm25 = float(ord(data[2])*256 + ord(data[1]))/10
            pm10 = float(ord(data[4])*256 + ord(data[3]))/10
            return (pm25, pm10)
        else :
            return None
    else :
        return None

if __name__=="__main__":
    start()
    setWork() # 전원이 SDS011에 공급됩니다.
    time.sleep(10)
    cnt = 10
    while cnt:
        particle = getParticle()
        if particle :
            pm25, pm10 = particle
            print ("PM2.5 :" + str(pm25))
            print ("PM10 :" + str(pm10))
            print ("")
        time.sleep(5)
        cnt -= 1
    setSleep() # SDS011에 전원이 끊어 집니다.
    time.sleep(1)
    end()