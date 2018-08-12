from smbus2 import SMBus


class ServoMotor():
    def __init__(self, bus, addr):
        self.bus = bus
        self.addr = addr

    def _configure(self):
        """
        Configure the motor by writing to the i2c bus
        """
        # Sets it up for incrementing address after write
        bus.write_byte_data(self.addr, 0, 0x20)
        bus.write_byte_data(self.addr, 0xfe, 0x1e)

    def do_something(self):
        """
        Not sure what this actually does. Copied from here:
        https://learn.sparkfun.com/tutorials/pi-servo-hat-hookup-guide#software---python
        """
        # Write data to PWM chip
        bus.write_word_data(self.addr, 0x06, 0)
        bus.write_word_data(self.addr, 0x08, 1250)


if __name__ == '__main__':
    bus = SMBus(1)  # using i2c bus 1
    servo_motor = ServoMotor(bus, addr=0x40)
    servo_motor.do_something()
