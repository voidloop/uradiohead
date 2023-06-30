import struct

try:
    from micropython import const
except ImportError:
    def const(x):
        return x


def crc_ccitt_update(crc, data):
    data ^= crc & 0xFF
    data ^= data << 4
    return ((data << 8) | (crc >> 8) ^ (data >> 4) ^ (data << 3)) & 0xFFFF
