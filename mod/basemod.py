class Basemod:
    _running = False

    def start(self):
        self._running = True
        self._run()

    def stop(self):
        self._running = False
        self._stop()

    def _run(self):
        print('Basemod run')

    def _stop(self):
        print('Basemod stop')