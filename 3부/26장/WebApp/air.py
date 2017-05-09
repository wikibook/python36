# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from datetime import datetime, timedelta
from decimal import Decimal
import time
import json

class airInfo(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    temp = ndb.FloatProperty()
    press = ndb.FloatProperty()
    hum = ndb.FloatProperty()
    pm25 = ndb.FloatProperty()
    pm10 = ndb.FloatProperty()

def toDictFromNDB(p) :
    return { 'temp': str(p['temp']), 'pm10' : str(p['pm10']),\
        'pm25': str(p['pm25']), 'hum':str(p['hum']), 'press':str(p['press']),\
        'date':(p['date']+timedelta(hours=9)).strftime("%Y-%m-%d %H:%M %Z") }

def getAirInfoList(period):
    dt = datetime.now()
    td = timedelta(days=period)

    airInfos = airInfo.query().order(airInfo.date).filter(airInfo.date > (dt-td)).fetch()
    return json.JSONEncoder().encode([toDictFromNDB(p.to_dict()) for p in airInfos])

def saveAirInfoList(data):
    airinfo = airInfo()
    airinfo.pm10 = float(data['pm10'])
    airinfo.pm25 = float(data['pm25'])
    airinfo.temp = float(data['temp'])
    airinfo.hum = float(data['hum'])
    airinfo.press = float(data['press'])

    airinfo_key = airinfo.put()
    return airinfo_key.id()

def clearAirInfoList():
    ndb.delete_multi(airInfo.query().fetch(keys_only=True))
