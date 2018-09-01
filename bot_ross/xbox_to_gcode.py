import cnc
import math
import time

from threading import Thread
from xbox360controller import Xbox360Controller


class XboxToGcode(Thread):
    # The minimum speed (in mm/second) for the machine to accept a move command
    _DEADZONE = 1

    # The maximum speed (in mm/second) the machine can move in each axis
    _MAXSPEED = 10

    def __init__(self, callback, kill_callback=None, rate=30.0):
        """
        Pipe xbox controller input into gcode output

        Arguments:
            callback {function} -- a function that takes a line of gcode every time the controller updates

        Keyword Arguments:
            rate {float} -- the maximum update rate of the controller, in Hz (default: {60.0})
            kill_callback {function} -- a function that will be called immediately when the stop button is pressed
        """
        self._send_gcode = callback
        self._send_kill_command = kill_callback
        self._period = 1 / rate
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
                self._send_gcode(command)

            # wait so that the machine is not updated faster than the requested rate
            execution_time = time.time() - start_time
            time_to_wait = self._period - execution_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)

        self._controller.close()

    def _kill(self):
        if self._send_kill_command:
            self._send_kill_command()
        self._should_stop = True

    def _get_gcode(self):
        """
        Get a line of gcode for the current state of the xbox controller, or None if it is inactive.
        """
        dx = self._stick_to_distance(self._controller.axis_l.x)
        dy = self._stick_to_distance(self._controller.axis_l.y)

        distance = math.sqrt(dx * dx + dy * dy)
        speed = distance / self._xbox.refreshDelay

        # do a rapid move
        if speed >= self._DEADZONE:
            speed /= 60.0  # convert to mm/minute
            return 'G0 X{} Y{} F{}'.format(dx, dy, speed)

        return None

    def _stick_to_distance(self, stick):
        """
        Arguments:
            stick {float} -- the value of an analog stick axis from -1 to 1

        Returns:
            float -- the distance in mm the axis should move in one update based on the stick input
        """
        return stick * self._MAXSPEED * self._xbox.refreshDelay


if __name__ == '__main__':
    def _do_line_carefully(line):
        success = cnc.main.do_line(line)
        if not success:
            raise RuntimeError('An error occurred in gmachine')

    try:
        gcode_generator = XboxToGcode(_do_line_carefully)
        gcode_generator.join()
    finally:
        cnc.machine.release()
