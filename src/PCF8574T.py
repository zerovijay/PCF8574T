from machine import I2C
from micropython import const


class PCF8574T:
    # Constants representing pin modes and default address
    DEFAULT_ADDR: int = const(0x20)
    INPUT_LOW: int = const(0x1)  # Pin set to input, default state low
    INPUT_HIGH: int = const(0x1)  # Pin set to input, default state high
    OUTPUT_LOW: int = const(0x0)  # Pin set to output, default state low
    OUTPUT_HIGH: int = const(0x1)  # Pin set to output, default state high

    def __init__(self, port: I2C, addr: int = DEFAULT_ADDR) -> None:
        """
        Initialize the PCF8574T instance.

        :param port: An I2C object representing the communication bus.
        :param addr: The I2C address of the PCF8574 device.
        :raises ValueError: If the provided address is not valid.
        :raises TypeError: If the provided port is not a valid I2C object.
        :raises OSError: If the device is not found on the I2C bus.
        """
        if not ((0x20 <= addr <= 0x27) or (0x38 <= addr <= 0x3F)):
            raise ValueError(f"Invalid PCF8574x device address: 0x{addr:02X}")

        if not isinstance(port, I2C):
            raise TypeError("Invalid I2C object! Please provide a valid I2C object.")

        self.__i2c_device: I2C = port
        self.__addr: int = addr
        self.__pin_mode: int = 0xFF  # All pins as input initially

        if self.__addr not in self.__i2c_device.scan():
            raise OSError("PCF8574 not found on the I2C bus!")

    def __gpio_expander_read(self, stop: bool = True) -> int:
        """
        Read the current state of all pins from the I/O expander.

        :param stop: Whether to send a stop condition after the read operation.
        :return: The status byte representing the state of all pins.
        :raises RuntimeError: If there is an error during the read operation.
        """
        try:
            data: bytes = self.__i2c_device.readfrom(self.__addr, 1, stop)
            return data[0]  # Return the first byte directly as an integer
        except OSError as read_error:
            raise RuntimeError(f"Expander read error: {read_error}")

    def __gpio_expander_write(self, data: int, stop: bool = True) -> None:
        """
        Write data to the I/O expander.

        :param data: The data to be written to the I/O expander.
        :param stop: Whether to send a stop condition after the write operation.
        :raises RuntimeError: If the expander fails to write.
        """
        try:
            self.__i2c_device.writeto(self.__addr, bytes([data]), stop)
        except OSError as write_error:
            raise RuntimeError(f"Expander write error: {write_error}")

    def gpio_mask_mode(self, mask: int) -> None:
        """
        Write a mask to the I/O expander to set the pin states.

        :param mask: The mask to be written to the I/O expander.
        """
        self.__gpio_expander_write(data=mask)

    def gpio_get_all(self, stop: bool = True) -> int:
        """
        Read the current state of all pins from the I/O expander.

        :param stop: Whether to send a stop condition after the read operation.
        :return: The status byte representing the state of all pins.
        :raises RuntimeError: If there is an error during the read operation.
        """
        return self.__gpio_expander_read(stop=stop)

    def gpio_put_all(self, value: int, stop: bool = True) -> None:
        """
        Write data to the I/O expander to set the pin states.

        :param value: The byte to be written to the I/O expander.
        :param stop: Whether to send a stop condition after the write operation.
        :raises RuntimeError: If the expander fails to write.
        """
        self.__gpio_expander_write(data=value, stop=stop)

    def pin_mode(self, pin: int, mode: int, stop: bool = True) -> None:
        """
        Set the mode (INPUT or OUTPUT) for a specific pin.

        :param pin: The pin to configure (0 to 7).
        :param mode: The mode to set (INPUT_LOW, INPUT_HIGH, OUTPUT_LOW, OUTPUT_HIGH).
        :param stop: Whether to send a stop condition after the write operation.
        :raises ValueError: If the provided pin is not within the valid range.
        """
        if not 0 <= pin <= 7:
            raise ValueError(f"Invalid pin number: {pin}")

        self.__pin_mode &= ~(1 << pin)
        self.__pin_mode |= mode << pin

        # Write the updated pin modes to the I/O expander
        self.__gpio_expander_write(data=self.__pin_mode, stop=stop)

    def writeto_pin(self, pin: int, value: int, stop: bool = True) -> None:
        """
        Write a digital value (0 or 1) to a specific pin.

        :param pin: The pin to write to (0 to 7).
        :param value: The value to write (True or False).
        :param stop: Whether to send a stop condition after the write operation.
        :raises ValueError: If the provided pin is not within the valid range.
        """
        if not 0 <= pin <= 7:
            raise ValueError(f"Invalid pin number: {pin}")

        pin_state: int = self.__gpio_expander_read(stop=False)
        pin_state = (pin_state | (1 << pin)) if value else (pin_state & ~(1 << pin))

        self.__gpio_expander_write(data=pin_state, stop=stop)

    def readfrom_pin(self, pin: int, stop: bool = True) -> bool:
        """
        Read the digital value (0 or 1) from a specific input pin.

        :param pin: The pin to read from (0 to 7).
        :param stop: Whether to send a stop condition after the read operation.
        :return: The digital value (0 or 1) read from the specified pin.
        :raises ValueError: If the provided pin is not within the valid range.
        :raises RuntimeError: If there is an error during the read operation.
        """
        if not 0 <= pin <= 7:
            raise ValueError(f"Invalid pin number: {pin}")

        status: int = self.__gpio_expander_read(stop=stop)
        return (status & (1 << pin)) != 0

    def deinit(self) -> None:
        """
        Clean up and deinitialize the I2C interface.

        This method should be called when you are done using the object,
        to ensure proper resource cleanup.
        """
        self.__i2c_device.deinit()

    def __del__(self) -> None:
        """
        Destructor to ensure the deinitialization of the I2C interface.
        """
        self.deinit()
