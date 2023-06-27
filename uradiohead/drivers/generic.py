import time

from constants import RH_BROADCAST_ADDRESS


class GenericDriver:
    def __init__(self):
        self._address = RH_BROADCAST_ADDRESS
        self._header_to = RH_BROADCAST_ADDRESS
        self._header_from = RH_BROADCAST_ADDRESS
        self._header_ident = 0
        self._header_flags = 0
        self._rx_bad = 0
        self._rx_good = 0
        self._tx_good = 0
        self._cad_timeout = 0
        self._mode = RH_MODE_INITIALISING

    @staticmethod
    def init():
        return True

    def wait_available(self, timeout=None, poll_delay=None):
        if timeout is None:
            while not self.available():
                if poll_delay:
                    time.sleep(poll_delay)
        else:
            start = time.time()
            while (time.time() - start) < timeout:
                if self.available():
                    return True
                if poll_delay:
                    time.sleep(poll_delay)

    def wait_packet_sent(self, timeout=None):
        if timeout is None:
            while self._mode == RH_MODE_TX:
                pass
        else:
            start = time.time()
            while (time.time() - start) < timeout:
                if self._mode != RH_MODE_TX:
                    return True
