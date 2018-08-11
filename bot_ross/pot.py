# include RPi libraries in to Python code
import RPi.GPIO as GPIO
import time


class Pot():
    def __init__(self, a, b):
        # define GPIO pins with variables a_pin and b_pin
        self.a_pin = a
        self.b_pin = b

    # create discharge function for reading capacitor data
    def discharge(self):
        GPIO.setup(self.a_pin, GPIO.IN)
        GPIO.setup(self.b_pin, GPIO.OUT)
        GPIO.output(self.b_pin, False)
        time.sleep(0.005)

    # create time function for capturing analog count value
    def charge_time(self):
        GPIO.setup(self.b_pin, GPIO.IN)
        GPIO.setup(self.a_pin, GPIO.OUT)
        count = 0
        GPIO.output(self.a_pin, True)
        while not GPIO.input(self.b_pin):
            count = count +1
        return count

    # create analog read function for reading charging and discharging data
    def analog_read(self):
        self.discharge()
        return self.charge_time()


if __name__ == '__main__':
    pot = Pot(a=18, b=23)

    # instantiate GPIO as an object
    GPIO.setmode(GPIO.BCM)

    # provide a loop to display analog data count value on the screen
    while True:
        print(pot.analog_read())
        time.sleep(1)
