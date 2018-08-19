import RPi.GPIO as GPIO
import time
import sys


class RawPWMServoMotor():
    def __init__(self, pin):
        self._pin = pin
        self._speed = 0
        self._step = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def set_speed(self, val):
        self._speed = val

    def update(self):
        MS = 1 / 1000
        period = 1 / 50

        # Convert the input value from -1 to 1 to an on time from 1 ms (full back) to 2 ms (full forward)
        # TODO figure out why this range was way off. We may have more success with the I2C version.
        on_time = (self._speed + 1) * MS
        off_time = period - on_time

        GPIO.output(self._pin, GPIO.HIGH)
        time.sleep(on_time)
        GPIO.output(self._pin, GPIO.LOW)
        time.sleep(off_time)


if __name__ == '__main__':
    """
    .6 to -.6 seems to be the actual range
    """
    if len(sys.argv) < 2:
        print('enter a speed from -1 to 1')
        sys.exit()
    speed = float(sys.argv[1])

    motor = RawPWMServoMotor(12)
    motor.set_speed(speed)
    try:
        while True:
            motor.update()
    except KeyboardInterrupt:
        GPIO.cleanup()
