import threading

class Basemod:
    _running = False
    _thread_stop_event = None
    _thread = None

    def __init__(self):
        self._thread_stop_event = threading.Event()

    def start(self):
        print('Mod starting')
        self._running = True
        self._run()

    def stop(self):
        print('Mod stopping')
        self._running = False
        self._stop()

    def _run(self):
        print('Basemod run')

    def _stop(self):
        print('Basemod stop')

    @property
    def thread_stop_event(self):
        return self._thread_stop_event

    @property
    def thread(self):
        return self._thread
    