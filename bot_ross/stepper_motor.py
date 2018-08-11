import os
if hasattr(os, "uname") and os.uname().nodename == "raspberrypi":
    import RPi.GPIO as GPIO
else:
    import MockRPI.GPIO as GPIO
import time
import math

class StepperMotor:
    self._DT = 0.1 #The time delay between steps
    self.i = 0 #The current step

    def __init__(self, out1, out2, out3, out4):
        """ 
        """
        self._out1 = out1
        self._out2 = out2
        self._out3 = out3
        self._out4 = out4
        GPIO.setup(self._out1, GPIO.OUT)
        GPIO.setup(self._out2, GPIO.OUT)
        GPIO.setup(self._out3, GPIO.OUT)
        GPIO.setup(self._out4, GPIO.OUT)

    def calibrate(self):
        #How does one calibrate?

    def step(self, steps):
        """
        """
        direction = steps / math.fabs(steps)
        for x in range(0, steps, -direction):
            self.i += direction
            if self.i == -1:
                self.i = 7
            elif self.i == 8:
                self.i = 0

            if self.i == 0:
                GPIO.output(self._out1, GPIO.HIGH)
                GPIO.output(self._out2, GPIO.LOW)
                GPIO.output(self._out3, GPIO.LOW)
                GPIO.output(self._out4, GPIO.LOW)
            elif self.i == 1:
                GPIO.output(self._out1, GPIO.HIGH)
                GPIO.output(self._out2, GPIO.HIGH)
                GPIO.output(self._out3, GPIO.LOW)
                GPIO.output(self._out4, GPIO.LOW)
            elif self.i == 2:  
                GPIO.output(self._out1, GPIO.LOW)
                GPIO.output(self._out2, GPIO.HIGH)
                GPIO.output(self._out3, GPIO.LOW)
                GPIO.output(self._out4, GPIO.LOW)
            elif self.i == 3:    
                GPIO.output(self._out1, GPIO.LOW)
                GPIO.output(self._out2, GPIO.HIGH)
                GPIO.output(self._out3, GPIO.HIGH)
                GPIO.output(self._out4, GPIO.LOW)
            elif self.i == 4:  
                GPIO.output(self._out1, GPIO.LOW)
                GPIO.output(self._out2, GPIO.LOW)
                GPIO.output(self._out3, GPIO.HIGH)
                GPIO.output(self._out4, GPIO.LOW)
            elif self.i == 5:
                GPIO.output(self._out1,GPIO.LOW)
                GPIO.output(self._out2,GPIO.LOW)
                GPIO.output(self._out3,GPIO.HIGH)
                GPIO.output(self._out4,GPIO.HIGH)
            elif self.i == 6:    
                GPIO.output(self._out1, GPIO.LOW)
                GPIO.output(self._out2, GPIO.LOW)
                GPIO.output(self._out3, GPIO.LOW)
                GPIO.output(self._out4, GPIO.HIGH)
            elif self.i == 7:    
                GPIO.output(self._out1, GPIO.HIGH)
                GPIO.output(self._out2, GPIO.LOW)
                GPIO.output(self._out3, GPIO.LOW)
                GPIO.output(self._out4, GPIO.HIGH)    
            
            time.sleep(self._DT)

    