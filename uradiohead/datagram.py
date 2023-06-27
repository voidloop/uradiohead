class Datagram:
    def __init__(self, driver, address):
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

    def send_to(self, buf, to_addr):
        self.header_to = to_addr
        return self._driver.send(buf)

    def recv_from(self):
        return self._driver.recv(), self.header_from, self.header_to, self.header_ident

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
    def header_ident(self):
        return self._driver.header_ident

    @header_ident.setter
    def header_ident(self, ident):
        self._driver.header_ident = ident

    def available(self):
        self._driver.available()

    def wait_available(self, timeout=None, poll_delay=None):
        self._driver.wait_available(timeout, poll_delay)

    def wait_packet_sent(self, timeout=None):
        self._driver.wait_packet_sent(timeout)
