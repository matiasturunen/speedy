from .basemod import Basemod
from threading import Thread
from datetime import datetime
from Adafruit_BME280 import *
import pygame, time


class Weather(Basemod):
    _screen = None
    sensor = None

    def _run(self):
        super()._run()
        self._timerInterval = 5.0
        if (self._screen == None):
            from ui import Screen
            self._screen = Screen
            print('set screen')


        self.sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def tick(self):
        degrees = self.sensor.read_temperature()
        pascals = self.sensor.read_pressure()
        hectopascals = pascals / 100
        humidity = self.sensor.read_humidity()

        temp = '{0:4.1f} deg C'.format(degrees)
        pres = '{0:d} hPa'.format(int(hectopascals))
        hum = '{0:d} %'.format(int(humidity))

        self._screen.clear(autoUpdate=False)
        self._screen.text(temp,  
            (5, 5),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 90),
            autoUpdate=False
        )
        self._screen.text(pres,  
            (5, 80),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 90),
            autoUpdate=False
        )
        self._screen.text(hum,  
            (5, 155),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 90),
            autoUpdate=True
        )


    

weather = Weather()