import threading
import time
from threading import Thread

class Basemod:
    _running = False
    _thread_stop_event = None
    _thread = None
    _startTime = None
    _timerRunning = False
    _timerInterval = 0.5

    def __init__(self):
        self._thread_stop_event = threading.Event()

    def start(self):
        print('Mod starting')
        self._running = True
        self._run()

    def stop(self):
        print('Mod stopping')
        self._running = False
        self._thread.join()
        self._timerRunning = False

    def tick(self):
        pass

    def _clockloop(self, stop_event):
        while self._timerRunning and not stop_event.wait(self._timerInterval):
            self.tick()

    def _run(self):
        print('Mod run')
        self._thread = Thread(
            target=self._clockloop,
            daemon=True,
            args=(self._thread_stop_event,) # Magic comma for python tuples
        )
        self._timerRunning = True
        self._thread.start()

    def _stop(self):
        print('Basemod stop')

    @property
    def thread_stop_event(self):
        return self._thread_stop_event

    @property
    def thread(self):
        return self._thread
    