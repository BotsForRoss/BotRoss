import RPi.GPIO as GPIO
import time 

out1 = 13
out2 = 11
out3 = 15
out4 = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

print("I aint gonna calibrate SHIT")


try:
    while(1):
        GPIO.output(out1, True)
        GPIO.output(out2, False)
        GPIO.output(out3, False)
        GPIO.output(out4, False)
        time.sleep(0.1)
        GPIO.output(out1, False)
        GPIO.output(out2, True)
        GPIO.output(out3, False)
        GPIO.output(out4, False)
        time.sleep(0.1)
        GPIO.output(out1, False)
        GPIO.output(out2, False)
        GPIO.output(out3, True)
        GPIO.output(out4, False)
        time.sleep(0.1)
        GPIO.output(out1, False)
        GPIO.output(out2, False)
        GPIO.output(out3, False)
        GPIO.output(out4, True)
        time.sleep(0.1)
              
except KeyboardInterrupt:
    GPIO.cleanup()
