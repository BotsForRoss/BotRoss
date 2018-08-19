from smbus2 import SMBus


class ServoMotor():
    """
    A class to operate the SparkFun Pi Servo HAT and the PCA9685 LED controller inside.
    - Sparkfun page:  https://www.sparkfun.com/products/14328
    - Datasheet:      https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf
    - Software guide: https://learn.sparkfun.com/tutorials/pi-servo-hat-hookup-guide#software---python
    """

    def __init__(self, bus, addr):
        self._bus = bus
        self.addr = addr
        self._configure()

    def _configure(self):
        """
        Configure the motor by writing to the i2c bus
        """
        # Enable auto-increment. The control register is automatically incremented after a read or write, allowing us
        # to program the registers sequentially.
        self._bus.write_byte_data(self.addr, 0, 0b00100000)

        # Set the PWM prescalar to its default value of 200 Hz (this makes the pulse period 5 ms)
        self._bus.write_byte_data(self.addr, 0xfe, 0x1e)

    def set_led_output(self, channel, on_time, off_time):
        """
        Configure the LED output and PWM control of the PCA9685.

        on_time and off_time range from 0 to 4095 with a unit of 5 / 4095 ms (for the default frequency of 200 Hz)

        Arguments:
            channel {int} -- the LED channel to set in the range [0, 15]
            on_time {int} -- the time in the PWM period that the LED output is asserted high
            off_time {int} -- the time in the PWM period that the LED output is negated

        Raises:
            ValueError -- if the channel, on_time, or off_time are out of range
        """
        if on_time > off_time or off_time > 4095 or on_time < 0 or off_time < 0:
            raise ValueError('invalid on_time/off_time range ({}, {})'.format(on_time, off_time))
        if channel < 0 or channel >= 16:
            raise ValueError('channel {} not in range [0, 16)'.format(channel))

        # Determine the control registers for this channel
        on_addr = 0x06 + channel * 4
        off_addr = on_addr + 2

        self._bus.write_word_data(self.addr, on_addr, on_time)  # Set the ON time
        self._bus.write_word_data(self.addr, off_addr, off_time)  # Set the OFF time

    def set_duty_cycle(self, channel, duty_cycle):
        """
        Set the duty cycle of an LED on the PCA9685.

        Arguments:
            channel {int} -- the LED channel to set in the range [0, 15]
            duty_cycle {int} -- from 0 to 4095, where 4095 is 100% duty cycle
        """
        self.set_led_output(channel, 0, duty_cycle)

    def set_angle(self, channel, angle):
        """
        Set the angle of the motor. It's actually a speed, but okay.

        Arguments:
            channel {int} -- the LED channel to set in the range [0, 15]
            angle {float} -- the angle to set the motor to, in degrees. Sparkfun suggests the range is [-90, 90].
        """
        duty_cycle_raw = round(1250 - 4.6 * angle)
        self.set_duty_cycle(channel, duty_cycle_raw)

    def set_speed(self, channel, speed):
        """
        Set the speed

        Arguments:
            channel {int}
            speed {float}
        """
        self.set_angle(channel, speed * 90)


if __name__ == '__main__':
    bus = SMBus(1)  # using i2c bus 1
    servo_motor = ServoMotor(bus, addr=0x40)
    servo_motor.set_angle(0, -45)
    bus.close()
