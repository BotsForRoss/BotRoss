import math
import time

from threading import Thread
from xbox360controller import Xbox360Controller


# The minimum speed (in mm/second) for the machine to accept a move command
_DEFAULT_MINSPEED = 1 / 60.0  # mm/second

# The maximum speed (in mm/second) the machine can move in each axis
_DEFAULT_MAXSPEED = 1  # mm/second

_DEFAULT_NUM_EXTRUDERS = 6
_LED_MODES = [
    Xbox360Controller.LED_OFF,
    Xbox360Controller.LED_BLINK,
    Xbox360Controller.LED_ROTATE,
    Xbox360Controller.LED_ROTATE_TWO
]


class XboxToGcode(Thread):
    """
    Convert xbox 360 controller input to GCode.

    | input       | action       | gcode |
    |------------ |--------------|-------|
    | select      | quit         | N/A   |
    | right stick | X/Y axis     | G0    |
    | triggers    | Z axis       | G0    |
    | right thumb | sprint       | N/A   |
    | home button | go home      | G28   |
    | bumpers     | cycle colors | N/A   |
    | A button    | extrude      | M126  |
    | B button    | unextrude    | M127  |
    | Y button    | blink LED    | N/A   |
    """

    def __init__(self, callback, kill_callback=None, rate=30.0,
                 range_x=(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED),
                 range_y=(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED),
                 range_z=(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED),
                 num_extruders=_DEFAULT_NUM_EXTRUDERS):
        """
        Pipe xbox controller input into gcode output

        Arguments:
            callback {function} -- a function that takes a line of gcode every time the controller updates.
                Returns True iff the callback succeeded.

        Keyword Arguments:
            rate {float} -- the maximum update rate of the controller, in Hz (default: {60.0})
            kill_callback {function} -- a function that will be called immediately when the stop button is pressed
            range_x {(float, float)} -- a tuple of (min speed, max speed) for the range of speeds this should command
                in the x axis, in mm/second
            range_y {(float, float)} -- same as range_x but for the y axis
            range_z {(float, float)} -- same as range_x but for the z axis
            num_extruders {int} -- the number of extruders (default: {6})
        """
        # configuration
        self._send_gcode = callback
        self._send_kill_command = kill_callback
        self._period = 1 / rate
        self._range_x = range_x
        self._range_y = range_y
        self._range_z = range_z
        self._num_extruders = num_extruders

        # state
        self._extruder_id = 0
        self._led_mode = 0
        self._go_home = False  # to capture G28 commands
        self._should_stop = False
        self._is_sprinting = False

        self._controller = Xbox360Controller()
        super().__init__()

    def run(self):
        self._controller.button_select.when_pressed = self._kill
        self._controller.button_trigger_l.when_released = self._use_prev_color
        self._controller.button_trigger_r.when_released = self._use_next_color
        self._controller.button_mode.when_released = self._set_go_home
        self._controller.button_thumb_r.when_pressed = self._set_sprinting
        self._controller.button_thumb_r.when_released = self._clear_sprinting
        self._controller.button_y.when_released = self._use_next_led_mode

        # configure the machine to use relative positioning
        self._send_gcode('G91')

        while not self._should_stop:
            start_time = time.time()

            command = self._get_gcode()
            if command:
                success = self._send_gcode(command)
                if not success:
                    break

            # wait so that the machine is not updated faster than the requested rate
            execution_time = time.time() - start_time
            time_to_wait = self._period - execution_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)

        self._controller.close()

    def _use_next_color(self, _):
        self._extruder_id = (self._extruder_id + 1) % self._num_extruders

    def _use_prev_color(self, _):
        self._extruder_id = (self._extruder_id - 1) % self._num_extruders

    def _use_next_led_mode(self, _):
        self._led_mode = (self._led_mode + 1) % len(_LED_MODES)
        self._controller.set_led(_LED_MODES[self._led_mode])

    def _set_go_home(self, _):
        self._go_home = True

    def _set_sprinting(self, _):
        self._is_sprinting = True

    def _clear_sprinting(self, _):
        self._is_sprinting = False

    def _kill(self, _):
        if self._send_kill_command:
            self._send_kill_command()
        self._should_stop = True

    def _get_gcode(self):
        """
        Get a line of gcode for the current state of the xbox controller, or None if it is inactive.
        """
        # check home button
        if self._go_home:
            self._go_home = False
            return 'G28'

        # check extruder buttons
        if self._controller.button_a.is_pressed:
            return 'M126 T{} P{}'.format(self._extruder_id, self._period)
        if self._controller.button_b.is_pressed:
            return 'M127 T{} P{}'.format(self._extruder_id, self._period)

        # calculate commanded velocity on each axis
        vel_x = self._controller.axis_r.x * self._range_x[1]
        vel_y = self._controller.axis_r.y * self._range_y[1]
        if self._controller.trigger_l.value:
            vel_z = -self._controller.trigger_l.value * self._range_z[1]
        else:
            vel_z = self._controller.trigger_r.value * self._range_z[1]
        if not self._is_sprinting:
            vel_x /= 2.0
            vel_y /= 2.0
            vel_z /= 2.0

        # if any axis is moving fast enough, send a rapid move command
        if abs(vel_x) > self._range_x[0] or abs(vel_y) > self._range_y[0] or abs(vel_z) > self._range_z[0]:
            dx = vel_x * self._period
            dy = vel_y * self._period
            dz = vel_z * self._period
            speed = math.sqrt(vel_x * vel_x + vel_y * vel_y + vel_z * vel_z) * 60.0  # convert to mm/minute
            return 'G0 X{} Y{} Z{} F{}'.format(dx, dy, dz, speed)

        return None


if __name__ == '__main__':
    def do_line(line):
        padding = 80 - len(line)
        if padding > 0:
            line = line + ' ' * padding
        print(line, end='\r')
        return True

    gcode_generator = XboxToGcode(do_line, rate=1.0)
    gcode_generator.start()
    gcode_generator.join()
