from .basemod import Basemod
from threading import Thread
from datetime import datetime
import pygame, time

class Clock(Basemod):
    _startTime = None
    _timerRunning = False
    _paintInterval = 0.5
    _screen = None

    def _run(self):
        if (self._screen == None):
            from ui import Screen
            self._screen = Screen
            print('set screen')
        

        #if (not self._thread):
        print('clock run')
        self._thread = Thread(
            target=self._clockLoop,
            daemon=True,
            args=(self._thread_stop_event,) # Magic comma for python tuples
        )
        self._timerRunning = True
        self._thread.start()


    def _clockLoop(self, stop_event):
        while self._timerRunning and not stop_event.wait(self._paintInterval):
            self._showTime()

    def _showTime(self):
        t = datetime.now()
        print('Time:', t)
        self._screen.clear()
        self._screen.text(t.strftime('%H:%M:%S'), 
            (25, 70),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 100)
        )

    def _stop(self):
        self._thread.join()
        self._timerRunning = False
    

clock = Clock()
