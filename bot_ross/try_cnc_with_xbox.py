import cnc.main
import cnc.logging_config
import cnc.config as config

from xbox_to_gcode import XboxToGcode


if __name__ == '__main__':
    min_speed = config.MIN_VELOCITY_MM_PER_MIN / 60.0

    extruder_ranges = [(min_speed, e['max_speed'] / 60.0) for e in config.EXTRUDER_CONFIG]

    # cnc.logging_config.debug_enable()
    gcode_generator = XboxToGcode(
        cnc.main.do_line,
        kill_callback=cnc.hal.disable_steppers,
        rate=30.0,
        range_x=(min_speed, config.MAX_VELOCITY_MM_PER_MIN_X / 60.0),
        range_y=(min_speed, config.MAX_VELOCITY_MM_PER_MIN_X / 60.0),
        range_z=(min_speed, config.MAX_VELOCITY_MM_PER_MIN_X / 60.0),
        range_e=extruder_ranges
    )
    try:
        gcode_generator.start()
        gcode_generator.join()
    finally:
        cnc.main.machine.release()
