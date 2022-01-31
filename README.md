# Micropython SSD1306-GFX
Micropython Utility library for Adafruit 0.96" SSD1306 monochrome OLED Display - GFX functions &amp; examples

### This project includes

- GFX pixel drawing functions for basic shapes (circle, rectangle, lines, frames, triangles)
- Easy setup of an I2C / SPI connection to the display
- Bresenham algorithm for drawing cleaner lines and circles
- Examples
  
  
## Warning

This project was written just **for fun and personal use**. 
Altough depreciated [Adafruits's GFX Library](https://github.com/adafruit/micropython-adafruit-gfx/blob/master/gfx.py) probably provides better performance
  
  

## Installation

### Prerequisits

Your device needs to bet setup for micropython.<br>
If not follow this [tutorial](https://docs.micropython.org/en/v1.15/esp32/tutorial/intro.html) from micropython.org.<br>

As development IDE I **personally** recommend [thonny](https://thonny.org/).  

This project was wirtten and tested with an ESP32 using an I2C connection but it should work fine on other micropython devices.  
The SPI implemenatation is not yet tested.  


### This library requires the display driver for SSD1306

Keep a copy of [ssd1306.py](https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py) in the same directory
  
  
## Display setup

### I2C

| I2C Device | ESP32| 
| ------- | --------- |
| SDA | SDA default is **GPIO 21** | 
| SCL | SCL default is **GPIO 22** |
| GND | GND |
| VCC | **3.3V** and **5V** should work |

| I2C Device | ESP8266| 
| ------- | --------- |
| SDA | SDA default is **GPIO 04** | 
| SCL | SCL default is **GPIO 05** |
| GND | GND |
| VCC | **3.3V** and **5V** should work |

### SPI

_please consider contributing to this section..._

## First steps

#### Copy ssd1306.py and ssd1306_gfx.py onto your device and safe them.
Keep them in the same directory on the micropython device

#### Import the Library classes
the ssd1306_gfx class inherits the methods of the ssd1306.py class.

```python
import ssd1306_gfx
```

#### Initiliazition of the connection by calling the SSD1306_I2C_SETUP or SSD1306_SPI_SETUP class
**Here I2C:** This initializes the I2C connection and the driver class

```pythonn
ssd1306_display = SSD1306_I2C_SETUP(22, 21, 128, 64)
// ssd1306_display = SSD1306_I2C_SETUP(SCL Pin, SDA Pin, display width, display height)
```

#### Draw a simple shape

```python
ssd1306_display.triangle( 0, 0, 25 , 0, 25, 63)
ssd1306_display.circle(None, None, None, 3) #Utilizes default values
ssd1306_display.text("Test TEXT", 10, 20, 0)

ssd1306_display.show() #Writes the buffer onto the display
```


Please feel invited to contribute and improve!
