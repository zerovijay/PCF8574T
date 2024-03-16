import utime
from machine import I2C, Pin

from ..src.PCF8574T import PCF8574T

LED_PIN: int = 0  # Set GPIO P0 as a LED pin


def main() -> None:
    i2c: I2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)  # I2C object.
    gpio_exp = PCF8574T(i2c)  # PCF8574T object.
    gpio_exp.set_gpio_mode(LED_PIN, gpio_exp.OUTPUT)  # Pin: 0 configured as output.

    while True:
        gpio_exp.gpio_write(LED_PIN, True)  # LED ON.
        utime.sleep_ms(500)
        gpio_exp.gpio_write(LED_PIN, False)  # LED OFF.
        utime.sleep_ms(500)


if __name__ == "__main__":
    main()
