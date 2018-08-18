import unittest

from unittest.mock import patch, Mock
from xbox_bindings import _FOREVER, _convert_stick_axis_to_stepper_motor, \
                          stick_axis_to_stepper_motor_binding


class TestXboxBindings(unittest.TestCase):
    def test_convert(self):
        converted = _convert_stick_axis_to_stepper_motor(-.6, 10)
        self.assertEqual(converted['frequency'], 6)
        self.assertEqual(converted['goal'], -_FOREVER)

    @patch('xbox_bindings._convert_stick_axis_to_stepper_motor')
    def test_update(self, mock_convert):
        mock_convert.return_value = {
            'frequency': 100,
            'goal': 2000
        }
        stick_axis = Mock(return_value=.5)
        motor = Mock()
        binding = stick_axis_to_stepper_motor_binding(stick_axis, motor)
        binding()
        motor.set_stepper.assert_called_once_with(frequency=100, goal=2000)


if __name__ == '__main__':
    unittest.main()
