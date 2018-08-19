import argparse
import defines
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
        self._is_complete = True
        self._last_update_time = 0
        self._pos = 0  # where we at

        self._out1 = out1
        self._out2 = out2
        self._out3 = out3
        self._out4 = out4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._out1, GPIO.OUT)
        GPIO.setup(self._out2, GPIO.OUT)
        GPIO.setup(self._out3, GPIO.OUT)
        GPIO.setup(self._out4, GPIO.OUT)

    def set_stepper_absolute(self, frequency, setpoint, wait=False):
        """
        Set the stepper motor's frequency (speed) and desired position

        Arguments:
            frequency {float} -- The frequency at which the stepper motor should step (Hz)
            setpoint {int} -- The absolute position the stepper motor should move towards, in steps

        Keyword Arguments:
            wait {bool} -- True iff the calling thread should wait until the stepper motor has reached the input goal
                (default: {False})
        """
        diff = setpoint - self._pos
        self.set_stepper(frequency, diff, wait=wait)

    def set_stepper(self, frequency, goal, wait=False):
        """
        Sets the frequency of steps and number of steps to be taken, and then starts the stepper
            motor

        Arguments:
            frequency {float} -- The frequency at which the stepper motor should step (Hz)
            goal {int} -- The number of steps desired. Negative means reverse.

        Keyword Arguments:
            wait {bool} -- True iff the calling thread should wait until the stepper motor has reached the input goal
                (default: {False})
        """
        # If stopping, mark complete
        self._is_complete = frequency == 0 or goal == 0

        # Stop the current timer
        if self._timer:
            self._timer.cancel()

        # If the motor is going to move, call _start_stepper
        if not self._is_complete:
            self._start_stepper(frequency, goal)

        if wait:
            self.wait_until_complete()

    def wait_until_complete(self):
        while self._timer and not self._is_complete:
            self._timer.join()

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
                                          self._step_and_reset_timer, args=(period, 0, goal, direction))
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
        self._pos += int(direction)
        self._last_update_time = time.time()
        if math.fabs(goal - current_step) > 0:
            self._timer = threading.Timer(period, self._step_and_reset_timer,
                                          args=(period, current_step, goal, direction))
            self._timer.start()
        else:
            self._is_complete = True

    def zero(self):
        """
        Set the stepper motor's current position as zero
        """
        self._pos = 0

    def step(self, direction=StepperMotorDirection.FORWARD):
        """
        Step the motor once

        Keyword Arguments:
            direction {StepperMotorDirection} -- what direction the motor should go
                (default: {StepperMotorDirection.FORWARD})
        """
        self._i = (self._i + direction.value) % 8

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
    goal = args.goal

    sp1 = StepperMotor(
        out1=defines.STEPPER_Z_1,
        out2=defines.STEPPER_Z_2,
        out3=defines.STEPPER_Z_3,
        out4=defines.STEPPER_Z_4
    )

    try:
        sp1.set_stepper(freq, goal, wait=True)
    finally:
        GPIO.cleanup()
