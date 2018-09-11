import math
import time

from enum import Enum
from threading import Thread
from xbox360controller import Xbox360Controller


# The minimum speed (in mm/second) for the machine to accept a move command
_DEFAULT_MINSPEED = 1 / 60.0  # mm/second

# The maximum speed (in mm/second) the machine can move in each axis
_DEFAULT_MAXSPEED = 1  # mm/second

_LED_MODES = [
    Xbox360Controller.LED_OFF,
    Xbox360Controller.LED_BLINK,
    Xbox360Controller.LED_ROTATE,
    Xbox360Controller.LED_ROTATE_TWO
]

_STICK_DEADZONE = .2


class DpadDirection(Enum):
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7

    @staticmethod
    def from_dpad(x, y):
        """
        Convert input from the dpad into a direction

        Arguments:
            x {int} -- 1 if right, -1 if left, and 0 otherwise
            y {int} -- 1 if up, -1 if down, and 0 otherwise

        Returns:
            DpadDirection -- the direction derived from x and y
        """
        if x == 0:
            if y == 0:
                return None
            elif y == 1:
                return DpadDirection.N
            return DpadDirection.S
        elif x == 1:
            if y == 0:
                return DpadDirection.E
            elif y == 1:
                return DpadDirection.NE
            return DpadDirection.SE
        if y == 0:
            return DpadDirection.W
        elif y == 1:
            return DpadDirection.NW
        return DpadDirection.SW


class XboxToGcode(Thread):
    """
    Convert xbox 360 controller input to GCode.

    | input         | action       | gcode |
    |-------------- |--------------|-------|
    | select        | quit         | N/A   |
    | left stick    | X/Y axis     | G0    |
    | right stick   | Z axis       | G0    |
    | right trigger | extrude      | G0    |
    | left trigger  | un-extrude   | G0    |
    | home button   | go home      | G28   |
    | dpad          | select color | T     |
    | Y button      | blink LED    | N/A   |
    """

    def __init__(self, callback, *range_e, kill_callback=None, rate=30.0,
                 range_x=(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED),
                 range_y=(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED),
                 range_z=(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED)):
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
            range_e {[(float, float)]} -- a list containing the range for each extruder as a tuple of
                (min speed, max speed) in mm/second
        """
        # configuration
        self._send_gcode = callback
        self._send_kill_command = kill_callback
        self._period = 1 / rate
        self._range_x = range_x
        self._range_y = range_y
        self._range_z = range_z
        if range_e:
            self._range_e = range_e
        else:
            self._range_e = [(_DEFAULT_MINSPEED, _DEFAULT_MAXSPEED)]

        # state
        self._extruder_id = 0
        self._next_extruder_id = 0
        self._led_mode = 0
        self._go_home = False  # to capture G28 commands
        self._should_stop = False

        self._controller = Xbox360Controller()
        super().__init__()

    def run(self):
        self._controller.button_select.when_pressed = self._kill
        self._controller.button_mode.when_released = self._set_go_home
        self._controller.button_y.when_released = self._use_next_led_mode
        self._controller.hat.when_moved = self._select_color_from_stick

        # configure the machine to use relative positioning
        self._send_gcode('G91')

        while not self._should_stop:
            start_time = time.time()

            command = self._get_gcode()
            if command:
                # print('sent command: \"{}\"'.format(command))
                success = self._send_gcode(command)
                if not success:
                    break

            # wait so that the machine is not updated faster than the requested rate
            execution_time = time.time() - start_time
            time_to_wait = self._period - execution_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)

        self._controller.close()

    def _num_extruders(self):
        return len(self._range_e)

    def _extruder_range(self):
        return self._range_e[self._extruder_id]

    def _select_color_from_stick(self, _):
        direction = DpadDirection.from_dpad(self._controller.hat.x, self._controller.hat.y)
        if not direction:
            return
        index = direction.value
        if index >= self._num_extruders():
            return

        self._next_extruder_id = index

    def _use_next_led_mode(self, _):
        self._led_mode = (self._led_mode + 1) % len(_LED_MODES)
        self._controller.set_led(_LED_MODES[self._led_mode])

    def _set_go_home(self, _):
        self._go_home = True

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

        # check extruder change
        if self._next_extruder_id != self._extruder_id:
            self._extruder_id = self._next_extruder_id
            return 'T{}'.format(self._extruder_id)

        # calculate commanded velocity on each axis
        vel_x = 0
        vel_y = 0
        vel_z = 0
        vel_e = 0

        axis_lx = self._controller.axis_l.x
        if abs(axis_lx) > _STICK_DEADZONE:
            vel_x = axis_lx * self._range_x[1]

        axis_ly = self._controller.axis_l.y
        if abs(axis_ly) > _STICK_DEADZONE:
            vel_y = axis_ly * self._range_y[1]

        axis_ry = self._controller.axis_r.y
        if abs(axis_ry) > _STICK_DEADZONE:
            vel_z = axis_ry * self._range_z[1]

        range_e = self._extruder_range()
        if self._controller.trigger_l.value:
            vel_e = -self._controller.trigger_l.value * range_e[1]
        else:
            vel_e = self._controller.trigger_r.value * range_e[1]

        # if any axis is moving fast enough, send a rapid move command
        if abs(vel_x) > self._range_x[0] or abs(vel_y) > self._range_y[0] or abs(vel_z) > self._range_z[0] \
                or abs(vel_e) > range_e[0]:
            dx = vel_x * self._period
            dy = vel_y * self._period
            dz = vel_z * self._period
            de = vel_e * self._period

            speed = math.sqrt(vel_x * vel_x + vel_y * vel_y + vel_z * vel_z + vel_e * vel_e)
            speed *= 60.0  # convert to mm/minute

            return 'G1 X{} Y{} Z{} E{} F{}'.format(dx, dy, dz, de, speed)

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
