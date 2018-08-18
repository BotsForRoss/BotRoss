_MAX_FREQUENCY = 10  # Hz
_FOREVER = 4096


def _binding_factory(input_fn, output_fn, converter=None):
    """
    Make a "binding" that takes an input from a function, pipes it through a converter, and outputs it to another
    function

    Arguments:
        input_fn -- a function to take input from
        output_fn -- a function that takes the input as a keyword arguments

    Keyword Arguments:
        converter -- an optional function to do some conversion on the input before sending it to output
            (default: {None})

    Returns:
        A function that takes no arguments and returns a tuple of the input value and the converted value sent to the
        output function
    """
    def update():
        val = input_fn()
        if converter:
            converted = converter(val)
        else:
            converted = val
        output_fn(**converted)
        return val, converted
    return update


def _convert_stick_axis_to_stepper_motor(val, scalar):
    freq = abs(val * scalar)
    goal = _FOREVER if val > 0 else -_FOREVER
    return {
        'frequency': freq,
        'goal': goal
    }


def stick_axis_to_stepper_motor_binding(stick_axis, motor, scalar=_MAX_FREQUENCY):
    """
    Bind an analog stick axis to a stepper motor

    Arguments:
        stick_axis -- a function that returns -1 to 1
        motor {StepperMotor} -- the motor to control

    Keyword Arguments:
        scalar {float} -- a scalar to multiply the axis input by before sending it to the motor (default: {10})

    Returns:
        A function that takes no arguments but will update the motor based on the axis input
    """
    return _binding_factory(stick_axis, motor.set_stepper,
                            lambda val: _convert_stick_axis_to_stepper_motor(val, scalar))
