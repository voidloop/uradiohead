import unittest
from unittest.mock import MagicMock

from uradiohead.drivers import UartDriver
from uradiohead.drivers.uart import _RX_STATE_IDLE  # noqa


class TestUartDriver(unittest.TestCase):
    def test_uart_driver(self):
        uart = MagicMock()
        driver = UartDriver(uart)
        self.assertEqual(driver.init(), True)
        self.assertEqual(driver._rx_state, _RX_STATE_IDLE)

        driver.send(b"test")
        data = b''.join(call.args[0] for call in uart.mock_calls if call[0] == "write")

        uart.any.return_value = True
        driver.recv()

        pass
