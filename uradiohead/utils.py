try:
    from micropython import const
except ImportError:
    def const(x):
        return x

try:
    from time import ticks_ms, ticks_diff
except ImportError:
    import time


    def ticks_ms():
        return int(time.time() * 1000)


    def ticks_diff(t1, t2):
        return t1 - t2


def crc_ccitt_update(crc, data):
    data ^= crc & 0xFF
    data ^= (data << 4) & 0xFF
    return (((data << 8) | (crc >> 8)) ^ (data >> 4) ^ (data << 3)) & 0xFFFF


def crc_xmodem_update(crc, data):
    crc ^= (data << 8)
    for _ in range(8):
        if crc & 0x8000:
            crc = (crc << 1) ^ 0x1021
        else:
            crc <<= 1
        crc &= 0xFFFF
    return crc
