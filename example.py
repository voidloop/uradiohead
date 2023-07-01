from machine import UART

from uradiohead.drivers import UartDriver

uart = UART(0, 9600)
driver = UartDriver(uart)


def main():
    if driver.init():
        print("Driver initialized")
    else:
        raise RuntimeError("Driver initialization failed")


if __name__ == '__main__':
    main()
