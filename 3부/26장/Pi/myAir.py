#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from datetime import datetime, timedelta
import bme280
import sds011 # 미세먼지 측정 모듈 임포트

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO  # GPIO 임포트

# Python Image Library를 임포트 합니다.
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import urllib

# 라즈베리 파이와 연결된 BCM 핀번호를 선언합니다.
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
btnPinNum = 6 # 버튼 입력 핀번호
ledPinNum = 5 #LED 버튼 입력 번호

# SPI를 사용하는 128x64 해상도 디스플레이를 선언합니다.
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 라이브러리를 초기화
disp.begin()

# 디스플레이를 클리어 해줍니다.
disp.clear()
disp.display()

# sds011을 초기화 해줍니다.
sds011.start()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

#LED 핀 초기화
GPIO.setmode(GPIO.BCM) #GPIO num으로 사용
GPIO.setup(ledPinNum, GPIO.OUT) #GPIO 5번 핀을 출력용으로 선언

draw = ImageDraw.Draw(image)
server_address = "http://fastpy003.appspot.com" # 측정 데이터를 저장할 곳의 웹서비스 주소
airInfo = {'temp': 0.0, 'hum': 0.0, 'press':0.0, 'pm25':0.0, 'pm10': 0.0} # 측정 데이터 저장소

pm10WarnVal = 81 #81 # 미세 먼지 경고 기준값
cancelHumVal = 80 

# 화면에 어떤 데이터를 그릴지 정합니다. 
displayMode = 1 # 1: 온도, 2: 습도, 3 대기압, 4:미세먼지, 5: 초미세먼지,

# timestamp를 이용해 일정 시간이 마다 측정을 하고 데이터를 처리 할 수 있도록 구현됨.
displayInterval = timedelta(seconds=5)  # 5초 마다 1번씩 화면을 업데이트 한다.
checkBME280Interval = timedelta(seconds=60) # 60초 마다 온도, 습도, 대기압 측정
checkSDS011Interval = timedelta(minutes=9)  # 9분동안 sleep상태 1분 동안 미세먼지 측정
sendDataInterval = timedelta(minutes=3)  # 3분 한번 데이터를 서버로 전송한다.
saveDataInterval = timedelta(minutes=12)  # 12분 한번 데이터를 서버에 저장한다. 1시간에 5번

# 처음 시작 할 때 바로 데이터를 읽어 올 수 있도록 기준값을 현재 시간보다 하루 빠르게 한다.
prevDisplayTValue = datetime.now() - timedelta(days=1)
prevBME280TValue = datetime.now() - timedelta(days=1)
prevSDS011TValue = datetime.now() - timedelta(days=1)
SDS011WorkingTValue = datetime.now() # 미세먼지 센서는 1분간 동작 시킨다.
prevSendDataTValue = datetime.now()
prevSaveDataTValue = datetime.now()

