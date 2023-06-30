from uradiohead.datagram import Datagram
from uradiohead.drivers.generic import GenericDriver


def main():
    driver = GenericDriver()
    manager = Datagram(driver, 0x01)

    if driver.init():
        print("Driver initialized")
    else:
        raise RuntimeError("Driver initialization failed")


if __name__ == '__main__':
    main()
