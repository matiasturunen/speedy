import gc
from mod.basemod import Basemod
#import mod

def stopModThreads():
	for obj in gc.get_objects():
		if isinstance(obj, Basemod):
			obj.thread_stop_event.set()
			obj.thread.join()
			obj.thread_stop_event.clear()