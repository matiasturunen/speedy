from .basemod import Basemod
from queue import Empty
import pygame, time
import math

class Speed(Basemod):
    _screen = None
    _GPSQueue = None

    def start(self, kwargs):
        if ('gpsqueue' in kwargs.keys()):
            self._GPSQueue = kwargs['gpsqueue']
        super().start()


    def _run(self):
        super()._run()
        if (self._screen == None):
            from ui import Screen
            self._screen = Screen
            print('set screen')

    def tick(self):
        spd = 0
        dist = 0

        try:
            info = self._GPSQueue.get(timeout=1)
            spd = info.speed
            dist = info.distance
        except Empty:
            #print('Empty queue')
            pass
        except Exception as e:
            pass
            
        
        self._screen.clear(autoUpdate=False)
        self._screen.text(str(round(spd, 1)) + ' m/s', 
            (25, 70),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 100)
        )


speed = Speed()
