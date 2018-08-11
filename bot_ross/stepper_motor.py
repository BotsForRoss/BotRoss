import argparse
import os
import RPi.GPIO as GPIO
import time
import math

class StepperMotor:
    def __init__(self, out1, out2, out3, out4, dt=0.1, forward=True):
        self._DT = dt  # The time delay between steps
        self.i = 0  # The current step
        self._last_update = time.time()
        self._direction = 1 if forward else -1
        self._out1 = out1
        self._out2 = out2
        self._out3 = out3
        self._out4 = out4
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._out1, GPIO.OUT)
        GPIO.setup(self._out2, GPIO.OUT)
        GPIO.setup(self._out3, GPIO.OUT)
        GPIO.setup(self._out4, GPIO.OUT)

    def calibrate(self):
        # How does one calibrate?
        pass

    def update(self):
        current_dt = time.time() - self._last_update
        if current_dt >= self._DT:
            step(direction=self._direction)
            self._last_update = time.time()

    def step(self, direction=1):
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
            GPIO.output(self._out1, GPIO.LOW)
            GPIO.output(self._out2, GPIO.LOW)
            GPIO.output(self._out3, GPIO.HIGH)
            GPIO.output(self._out4, GPIO.HIGH)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run a stepper motor test')
    parser.add_argument('--dt', type=float, default=0.1, help='how fast to run it?')
    parser.add_argument('--len', type=int, default=10, help='how long to run it (seconds)')
    args = parser.parse_args()

    dt = args.dt
    test_duration = args.len
    
    sp1 = StepperMotor(
        out1=31,
        out2=33,
        out3=35,
        out4=37,
        dt=dt,
        forward=True
    )

    start_time = time.time()
    while time.time() - start_time < test_duration:
        sp1.update()
