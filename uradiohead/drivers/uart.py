import struct

from ..constants import RH_BROADCAST_ADDRESS
from ..drivers.generic import GenericDriver
from ..utils import crc_ccitt_update, const

_STX = const(0x02)
_ETX = const(0x03)
_DLE = const(0x10)
_SYN = const(0x16)

_RX_UART_HEADER_LEN = const(4)
_RH_UART_DEFAULT_PAYLOAD_LEN = const(64)

_RX_STATE_INIT = const(0)
_RX_STATE_IDLE = const(1)
_RX_STATE_DLE = const(2)
_RX_STATE_DATA = const(3)
_RX_STATE_ESCAPE = const(4)
_RX_STATE_WAIT_FCS_1 = const(5)
_RX_STATE_WAIT_FCS_2 = const(6)


class UartDriver(GenericDriver):
    def __init__(self, uart, payload_len=_RH_UART_DEFAULT_PAYLOAD_LEN):
        super().__init__()
        self._uart = uart
        self._rx_buf = bytearray(payload_len)
        self._rx_buf_len = 0
        self._rx_buf_valid = False
        self._rx_state = _RX_STATE_INIT
        self._rx_fcs = 0xFFFF
        self._tx_fcs = 0xFFFF
        self._rx_recd_fcs = 0xFFFF
        self.promiscuous = False

    def init(self):
        if not super().init():
            return False
        self._rx_state = _RX_STATE_IDLE
        return True

    def available(self):
        while not self._rx_buf_valid and self._uart.any():
            ch = self._uart.read(1)[0]
            self._handle_rx(ch)
        return self._rx_buf_valid

    def _handle_rx(self, ch):
        if self._rx_state == _RX_STATE_IDLE:
            if ch == _DLE:
                self._rx_state = _RX_STATE_DLE

        elif self._rx_state == _RX_STATE_DLE:
            if ch == _STX:
                self._rx_state = _RX_STATE_DATA
                self._clear_rx_buf()
            else:
                self._rx_state = _RX_STATE_IDLE

        elif self._rx_state == _RX_STATE_DATA:
            if ch == _DLE:
                self._rx_state = _RX_STATE_ESCAPE
            else:
                self._append_rx_buf(ch)

        elif self._rx_state == _RX_STATE_ESCAPE:
            if ch == _ETX:
                self._rx_fcs = crc_ccitt_update(self._rx_fcs, _DLE)
                self._rx_fcs = crc_ccitt_update(self._rx_fcs, _ETX)
                self._rx_state = _RX_STATE_WAIT_FCS_1
            elif ch == _DLE:
                self._append_rx_buf(ch)
                self._rx_state = _RX_STATE_DATA
            else:
                self._rx_state = _RX_STATE_IDLE

        elif self._rx_state == _RX_STATE_WAIT_FCS_1:
            self._rx_recd_fcs = ch << 8
            self._rx_state = _RX_STATE_WAIT_FCS_2

        elif self._rx_state == _RX_STATE_WAIT_FCS_2:
            self._rx_recd_fcs |= ch
            self._rx_state = _RX_STATE_IDLE
            self._validate_rx_buf()

    def _clear_rx_buf(self):
        self._rx_buf_len = 0
        self._rx_buf_valid = False
        self._rx_fcs = 0xFFFF

    def _append_rx_buf(self, ch):
        if self._rx_buf_len < len(self._rx_buf):
            self._rx_buf[self._rx_buf_len] = ch
            self._rx_fcs = crc_ccitt_update(self._rx_fcs, ch)
            self._rx_buf_len += 1

    def _validate_rx_buf(self):
        if self._rx_recd_fcs != self._rx_fcs:
            self._rx_bad += 1
        else:
            self._rx_header_to = self._rx_buf[0]
            self._rx_header_from = self._rx_buf[1]
            self._rx_header_id = self._rx_buf[2]
            self._rx_header_flags = self._rx_buf[3]
            if self.promiscuous or self._rx_header_to == self.address or \
                    self._rx_header_to == RH_BROADCAST_ADDRESS:
                self._rx_good += 1
                self._rx_buf_valid = True

    def recv(self):
        if not self.available():
            return None
        data = bytes(self._rx_buf[_RX_UART_HEADER_LEN:self._rx_buf_len])
        self._clear_rx_buf()
        return data

    def send(self, buf):
        if len(buf) > self.max_message_length:
            return False

        # if not self.wait_cad():
        #     return None

        self._tx_fcs = 0xFFFF
        self._uart.write(struct.pack('!BB', _DLE, _STX))
        self._tx_data(self._tx_header_from)
        self._tx_data(self._tx_header_to)
        self._tx_data(self._tx_header_id)
        self._tx_data(self._tx_header_flags)
        for ch in buf:
            self._tx_data(ch)
        self._uart.write(struct.pack('!BB', _DLE, _ETX))
        self._tx_fcs = crc_ccitt_update(self._tx_fcs, _DLE)
        self._tx_fcs = crc_ccitt_update(self._tx_fcs, _ETX)
        self._uart.write(struct.pack('!H', self._tx_fcs))
        return True

    def _tx_data(self, ch):
        if ch == _DLE:
            self._uart.write(struct.pack('!B', _DLE))
        self._uart.write(struct.pack('!B', ch))
        self._tx_fcs = crc_ccitt_update(self._tx_fcs, ch)

    @property
    def max_message_length(self):
        return len(self._rx_buf) - _RX_UART_HEADER_LEN
