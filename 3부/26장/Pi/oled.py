#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import bme280

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# Python Image Library를 임포트 합니다.
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 라즈베리 파이와 연결된 BCM 핀번호를 선언합니다.
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# SPI를 사용하는 128x64 해상도 디스플레이를 선언합니다.
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 라이브러리를 초기화
disp.begin()

# 디스플레이를 클리어 해줍니다.
disp.clear()
disp.display()

width = disp.width
height = disp.height
# 디스플레이와 같은 사이즈(128x64)의 흑백 (1bit) PIL Image 객체를 생성합니다.
image = Image.new('1', (width, height))

# 이미지를 그리기위한 draw 객체를 가져옵니다. 일종의 캔버스라고 생각하면 됩니다.
draw = ImageDraw.Draw(image)

try:
    while True:
        # 캔버스에 1픽셀 두께의 사각형을 그리고 내부는 0 (검은색)으로 칠해줍니다.
        draw.rectangle((0,0,width-1,height-1), outline=1, fill=0)

        # 트루 타입 폰트를 로딩합니다. 폰트 사이즈는 15입니다.
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 15)
        # 트루 타입 한글 폰트
        hanFont = ImageFont.truetype('/usr/share/fonts/truetype/unfonts-core/UnDinaru.ttf', 12)

        # 온도, 대기압, 습도를 BME280부터 읽어 옵니다.
        temperature,pressure,humidity = bme280.readBME280All()

        top = 3
        labelX = 5
        dataX = 40

        # (labelX, top) 좌표를 기준으로 텍스트를 출력합니다.
        draw.text((labelX, top), u"온도", font=hanFont, fill=255)
        draw.text((labelX, top+20), u"습도", font=hanFont, fill=255)
        draw.text((labelX, top+40), u"대기압", font=hanFont, fill=255)

        draw.text((dataX, top), ":" + str(temperature) + "C", font=font, fill=255)
        draw.text((dataX, top+20), ":" + str(round(humidity,1)) + "%", font=font, fill=255)
        draw.text((dataX, top+40), ":" + str(round(pressure,2)), font=font, fill=255)

        # PIL Image 객체를 Bitmap으로 변환합니다.
        disp.image(image)
        # Bitmap 버퍼를 디스플레이 장치로 전송합니다.
        disp.display()
        time.sleep(3)
finally:
    disp.clear()
    disp.display()
