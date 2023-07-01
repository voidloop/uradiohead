import unittest

from uradiohead.utils import crc_ccitt_update, crc_xmodem_update


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.data = b'test'

    def test_crc_ccitt_update(self):
        crc = 0xFFFF
        for ch in self.data:
            crc = crc_ccitt_update(crc, ch)
        self.assertEqual(crc, 0xF877)

    def test_crc_xmodem_update(self):
        crc = 0xFFFF
        for ch in self.data:
            crc = crc_xmodem_update(crc, ch)
        self.assertEqual(crc, 0x1FC6)
