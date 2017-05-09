#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
from flask import redirect, render_template, request, url_for, Flask, current_app
from air import getAirInfoList, saveAirInfoList, clearAirInfoList
import json

#테스트
app = Flask(__name__)
app.debug = True     #debug mode

latestAirInfo = {'pm25': 0.0, 'pm10': 0.0, 'temp': 0.0, 'hum':0, 'press':0}

@app.route('/')
def home():
    # 최근 7일간의 데이터를 가져와 템플릿 파일이 렌더링 될 때 JS Object 형태로 삽입함.
    return render_template("home.html", 
        jsonAirInfoList = getAirInfoList(7)) 

@app.route('/getLatestAirInfo', methods=['GET'])
def getLatestAirInfo():
    #현재 서버에 저장되어 있는 미세먼지, 초미세 먼지, 온도, 습도, 기압 정보를 JSON형태로 출력함.
    if request.method == 'GET':
        return json.dumps(latestAirInfo)
    return "error"

@app.route('/setAirInfo', methods=['GET'])
def setAirInfo():
    # 공기 측정 결과를 서버에 저장 - 라즈베리 파이에서 요청
    if request.method == 'GET':
        data = request.args.to_dict(flat=True)
        latestAirInfo['pm25'] = data['pm25']
        latestAirInfo['pm10'] = data['pm10']
        latestAirInfo['temp'] = data['temp']
        latestAirInfo['hum'] = data['hum']
        latestAirInfo['press'] = data['press']
    return "success"

@app.route('/saveAirInfo', methods=['GET'])
def saveAirInfo():
    # 공기 측정 결과를 Google Cloud Datasotre에 저장
    if request.method == 'GET':
        data = request.args.to_dict(flat=True)
        return str(saveAirInfoList(data))


@app.route('/clearAirInfo', methods=['GET'])
def clearAirInfo():
    # 모든 데이터를 삭제.
    if request.method == 'GET':
        clearAirInfoList()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
# [END app]
