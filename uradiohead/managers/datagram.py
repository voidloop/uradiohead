from ..constants import RH_FLAGS_NONE
from ..drivers.generic import GenericDriver


class Datagram:
    def __init__(self, driver: GenericDriver, address):
        self._address = address
        self._driver = driver

    def init(self):
        ret = self._driver.init()
        if ret:
            self.address = self._address
        return ret

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._driver.address = address
        self.header_from = address
        self._address = address

    def sendto(self, buf, to_addr):
        self.header_to = to_addr
        return self._driver.send(buf)

    def recvfrom(self):
        return self._driver.recv(), self.header_from, self.header_to, self.header_id, self.flags

    @property
    def header_from(self):
        return self._driver.header_from

    @header_from.setter
    def header_from(self, from_addr):
        self._driver.header_from = from_addr

    @property
    def header_to(self):
        return self._driver.header_to

    @header_to.setter
    def header_to(self, to_addr):
        self._driver.header_to = to_addr

    @property
    def header_id(self):
        return self._driver.header_id

    @header_id.setter
    def header_id(self, id):  # noqa
        self._driver.header_id = id

    @property
    def flags(self):
        return self._driver.flags

    def set_header_flags(self, flags_to_set, flags_to_clear=RH_FLAGS_NONE):
        self._driver.set_header_flags(flags_to_set, flags_to_clear)

    def available(self):
        self._driver.available()

    def wait_available(self, poll_delay=None):
        self._driver.wait_available(poll_delay)

    def wait_available_timeout(self, timeout, poll_delay=None):
        self._driver.wait_available_timeout(timeout, poll_delay)

    def wait_packet_sent(self, timeout=None):
        self._driver.wait_packet_sent(timeout)