try:
    drawTop = 3
    drawSubLabelX = 5
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 27)
    hanFont = ImageFont.truetype('/usr/share/fonts/truetype/unfonts-core/UnDinaru.ttf', 15)
    midHanFont = ImageFont.truetype('/usr/share/fonts/truetype/unfonts-core/UnDinaru.ttf', 12)

    while True:
        currentDateTime = datetime.now()

        if currentDateTime - prevBME280TValue > checkBME280Interval :
            # 온도, 습도, 기압 정보를 가져온다.
            prevBME280TValue = datetime.now() # 현재시간 저장
            print("read BME280")
            airInfo['temp'], airInfo['press'], airInfo['hum'] = bme280.readBME280All()
            airInfo['temp'] = round(airInfo['temp'],1)
            airInfo['press'] = round(airInfo['press'],1)
            airInfo['hum'] = round(airInfo['hum'],1)

        if currentDateTime - prevSDS011TValue > checkSDS011Interval :
            #미세먼지 측정을 위해 sds011을 켠다.
            prevSDS011TValue = datetime.now() # 현재시간 저장
            print("turn on SDS011")
            if not sds011.isWorkingMode() :
                SDS011WorkingTValue = currentDateTime + timedelta(minutes=1) 
                sds011.setWork()

        if currentDateTime > SDS011WorkingTValue :
            #미세먼지 측정 후 60초가 지나면 데이터를 읽고 센서 전원을 끊는다.
            if sds011.isWorkingMode() : # 센서가 동작하고 있으면 미세먼지 정보를 읽어온다.
                print("get on particle info")
                particle = sds011.getParticle()
                if particle :
                    # 습도가 cancelHumVal 이상 넘어가면 정확도가 떨어지기 때문에 측정값을 무시한다.
                    if airInfo['hum'] < cancelHumVal :
                        airInfo['pm25'], airInfo['pm10'] = particle
                        airInfo['pm25'] = round(airInfo['pm25'],1)
                        airInfo['pm10'] = round(airInfo['pm10'],1)

                        if airInfo['pm10'] > pm10WarnVal:
                            GPIO.output(ledPinNum, True)
                        else:
                            GPIO.output(ledPinNum, False)
                    else :
                        airInfo['pm25'] = 0.0
                        airInfo['pm10'] = 0.0
                        GPIO.output(ledPinNum, False)

                sds011.setSleep() # SDS011을 sleep 상태로 바꿔준다.
                print("turn off SDS011")

        if currentDateTime - prevDisplayTValue > displayInterval :
            prevDisplayTValue = datetime.now()

            print ("draw display :" + str(displayMode))
            draw.rectangle((0,0,width-1,height-1), outline=1, fill=0) # 테두리 그리기

            if displayMode == 1:
                 draw.text((drawSubLabelX, drawTop), u"온도 ( ℃ )", font=hanFont, fill=255)
                 draw.text((drawSubLabelX + 25, drawTop+25), str(airInfo['temp']) , font=font, fill=255)
            elif displayMode == 2:
                 draw.text((drawSubLabelX, drawTop), u"습도 ( % )", font=hanFont, fill=255)
                 draw.text((drawSubLabelX + 25, drawTop+25), str(airInfo['hum']) , font=font, fill=255)
            elif displayMode == 3:
                 draw.text((drawSubLabelX, drawTop), u"대기압 ( hPa )", font=hanFont, fill=255)
                 draw.text((drawSubLabelX + 12, drawTop+25), str(airInfo['press']) , font=font, fill=255)
            elif displayMode == 4:
                 draw.text((drawSubLabelX, drawTop), u"미세먼지 (ug/m^3)", font=midHanFont, fill=255)
                 draw.text((drawSubLabelX + 25, drawTop+25), str(airInfo['pm10']) , font=font, fill=255)
            elif displayMode == 5:
                 draw.text((drawSubLabelX, drawTop), u"초미세먼지 (ug/m^3)", font=midHanFont, fill=255)
                 draw.text((drawSubLabelX + 25, drawTop+25), str(airInfo['pm25']) , font=font, fill=255)
                 displayMode = 0 # 처음으로 돌아 간다.

            displayMode += 1

            #draw display
            disp.image(image)
            disp.display()
        
        # Send Data to Server
        if currentDateTime - prevSendDataTValue > sendDataInterval :
            prevSendDataTValue = datetime.now()
            print ("send data")
            params = urllib.urlencode(airInfo) #URL에 데이터를 실어서 서버로 데이터를 전달.
            conn = urllib.urlopen( server_address + "/setAirInfo?%s" % params)
            print (conn.read().decode("utf-8") )

        if currentDateTime - prevSaveDataTValue > saveDataInterval :
            prevSaveDataTValue = datetime.now()
            print ("save data")
            params = urllib.urlencode(airInfo) #URL에 데이터를 실어서 서버로 데이터를 전달.
            conn = urllib.urlopen( server_address + "/saveAirInfo?%s" % params)
            print (conn.read().decode("utf-8") )

        time.sleep(0.5)   

finally:
    disp.clear()
    disp.display()
    sds011.setSleep() # SDS011에 전원이 끊어 집니다.
    time.sleep(1)
    sds011.end()