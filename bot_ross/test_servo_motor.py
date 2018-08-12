import sys
import unittest

from unittest.mock import Mock, patch, call

sys.modules['smbus2'] = Mock()  # mock before import for windows compatibility
from servo_motor import ServoMotor  # noqa: E402


class TestServoMotor(unittest.TestCase):
    def setUp(self):
        self.mock_bus = Mock()

    @patch.object(ServoMotor, '_configure')
    def test_init(self, mock_configure):
        motor = ServoMotor(self.mock_bus, 'addr!')
        self.assertEqual(motor.addr, 'addr!')
        mock_configure.assert_called_once()

    def test_configure(self):
        ServoMotor(self.mock_bus, 'addr!')
        self.mock_bus.write_byte_data.assert_has_calls([
            call('addr!', 0, 0b00100000),
            call('addr!', 0xfe, 0x1e)
        ])

    def test_set_led_output(self):
        motor = ServoMotor(self.mock_bus, 'addr!')
        motor.set_led_output(12, 50, 1200)
        self.mock_bus.write_word_data.assert_has_calls([
            call('addr!', 0x36, 50),
            call('addr!', 0x38, 1200)
        ])

    def test_set_led_output_range_errors(self):
        motor = ServoMotor(self.mock_bus, 'addr!')
        with self.assertRaises(ValueError):
            motor.set_led_output(3, -5, 400)
        with self.assertRaises(ValueError):
            motor.set_led_output(3, 4000, 1000)
        with self.assertRaises(ValueError):
            motor.set_led_output(3, 0, 4096)
        with self.assertRaises(ValueError):
            motor.set_led_output(16, 0, 400)

    @patch.object(ServoMotor, 'set_led_output')
    def test_set_duty_cycle(self, mock_set_led_output):
        motor = ServoMotor(self.mock_bus, 'addr!')
        motor.set_duty_cycle(4, 123)
        mock_set_led_output.assert_called_once_with(4, 0, 123)

    @patch.object(ServoMotor, 'set_duty_cycle')
    def test_set_angle(self, mock_set_duty_cycle):
        motor = ServoMotor(self.mock_bus, 'addr!')
        motor.set_angle(5, -45.4)
        mock_set_duty_cycle.assert_called_once_with(5, 1459)


if __name__ == '__main__':
    unittest.main()
