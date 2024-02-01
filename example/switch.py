from machine import I2C, Pin

from MicroPython_PCF8574T import GpioExpander

LED_PIN: int = 0  # LED pin
SWITCH: int = 1  # push button pin


def main() -> None:
    i2c: I2C = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)  # I2C object
    io_exp = GpioExpander(i2c)  # PCF8574T object

    io_exp.pin_mode(LED_PIN, io_exp.OUTPUT)  # Pin: 0 configured as output "LED_PIN pin"
    io_exp.pin_mode(SWITCH, io_exp.INPUT)  # Pin:1 configured as input "SWITCH pin"

    while True:
        status: int = io_exp.digital_read(SWITCH)  # The variable track the GPIO state
        if status:
            io_exp.digital_write(LED_PIN, True)
        else:
            io_exp.digital_write(LED_PIN, False)


if __name__ == "__main__":
    main()