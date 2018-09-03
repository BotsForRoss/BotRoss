import cnc.main
import cnc.logging_config
import cnc.config as config

from xbox_to_gcode import XboxToGcode


if __name__ == '__main__':
    cnc.logging_config.debug_enable()
    gcode_generator = XboxToGcode(
        cnc.main.do_line,
        rate=1.0,
        range_x=(config.MIN_VELOCITY_MM_PER_MIN / 60.0, config.MAX_VELOCITY_MM_PER_MIN_X / 60.0),
        range_y=(config.MIN_VELOCITY_MM_PER_MIN / 60.0, config.MAX_VELOCITY_MM_PER_MIN_Y / 60.0),
        range_z=(config.MIN_VELOCITY_MM_PER_MIN / 60.0, config.MAX_VELOCITY_MM_PER_MIN_Z / 60.0),
        range_e=(config.MIN_VELOCITY_MM_PER_MIN / 60.0, config.MAX_VELOCITY_MM_PER_MIN_E / 60.0),
        num_extruders=config.NUM_EXTRUDERS
    )
    gcode_generator.start()
    gcode_generator.join()
    cnc.main.machine.release()
