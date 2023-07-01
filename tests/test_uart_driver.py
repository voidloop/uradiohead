import unittest

from uradiohead.drivers import UartDriver
from uradiohead.drivers.uart import _RX_STATE_IDLE  # noqa
from uradiohead.managers import ReliableDatagram


class DummyUart:
    def __init__(self):
        self.data = bytearray()

    def write(self, data):
        self.data.extend(data)

    def read(self, n_bytes=None):
        if n_bytes is None:
            n_bytes = len(self.data)
        ret = self.data[:n_bytes]
        self.data = self.data[n_bytes:]
        return ret

    def any(self):
        return len(self.data)


class TestUartDriver(unittest.TestCase):
    def setUp(self):
        self.uart = DummyUart()

    def test_uart_driver(self):
        driver = UartDriver(self.uart)
        self.assertEqual(driver.init(), True)
        self.assertEqual(driver._rx_state, _RX_STATE_IDLE)

        data_to_send = b'te\x10st'
        driver.send(data_to_send)
        self.assertEqual(driver.recv(), data_to_send)

    def test_reliable_datagram(self):
        driver = UartDriver(self.uart)
        manager = ReliableDatagram(driver, 1)

        self.assertEqual(manager.init(), True)
        self.assertEqual(manager.address, 1)
        self.assertEqual(driver.address, 1)

        data_to_send = b'te\x10st'
        manager.sendto(data_to_send, 1)
        self.assertEqual(manager.recvfrom_ack(), (data_to_send, 1, 1, 0, 0))

        manager.sendto_wait(data_to_send, 1)

