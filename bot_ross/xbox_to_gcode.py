import math
import time

from threading import Thread
from xbox360controller import Xbox360Controller


# The minimum speed (in mm/second) for the machine to accept a move command
_DEFAULT_MINSPEED = 1 / 60.0  # mm/second

# The maximum speed (in mm/second) the machine can move in each axis
_DEFAULT_MAXSPEED = 1  # mm/second


class XboxToGcode(Thread):
    def __init__(self, callback, kill_callback=None, rate=30.0,
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
        """
        self._send_gcode = callback
        self._send_kill_command = kill_callback
        self._period = 1 / rate
        self._range_x = range_x
        self._range_y = range_y
        self._range_z = range_z
        self._should_stop = False
        self._controller = Xbox360Controller()
        super().__init__()

    def run(self):
        self._controller.button_select.when_pressed = self._kill

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

    def _kill(self, _):
        if self._send_kill_command:
            self._send_kill_command()
        self._should_stop = True

    def _get_gcode(self):
        """
        Get a line of gcode for the current state of the xbox controller, or None if it is inactive.
        """
        vel_x = self._controller.axis_l.x * self._range_x[1]
        vel_y = self._controller.axis_l.y * self._range_y[1]

        if vel_x > self._range_x[0] or vel_y > self._range_y[0]:
            # do a rapid move
            dx = vel_x * self._period
            dy = vel_y * self._period
            speed = math.sqrt(vel_x * vel_x + vel_y * vel_y) * 60.0  # convert to mm/minute
            return 'G0 X{} Y{} F{}'.format(dx, dy, speed)

        return None
