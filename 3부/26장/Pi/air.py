#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import bme280
import sds011 # 미세먼지 측정 모듈 임포트

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

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
BtnPinNum = 6 # 버튼 입력 핀번호

# SPI를 사용하는 128x64 해상도 디스플레이를 선언합니다.
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 라이브러리를 초기화
disp.begin()

# 디스플레이를 클리어 해줍니다.
disp.clear()
disp.display()

sds011.start()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))

draw = ImageDraw.Draw(image)

mode = 0 # 0: auto, 1: 온도,습도,대기압, 2: 온도, 3: 습도, 4 대기압, 5:미세먼지, 6: 초미세먼지, 7: 화면 꺼짐
displayMode = 0 # 1: 온도,습도,대기압, 2: 온도, 3: 습도, 4 대기압, 5:미세먼지, 6: 초미세먼지
firstFlag = True

meanInterval = 60 # 60초 마다 온도, 습도, 대기압 측정
particleMeanInterval = 9 # 온,습도 대기압 측정 9번 하면 1번 미세 먼지 측정을 한다.
displayInterval = 5 # 5초 마다 화면 갱신을 한다.
saveAirInfoInterval = 10 # 180분 마다 한번 측정정보를 Google Cloud Datastore에 저장한다.
sendAirInfoInterval = 3 # 3분 마다 측정정보를 서버에 보낸다.

airInfo = {'temp': 0.0, 'hum': 0.0, 'press':0.0, 'pm25':0.0, 'pm10': 0.0} # 측정 데이터 저장소

try:
    
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 15)
    hanFont = ImageFont.truetype('/usr/share/fonts/truetype/unfonts-core/UnDinaru.ttf', 12)
    prevTimeStamp = time.time() # 이전 측정 timestamp 값
    particleCnt = 0
    sendCountdown = 0
    saveCountdown = 0
    while True:
        if ((time.time() - prevTimeStamp > meanInterval) or firstFlag) :
            prevTimeStamp = time.time()
            # 온도 습도 대기압 정보를 읽어온다.
            airInfo['temp'], airInfo['press'], airInfo['hum'] = bme280.readBME280All()
            airInfo['temp'] = round(airInfo['temp'],1)
            airInfo['press'] = round(airInfo['press'],1)
            airInfo['hum'] = round(airInfo['hum'],1)

            if (particleCnt > particleMeanInterval) and sds011.isWorkingMode() :
                particle = sds011.getParticle()
                if particle :
                    airInfo['pm25'], airInfo['pm10'] = particle
                    airInfo['pm25'] = round(airInfo['pm25'],1)
                    airInfo['pm10'] = round(airInfo['pm10'],1)

                particleCnt  = 0
                sds011.setSleep()
                time.sleep(2)
            elif particleCnt == particleMeanInterval :
                sds011.setWork() # sds011을 동작시킨다. 다음 인터벌(60초) 때 측정을 한다.

            if firstFlag :
                sds011.setWork()
                particleCnt = 9
                firstFlag = False

            #측정을 3번 할 때 (3 * 60 = 180초) 1번 서버에 데이터를 전달한다.
            if sendCountdown == sendAirInfoInterval :
                print ("send data..")
                params = urllib.urlencode(airInfo) #URL에 데이터를 실어서 서버로 데이터를 전달.
                conn = urllib.urlopen("http://fastpy003.appspot.com/setAirInfo?%s" % params)
                print (conn.read().decode("utf-8") )
                sendCountdown = 0

            if saveCountdown == saveAirInfoInterval:
                print ("save data..")
                params = urllib.urlencode(airInfo) #URL에 데이터를 실어서 서버로 데이터를 전달.
                conn = urllib.urlopen("http://fastpy003.appspot.com/saveAirInfo?%s" % params)
                print (conn.read().decode("utf-8") )
                saveCountdown = 0

            particleCnt += 1
            sendCountdown += 1
            saveCountdown += 1

        draw.rectangle((0,0,width-1,height-1), outline=1, fill=0) # 테두리 그리기

        top = 3
        labelX = 5
        dataX = 40

        # (labelX, top) 좌표를 기준으로 텍스트를 출력합니다.
        draw.text((labelX, top), u"온도", font=hanFont, fill=255)
        draw.text((labelX, top+20), u"습도", font=hanFont, fill=255)
        draw.text((labelX, top+40), u"대기압", font=hanFont, fill=255)

        draw.text((dataX, top), ":" + str(airInfo['temp']) + "C", font=font, fill=255)
        draw.text((dataX, top+20), ":" + str(round(airInfo['hum'],1)) + "%", font=font, fill=255)
        draw.text((dataX, top+40), ":" + str(round(airInfo['press'],2)), font=font, fill=255)

        # PIL Image 객체를 Bitmap으로 변환합니다.
        disp.image(image)
        # Bitmap 버퍼를 디스플레이 장치로 전송합니다.
        disp.display()

        time.sleep(0.5)

finally:
    disp.clear()
    disp.display()
    sds011.setSleep() # SDS011에 전원이 끊어 집니다.
    time.sleep(1)
    sds011.end()
