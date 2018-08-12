import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
count = 1
while True:
    input_state = GPIO.input(18)
    if input_state is False:
        print('fuck', count)
        count += 1
        time.sleep(0.2)
    
