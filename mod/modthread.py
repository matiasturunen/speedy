import threading

class ModThread(threading.Thread):
	def __init__(self, target, name, daemon):
		super(ModThread, self).__init__(name=name, target=target, daemon=daemon)
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def start(self):
		super(ModThread, self).start()

	def stopped(self):
		return self._stop_event.is_set()
