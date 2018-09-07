import cnc.main
import cnc.logging_config
import cnc.config as config

from xbox_to_gcode import XboxToGcode


if __name__ == '__main__':
    # max_speed = config.MAX_VELOCITY_MM_PER_MIN_X / 60.0
    min_speed = 10
    max_speed = 100

    # cnc.logging_config.debug_enable()
    gcode_generator = XboxToGcode(
        cnc.main.do_line,
        kill_callback=cnc.hal.disable_steppers,
        rate=10.0,
        range_x=(min_speed, max_speed),
        range_y=(min_speed, max_speed),
        range_z=(min_speed, max_speed),
        range_e=(min_speed, max_speed),
        num_extruders=len(config.EXTRUDER_CONFIG)
    )
    gcode_generator.start()
    gcode_generator.join()
    cnc.main.machine.release()
