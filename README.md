# PCF8574T GpioExpander MicroPython Library

[![GitHub License](https://img.shields.io/github/license/zerovijay/PCF8574T?style=social)](LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/zerovijay/PCF8574T)](https://github.com/zerovijay/PCF8574T/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/zerovijay/PCF8574T)](https://github.com/zerovijay/PCF8574T/forks)
[![GitHub issues](https://img.shields.io/github/issues-raw/zerovijay/PCF8574T?style=social)](https://github.com/zerovijay/PCF8574T/issues)
[![GitHub Release](https://img.shields.io/github/v/release/zerovijay/PCF8574T?include_prereleases&display_name=release&style=social)](https://github.com/zerovijay/PCF8574T/releases)

## Overview

The PCF8574/74A MicroPython Library simplifies the process of expanding input and output capabilities via the I2C
interface. It provides an intuitive solution for extending the number of GPIO pins available in MicroPython projects,
making it easier to manage GPIO pins for various applications. With its user-friendly interface and robust
functionality, this library is suitable for a wide range of projects requiring additional I/O expansion.

## Installation

1. Clone the repository into the project directory:

    ```bash
    git clone https://github.com/zerovijay/PCF8574T.git
    ```

## Usage

### Initialization

```python
from machine import I2C, Pin
from PCF8574T import PCF8574T

# Customize I2C configuration, Don't forget to set frequency 100000kHz.
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)

# Initialize the MicroPython_PCF8574T instance
expander = PCF8574T(port=i2c, addr=0x27)
```

### Pin Configuration

```python
# Set pin mode (INPUT)
expander.pin_mode(pin_num=2, mode=expander.INPUT)

# Set pin mode (OUTPUT)
expander.pin_mode(pin_num=5, mode=expander.OUTPUT)
```

### Digital Write

```python
# Write digital value
expander.digital_write(pin_num=5, value=True)
```

### Digital Read

```python
# Read digital value (0 or 1) from the input pin
value = expander.digital_read(pin_num=2)
```

For more examples, see the [Examples directory](example).

## Important Notes

- The NXP [PCF8574/74A](docs/PCF8574_PCF8574A.pdf) and [Texas Instrument PCF8574](docs/pcf8574.pdf) are functionally the
  same, but have a different slave address.
- Ensure a valid I2C object for communication.
- Macro: `PIN_MIN` and `PIN_MAX` Pin numbering from 0 to 7.
- Macro: `INPUT`, `INPUT_PULLUP`, `OUTPUT`, `OUTPUT_PULLUP` representing pin modes.
- Robust exception handling implemented for potential I2C communication errors.

## Contribution

Contributions to the GpioExpander Library are highly appreciated. If you encounter any issues or have suggestions for
improvements, please create an issue or submit a pull request.

இந்த PCF8574T மென்பொருள் நூலகத்திற்கான பங்களிப்புகள் மிகவும் ஊக்குவிக்கப்படுகின்றன! உங்களுக்கு ஏதேனும் சிக்கல்கள்
ஏற்பட்டாலோ அல்லது மேம்பாடுகளுக்கான பரிந்துரைகள் இருந்தாலோ, தயவுசெய்து 'சிக்கல்' ஒன்றை உருவாக்கவும் அல்லது இழுக்கும்
கோரிக்கையைச் சமர்ப்பிக்கவும்.

நன்றி.

## License

This library is released under the [MIT License](LICENSE).
