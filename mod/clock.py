from .basemod import Basemod

from datetime import datetime
import pygame, time

class Clock(Basemod):
    _screen = None

    def _run(self):
        super()._run()
        if (self._screen == None):
            from ui import Screen
            self._screen = Screen
            print('set screen')

    def tick(self):
        t = datetime.now()
        print('Time:', t)
        self._screen.clear()
        self._screen.text(t.strftime('%H:%M:%S'), 
            (25, 70),
            color=(255,0,0),
            font=pygame.font.SysFont('sans-serif', 100)
        )


clock = Clock()
