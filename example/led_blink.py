import utime
from machine import I2C, Pin

from MicroPython_PCF8574T import GpioExpander

LED_PIN: int = 0


def main() -> None:
    i2c: I2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)  # I2C object
    io_exp = GpioExpander(i2c)  # PCF8574T object

    io_exp.pin_mode(LED_PIN, io_exp.OUTPUT)  # Pin: 0 configured as output

    while True:
        io_exp.digital_write(LED_PIN, True)  # LED ON
        utime.sleep_ms(500)
        io_exp.digital_write(LED_PIN, False)  # LED OFF
        utime.sleep_ms(500)


if __name__ == "__main__":
    main()
