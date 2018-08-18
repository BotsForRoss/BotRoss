import defines
from stepper_motor import StepperMotor, StepperMotorDirection  # noqa: 402
from switch import Switch


class BrushCNC():
    def __init__(self):
        self._stepper_x = StepperMotor(
            defines.STEPPER_X_1,
            defines.STEPPER_X_2,
            defines.STEPPER_X_3,
            defines.STEPPER_X_4
        )
        self._stepper_y_left = StepperMotor(
            defines.STEPPER_Y_LEFT_1,
            defines.STEPPER_Y_LEFT_2,
            defines.STEPPER_Y_LEFT_3,
            defines.STEPPER_Y_LEFT_4
        )
        self._stepper_y_right = StepperMotor(
            defines.STEPPER_Y_RIGHT_1,
            defines.STEPPER_Y_RIGHT_2,
            defines.STEPPER_Y_RIGHT_3,
            defines.STEPPER_Y_RIGHT_4
        )
        self._stepper_z = StepperMotor(
            defines.STEPPER_Z_1,
            defines.STEPPER_Z_2,
            defines.STEPPER_Z_3,
            defines.STEPPER_Z_4
        )
        self._switch_reset_x = Switch(defines.SWITCH_RESET_X)
        self._switch_reset_y = Switch(defines.SWITCH_RESET_Y)
        self._switch_reset_z = Switch(defines.SWITCH_RESET_Z)

    def zeroing(self):
        """
        Uses the limit switches for each of the motors to bring them all back to a zeroed position
        """
        x_zeroed, y_zeroed, z_zeroed = False, False, False
        self._stepper_x.set_stepper(defines.STEPPER_X_MAX_HZ / 2, -defines.BOARD_X_LENGTH)
        self._stepper_y_left.set_stepper(defines.STEPPER_Y_MAX_HZ / 2, -defines.BOARD_Y_LENGTH)
        self._stepper_y_right.set_stepper(defines.STEPPER_Y_MAX_HZ / 2, -defines.BOARD_Y_LENGTH)
        self._stepper_z.set_stepper(defines.STEPPER_Z_MAX_HZ / 2, -defines.BOARD_Z_LENGTH)

        while x_zeroed is False or y_zeroed is False or z_zeroed is False:
            if x_zeroed is False and self._switch_reset_x.get_state() is True:
                self._stepper_x.set_stepper(0, 0)
                self._stepper_x.zero()
                x_zeroed = True

            if y_zeroed is False and self._switch_reset_y.get_state() is True:
                self._stepper_y_left.set_stepper(0, 0)
                self._stepper_y_right.set_stepper(0, 0)
                self._stepper_y_left.zero()
                self._stepper_y_right.zero()
                y_zeroed = True

            if z_zeroed is False and self._switch_reset_z.get_state() is True:
                self._stepper_z.set_stepper(0, 0)
                self._stepper_z.zero()
                z_zeroed = True
