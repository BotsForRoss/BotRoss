import sys
import unittest

from unittest.mock import Mock, patch, call

mock_gpio = Mock()
mock_rpi = Mock()
mock_rpi.GPIO = mock_gpio
sys.modules['RPi'] = mock_rpi
sys.modules['RPi.GPIO'] = mock_gpio
from pot import Pot

class TestPot(unittest.TestCase):
    @patch("time.sleep")
    def test_discharge(self, mock_sleep):
        pot = Pot(5, 6)
        mock_gpio.IN = 'in'
        mock_gpio.OUT = 'out'
        
        pot.discharge()

        mock_gpio.setup.assert_has_calls([
            call(5, 'in'),
            call(6, 'out')
        ])
        mock_gpio.output.assert_called_once_with(6, False)
        mock_sleep.assert_called_once_with(0.005)


if __name__ == '__main__':
    unittest.main()
