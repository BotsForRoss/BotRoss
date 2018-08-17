import RPi.GPIO as GPIO


def Switch():
    def __init__(self, in_channel):
        self._in = in_channel

        GPIO.setMode(GPIO.BOARD)
        GPIO.setup(self._in, GPIO.IN)

    def get_state(self):
        return GPIO.input(self._in)
