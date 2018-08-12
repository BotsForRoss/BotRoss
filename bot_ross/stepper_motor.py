import argparse
import RPi.GPIO as GPIO
import time
import threading

from enum import Enum


class StepperMotorDirection(Enum):
    FORWARD = 1
    REVERSE = -1


class StepperMotor:
    def __init__(self, out1, out2, out3, out4):
        self.i = 0  # The current step
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

    def set_frequency(self, frequency, direction=StepperMotorDirection.FORWARD):
        """
        Set the frequency at which the stepper motor steps

        Arguments:
            frequency {float} -- The frequency at which the stepper motor should step (Hz)

        Keyword Arguments:
            direction {StepperMotorDirection} -- what direction the motor should go
                (default: {StepperMotorDirection.FORWARD})
        """
        # Stop the current timer
        if self._timer:
            self._timer.cancel()

        # If we're trying to stop, just don't set another timer
        if frequency == 0:
            return

        period = 1 / frequency

        # Set up the new repeating timer and step if appropriate
        time_since_last_update = time.time() - self._last_update_time
        if time_since_last_update >= period:
            # If it has not stepped for a period longer than the new update period, step and start the repeating timer
            self._step_and_reset_timer(period, direction)
        else:
            # If it's not time to step yet, set the timer to wait for the remaining time then repeat for the regular
            # period
            self._timer = threading.Timer(period - time_since_last_update,
                                          lambda: self._step_and_reset_timer(period, direction))
            self._timer.start()

    def _step_and_reset_timer(self, period, direction=StepperMotorDirection.FORWARD):
        """
        Step the motor once and set a timer to call this function again

        Arguments:
            period {float} -- the time between steps

        Keyword Arguments:
            direction {StepperMotorDirection} -- what direction the motor should go
                (default: {StepperMotorDirection.FORWARD})
        """
        self.step(direction=direction)
        self._last_update_time = time.time()
        self._timer = threading.Timer(period, lambda: self._step_and_reset_timer(period, direction))
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
        self.i += direction.value
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
    parser.add_argument('--freq', type=float, default=10, help='frequency of stepping')
    parser.add_argument('--len', type=int, default=10, help='how long to run it (seconds)')
    parser.add_argument('--dir', type=int, default=1, help='direction (1 for forward, -1 for reverse)')
    args = parser.parse_args()

    freq = args.freq
    test_duration = args.len
    direction = StepperMotorDirection(args.dir)

    sp1 = StepperMotor(
        out1=31,
        out2=35,
        out3=33,
        out4=37
    )

    sp1.set_frequency(freq, direction=direction)
    time.sleep(test_duration)
    sp1.set_frequency(0)
