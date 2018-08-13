import sys
import threading
import unittest

from unittest.mock import Mock, call, patch

mock_gpio = Mock()
mock_rpi = Mock()
mock_rpi.GPIO = mock_gpio
sys.modules['RPi'] = mock_rpi
sys.modules['RPi.GPIO'] = mock_gpio
from stepper_motor import StepperMotor, StepperMotorDirection  # noqa: 402


class TestStepperMotor(unittest.TestCase):
    def setUp(self):
        mock_gpio.BOARD = 'boarderino'
        mock_gpio.OUT = 'out!'
        mock_gpio.HIGH = 'hi'
        mock_gpio.LOW = 'lo'

    def test_init(self):
        StepperMotor(1, 2, 3, 4)
        mock_gpio.setmode.assert_called_once_with('boarderino')
        mock_gpio.setup.assert_has_calls([
            call(1, 'out!'),
            call(2, 'out!'),
            call(3, 'out!'),
            call(4, 'out!')
        ])

    def test_step(self):
        motor = StepperMotor(1, 2, 3, 4)

        # 7
        motor.step(StepperMotorDirection.REVERSE)
        mock_gpio.output.assert_has_calls([
            call(1, 'hi'),
            call(2, 'lo'),
            call(3, 'lo'),
            call(4, 'hi')
        ])
        mock_gpio.output.reset_mock()

        # 0
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'hi'),
            call(2, 'lo'),
            call(3, 'lo'),
            call(4, 'lo')
        ])
        mock_gpio.output.reset_mock()

        # 1
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'hi'),
            call(2, 'hi'),
            call(3, 'lo'),
            call(4, 'lo')
        ])
        mock_gpio.output.reset_mock()

        # 2
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'lo'),
            call(2, 'hi'),
            call(3, 'lo'),
            call(4, 'lo')
        ])
        mock_gpio.output.reset_mock()

        # 3
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'lo'),
            call(2, 'hi'),
            call(3, 'hi'),
            call(4, 'lo')
        ])
        mock_gpio.output.reset_mock()

        # 4
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'lo'),
            call(2, 'lo'),
            call(3, 'hi'),
            call(4, 'lo')
        ])
        mock_gpio.output.reset_mock()

        # 5
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'lo'),
            call(2, 'lo'),
            call(3, 'hi'),
            call(4, 'hi')
        ])
        mock_gpio.output.reset_mock()

        # 6
        motor.step(StepperMotorDirection.FORWARD)
        mock_gpio.output.assert_has_calls([
            call(1, 'lo'),
            call(2, 'lo'),
            call(3, 'lo'),
            call(4, 'hi')
        ])
        mock_gpio.output.reset_mock()

    @patch.object(StepperMotor, 'step')
    @patch('time.time', autospec=True)
    @patch('threading.Timer', autospec=True)
    def test_step_and_reset_timer(self, mock_timer, mock_time, mock_step):
        mock_time.return_value = 3000
        mock_timer_instance = Mock(spec=threading.Timer)
        mock_timer.return_value = mock_timer_instance
        motor = StepperMotor(1, 2, 3, 4)

        motor._step_and_reset_timer(10)

        mock_step.assert_called_once_with(direction=StepperMotorDirection.FORWARD)
        self.assertEqual(motor._last_update_time, 3000)
        mock_timer.assert_called_once()
        mock_timer_instance.start.assert_called_once()

    @patch.object(StepperMotor, '_step_and_reset_timer')
    @patch('time.time', autospec=True)
    def test_set_frequency_faster(self, mock_time, mock_reset_timer):
        # This tests the case where the time since last update is greater than the new period
        mock_time.return_value = 2
        motor = StepperMotor(1, 2, 3, 4)
        motor._timer = Mock(spec=threading.Timer)
        motor._last_update_time = 1

        motor.set_frequency(20)

        motor._timer.cancel.assert_called_once()
        mock_reset_timer.assert_called_once_with(.05, StepperMotorDirection.FORWARD)

    @patch('threading.Timer', autospec=True)
    @patch('time.time', autospec=True)
    def test_set_frequency_slower(self, mock_time, mock_timer):
        # This tests the case where the time since last update is less than the new period
        mock_time.return_value = 2
        motor = StepperMotor(1, 2, 3, 4)
        mock_timer_instance = Mock(spec=threading.Timer)
        mock_timer.return_value = mock_timer_instance
        motor._last_update_time = 1.99

        motor.set_frequency(20)

        mock_timer.assert_called_once()
        mock_timer_instance.start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
