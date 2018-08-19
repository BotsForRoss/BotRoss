import defines
import RPi.GPIO as GPIO

from stepper_motor import StepperMotor
from raw_pwm_servo_motor import RawPWMServoMotor
from xbox import Joystick
from xbox_bindings import stick_axis_to_stepper_motor_binding


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
    stepper_motor_z = StepperMotor(
        defines.STEPPER_Z_1,
        defines.STEPPER_Z_2,
        defines.STEPPER_Z_3,
        defines.STEPPER_Z_4
    )

    servo_motor = RawPWMServoMotor(12)

    # bind the controller inputs to motors
    x_binding = stick_axis_to_stepper_motor_binding(xbox.leftX, stepper_motor_x)
    y_binding = stick_axis_to_stepper_motor_binding(xbox.leftY, stepper_motor_y_left)
    z_binding = stick_axis_to_stepper_motor_binding(xbox.rightY, stepper_motor_z)

    while not xbox.Back():  # "Back" is the select button
        x_in, x_out = x_binding()
        y_in, y_out = y_binding()
        z_in, z_out = z_binding()
        servo_motor.set_speed(xbox.rightY())
        servo_motor.update()
        print(
            'stick: {:.3f}/{:.3f}/{:.3f}\tfreq: {:.3f}/{:.3f}/{:.3f}\tgoal: {:5d}/{:5d}/{:5d}'.format(
                x_in, y_in, z_in,
                x_out['frequency'], y_out['frequency'], z_out['frequency'],
                x_out['goal'], y_out['goal'], z_out['goal']
            ),
            end='\r'
        )

    xbox.close()
    GPIO.cleanup()


if __name__ == '__main__':
    control_with_xbox()
