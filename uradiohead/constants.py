from .utils import const

RH_BROADCAST_ADDRESS = const(0xFF)
RH_MODE_INITIALISING = const(0)

RH_MODE_TX = const(1)
RH_MODE_RX = const(2)

RH_DEFAULT_TIMEOUT = const(200)
RH_DEFAULT_RETRIES = const(3)

RH_FLAGS_NONE = const(0x00)
RH_FLAGS_RETRY = const(0x40)
RH_FLAGS_ACK = const(0x80)

