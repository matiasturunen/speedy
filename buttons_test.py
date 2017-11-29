import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

btnlist = (12,13,15,16)
GPIO.setup(btnlist, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
	while True:
		for btn in btnlist:
			button_state = GPIO.input(btn)
			if (button_state == False):
				if (btn == 12):
					print('Button 4')
				if (btn == 13):
					print('Button 3')
				if (btn == 15):
					print('Button 2')
				if (btn == 16):
					print('Button 1')
except:
	GPIO.cleanup()
	print('cleanup')
