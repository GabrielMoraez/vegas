#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  watson_text_talker.py
#
#  Copyright 2018 Jeff Greenberg
#
#  MIT License
#
#  Text-to-Speech Interface using IBM's Watson Cloud based Text to Speech
#
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('2b53c9935a2de033ebda5ea719d0bdc4')
mgr = owm.weather_manager()

class Weather:

  @staticmethod
  def getWeather (location):
    # Search for current weather in London (Great Britain) and get details
    observation = mgr.weather_at_place(location)
    w = observation.weather

    w.detailed_status         # 'clouds'
    w.wind()                  # {'speed': 4.6, 'deg': 330}
    w.humidity                # 87
    w.temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    w.rain                    # {}
    w.heat_index              # None
    w.clouds                  # 75

    print(w.temperature('celsius'))
    return {w.detailed_status}

  @staticmethod
  def getCurrentTemperature (location):
    observation = mgr.weather_at_place(location)
    w = observation.weather

    return w.temperature('celsius')

  @staticmethod
  def getForecast (location, time):
    # Will it be clear tomorrow at this time in Milan (Italy) ?
    forecast = mgr.forecast_at_place('Milan,IT', 'daily')
    answer = forecast.will_be_clear_at(timestamps.tomorrow())

    print(answer)
