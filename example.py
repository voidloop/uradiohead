from uradiohead.drivers import UartDriver

def main():
    driver = GenericDriver()
    manager = Datagram(driver, 0x01)

    if driver.init():
        print("Driver initialized")
    else:
        raise RuntimeError("Driver initialization failed")


if __name__ == '__main__':
    main()
