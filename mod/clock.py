from .basemod import Basemod
from ui import Screen
from threading import Thread
from datetime import datetime
import pygame, time

class Clock(Basemod):
    _startTime = None
    _thread = None
    _timerRunning = False
    _paintInterval = 0.5
    _screen = None

    def _run(self):
        if (not self._thread):
            self._thread = Thread(
                target=self._clockLoop,
                daemon=True
            )
            self._thread.start()
            self._timerRunning = True

        if (self._screen == None):
            self._screen = Screen

    def _clockLoop(self):
        self._showTime()
        time.sleep(self._paintInterval)
        self._clockLoop()

    def _showTime(self):
        print('Time:', datetime.now())
        self._screen.clear()
        self._screen.text('asd', 
            (10, 10),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 40)
        )

    def _stop(self):
        if (self._timerRunning):
            self._thread.join()
        self._timerRunning = False

clock = Clock()
