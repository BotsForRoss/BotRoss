import defines
import RPi.GPIO as GPIO

from stepper_motor import StepperMotor
from xbox import Joystick


class AnalogStickAxisBinding():
    MAX_FREQUENCY = 10  # Hz
    FOREVER = 2048

    def __init__(self, stick_axis, stepper_motor):
        self._stick_axis = stick_axis
        self._stepper_motor = stepper_motor

    def _analog_to_motor_input(self, val):
        """
        Convert an analog (stick) input to a stepper_motor command

        Arguments:
            val {float} -- the analog stick input from -1 to 1

        Returns:
            (freq {float}, goal {int}) -- the frequency and goal to set the motor to
        """

        freq = abs(val * self.MAX_FREQUENCY)
        goal = self.FOREVER if val > 0 else -self.FOREVER
        return freq, goal

    def update(self, log=False):
        """
        Update the stepper motor to react to the current analog stick input

        Returns:
            (stick {float}, (freq {float}, goal {int})) -- the input from the stick axis and output to the motor
        """
        val = self._stick_axis()
        freq, goal = self._analog_to_motor_input(val)
        self._stepper_motor.set_stepper(freq, goal)
        if log:
            print('\rstick: {0:.3f}\tfreq: {0:.3f}\tgoal: {}'.format(val, freq, goal))
        return (val, (freq, goal))


def control_with_xbox():
    # init controller
    xbox = Joystick()

    # init motors
    stepper_motor_x = StepperMotor(
        defines.STEPPER_X_1,
        defines.STEPPER_X_2,
        defines.STEPPER_X_3,
        defines.STEPPER_X_4
    )
    stepper_motor_y_left = StepperMotor(
        defines.STEPPER_Y_LEFT_1,
        defines.STEPPER_Y_LEFT_2,
        defines.STEPPER_Y_LEFT_3,
        defines.STEPPER_Y_LEFT_4
    )
    # stepper_motor_y_right = StepperMotor(
    #     defines.STEPPER_Y_RIGHT_1,
    #     defines.STEPPER_Y_RIGHT_2,
    #     defines.STEPPER_Y_RIGHT_3,
    #     defines.STEPPER_Y_RIGHT_4
    # )
    # stepper_motor_z = StepperMotor(
    #     defines.STEPPER_Z_1,
    #     defines.STEPPER_Z_2,
    #     defines.STEPPER_Z_3,
    #     defines.STEPPER_Z_4
    # )

    # bind the controller inputs to motors
    x_binding = AnalogStickAxisBinding(xbox.leftX, stepper_motor_x)
    y_binding = AnalogStickAxisBinding(xbox.leftY, stepper_motor_y_left)

    while not xbox.Back():  # "Back" is the select button
        for binding in [x_binding, y_binding]:
            binding.update(log=True)

    xbox.close()
    GPIO.cleanup()


if __name__ == '__main__':
    control_with_xbox()
