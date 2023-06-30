import array
import random
import time

from ..constants import (
    RH_DEFAULT_TIMEOUT, RH_DEFAULT_RETRIES, RH_FLAGS_NONE,
    RH_FLAGS_ACK, RH_FLAGS_RETRY, RH_BROADCAST_ADDRESS)
from .datagram import Datagram


class ReliableDatagram(Datagram):
    def __init__(self, driver, addr):
        super().__init__(driver, addr)
        self._retransmissions = 0
        self._last_sequence_number = 0
        self._seen_ids = array.array('H', (0 for _ in range(256)))  # noqa
        self._timeout = RH_DEFAULT_TIMEOUT
        self._retries = RH_DEFAULT_RETRIES

    def sendto_wait(self, buf, addr):
        sequence_number = self._last_sequence_number + 1
        retries = 0

        while retries <= self._retries:
            retries = retries + 1
            self.header_id = sequence_number
            flags_to_set = RH_FLAGS_NONE
            flags_to_clear = RH_FLAGS_ACK
            if retries == 1:
                flags_to_clear |= RH_FLAGS_RETRY
            else:
                flags_to_set = RH_FLAGS_RETRY
            self.set_header_flags(flags_to_set, flags_to_clear)

            n_bytes = self.sendto(buf, addr)
            self.wait_packet_sent()

            if addr == RH_BROADCAST_ADDRESS:
                return n_bytes

            if retries > 1:
                self._retransmissions += 1

            send_time = time.time()
            timeout = int(random.uniform(self._timeout, self._timeout * 2))

            while True:
                timeleft = timeout - (time.time() - send_time)
                if timeleft <= 0:
                    break
                if self.wait_available_timeout(timeleft):
                    data = self.recvfrom()
                    if data is None:
                        continue
                    _, from_addr, to_addr, header_id, flags = data
                    if from_addr == addr and to_addr == self.address and \
                            flags & RH_FLAGS_ACK and header_id == sequence_number:
                        return n_bytes
                    elif not (flags & RH_FLAGS_ACK) and header_id == self._seen_ids[from_addr]:
                        self._acknowledge(header_id, from_addr)

        return None

    def _acknowledge(self, hdr_id, addr):
        self.header_id = hdr_id
        self.set_header_flags(RH_FLAGS_ACK)
        self.sendto(b'!', addr)
        self.wait_packet_sent()

    def recvfrom_ack(self):
        if self.available():
            data = self.recvfrom()
            if data is None:
                return None

            buf, from_addr, to_addr, header_id, flags = data
            if not (flags & RH_FLAGS_ACK):
                if to_addr == self.address:
                    self._acknowledge(header_id, from_addr)
                if not (flags & RH_FLAGS_RETRY) or header_id != self._seen_ids[from_addr]:
                    self._seen_ids[from_addr] = header_id
                    return buf, from_addr, to_addr, header_id, flags
        return None

    def recvfrom_ack_timeout(self, timeout):
        start_time = time.time()
        while True:
            timeleft = timeout - (time.time() - start_time)
            if timeleft <= 0:
                break
            if self.wait_available_timeout(timeleft):
                data = self.recvfrom_ack()
                if data:
                    return data
        return None

    @property
    def retransmissions(self):
        return self._retransmissions

    def reset_retransmissions(self):
        self._retransmissions = 0
