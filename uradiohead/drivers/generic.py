import time

from ..constants import RH_BROADCAST_ADDRESS, RH_MODE_INITIALISING, RH_MODE_TX


class GenericDriver:
    def __init__(self):
        self.address = RH_BROADCAST_ADDRESS
        self._tx_header_to = RH_BROADCAST_ADDRESS
        self._tx_header_from = RH_BROADCAST_ADDRESS
        self._tx_header_id = 0
        self._tx_header_flags = 0
        self._rx_bad = 0
        self._rx_good = 0
        self._tx_good = 0
        self._cad_timeout = 0
        self.mode = RH_MODE_INITIALISING

    def wait_available(self, poll_delay=None):
        while not self.available():
            if poll_delay:
                time.sleep(poll_delay)

    def wait_available_timeout(self, timeout, poll_delay=None):
        start = time.time()
        while (time.time() - start) < timeout:
            if self.available():
                return True
            if poll_delay:
                time.sleep(poll_delay)
        return False

    def wait_packet_sent(self):
        while self.mode == RH_MODE_TX:
            pass

    def wait_packet_sent_timeout(self, timeout):
        start = time.time()
        while (time.time() - start) < timeout:
            if self.mode != RH_MODE_TX:
                return True
        return False

    def set_header_flags(self, flags_to_set, flags_to_clear):
        self._tx_header_flags &= ~flags_to_clear
        self._tx_header_flags |= flags_to_set

    @property
    def header_id(self):
        return self._tx_header_id

    @header_id.setter
    def header_id(self, id):  # noqa
        self._tx_header_id = id

    @property
    def header_to(self):
        return self._tx_header_to

    @header_to.setter
    def header_to(self, addr):
        self._tx_header_to = addr

    @property
    def header_from(self):
        return self._tx_header_from

    @header_from.setter
    def header_from(self, addr):
        self._tx_header_from = addr

    @property
    def flags(self):
        return self._tx_header_flags

    @staticmethod
    def init():
        return True

    def available(self):
        raise NotImplemented

    def send(self, buf) -> bool:
        raise NotImplemented

    def recv(self):
        raise NotImplemented
