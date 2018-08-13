import argparse
import RPi.GPIO as GPIO
import time
import threading
import math

from enum import Enum


class StepperMotorDirection(Enum):
    FORWARD = 1
    REVERSE = -1

    def __int__(self):
        return self.value


class StepperMotor:
    def __init__(self, out1, out2, out3, out4):
        self._i = 0  # The current position in step cycle

        self._timer = None
        self._last_update_time = 0

        self._out1 = out1
        self._out2 = out2
        self._out3 = out3
        self._out4 = out4
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._out1, GPIO.OUT)
        GPIO.setup(self._out2, GPIO.OUT)
        GPIO.setup(self._out3, GPIO.OUT)
        GPIO.setup(self._out4, GPIO.OUT)

    def set_stepper(self, frequency, goal):
        """
        Sets the frequency of steps and number of steps to be taken, and then starts the stepper
            motor

        Arguments:
            frequency {float} -- The frequency at which the stepper motor should step (Hz)
            goal {int} -- The number of steps desired
        """
        # Stop the current timer
        if self._timer:
            self._timer.cancel()

        # If the motor is going to move, call _start_stepper
        if frequency != 0 and goal != 0:
            self._start_stepper(frequency, goal)

    def _start_stepper(self, frequency, goal):
        """
        Starts the stepping feedback loop

        Arguments:
            frequency {float} -- The frequency at which the stepper motor should step (Hz)
            goal {int} -- The number of steps desired
        """
        # For scope and such
        direction = None
        if goal > 0:
            direction = StepperMotorDirection.FORWARD
        else:
            direction = StepperMotorDirection.REVERSE

        period = 1 / frequency

        # Set up the new repeating timer and step if appropriate
        time_since_last_update = time.time() - self._last_update_time
        if time_since_last_update >= period:
            # If it has not stepped for a period longer than the new update period, step and start the repeating timer
            self._step_and_reset_timer(period, 0, goal, direction)
        else:
            # If it's not time to step yet, set the timer to wait for the remaining time then repeat for the regular
            # period
            self._timer = threading.Timer(period - time_since_last_update,
                                          lambda: self._step_and_reset_timer(period, 0, goal, direction))
            self._timer.start()

    def _step_and_reset_timer(self, period, current_step, goal, direction):
        """
        Step the motor once and set a timer to call this function again

        Arguments:
            period {float} -- the time between steps

        Keyword Arguments:
            direction {StepperMotorDirection} -- what direction the motor should go
                (default: {StepperMotorDirection.FORWARD})
        """
        self.step(direction)
        current_step += int(direction)
        self._last_update_time = time.time()
        if math.fabs(goal - current_step) > 0:
            self._timer = threading.Timer(period, lambda: self._step_and_reset_timer(period, current_step,
                                                                                     goal, direction))
            self._timer.start()

    def calibrate(self):
        # How does one calibrate?
        pass

    def step(self, direction=StepperMotorDirection.FORWARD):
        """
        Step the motor once

        Keyword Arguments:
            direction {StepperMotorDirection} -- what direction the motor should go
                (default: {StepperMotorDirection.FORWARD})
        """
        self._i += direction.value
        if self._i == -1:
            self._i = 7
        elif self._i == 8:
            self._i = 0

        if self._i == 0:
            GPIO.output(self._out1, GPIO.HIGH)
            GPIO.output(self._out2, GPIO.LOW)
            GPIO.output(self._out3, GPIO.LOW)
            GPIO.output(self._out4, GPIO.LOW)
        elif self._i == 1:
            GPIO.output(self._out1, GPIO.HIGH)
            GPIO.output(self._out2, GPIO.HIGH)
            GPIO.output(self._out3, GPIO.LOW)
            GPIO.output(self._out4, GPIO.LOW)
        elif self._i == 2:
            GPIO.output(self._out1, GPIO.LOW)
            GPIO.output(self._out2, GPIO.HIGH)
            GPIO.output(self._out3, GPIO.LOW)
            GPIO.output(self._out4, GPIO.LOW)
        elif self._i == 3:
            GPIO.output(self._out1, GPIO.LOW)
            GPIO.output(self._out2, GPIO.HIGH)
            GPIO.output(self._out3, GPIO.HIGH)
            GPIO.output(self._out4, GPIO.LOW)
        elif self._i == 4:
            GPIO.output(self._out1, GPIO.LOW)
            GPIO.output(self._out2, GPIO.LOW)
            GPIO.output(self._out3, GPIO.HIGH)
            GPIO.output(self._out4, GPIO.LOW)
        elif self._i == 5:
            GPIO.output(self._out1, GPIO.LOW)
            GPIO.output(self._out2, GPIO.LOW)
            GPIO.output(self._out3, GPIO.HIGH)
            GPIO.output(self._out4, GPIO.HIGH)
        elif self._i == 6:
            GPIO.output(self._out1, GPIO.LOW)
            GPIO.output(self._out2, GPIO.LOW)
            GPIO.output(self._out3, GPIO.LOW)
            GPIO.output(self._out4, GPIO.HIGH)
        elif self._i == 7:
            GPIO.output(self._out1, GPIO.HIGH)
            GPIO.output(self._out2, GPIO.LOW)
            GPIO.output(self._out3, GPIO.LOW)
            GPIO.output(self._out4, GPIO.HIGH)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run a stepper motor test')
    parser.add_argument('--freq', type=float, default=10, help='frequency of stepping')
    parser.add_argument('--goal', type=int, default=100, help='number of steps desired')
    args = parser.parse_args()

    freq = args.freq
    goal = args.len

    sp1 = StepperMotor(
        out1=31,
        out2=35,
        out3=33,
        out4=37
    )

    sp1.set_stepper(freq, goal)
