import defines
from stepper_motor import StepperMotor, StepperMotorDirection  # noqa: 402


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

    # Control Stuff!