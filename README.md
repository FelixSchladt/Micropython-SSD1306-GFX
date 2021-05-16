# Micropython SSD1306-tools
Micropython Utility library for Adafruit 0.96" SSD1306 monochrome OLED Display - Basic shapes &amp; examples

### This project includes

- Functions for basic shapes (circle, rectangle, lines, frames, ~~triangles~~)
- Easy setup of an I2C / SPI connection to the display
- Examples

## Content

1. Installation
2. Display setup
3. 1306_tools object initialization
4. Functions
5. Contribute

## Installation

### Prerequisits

Your device needs to bet setuop for micropython [micropython.org tutorial](https://docs.micropython.org/en/v1.15/esp32/tutorial/intro.html)

As development IDE I **personally** recommend [thonny](https://thonny.org/).

This project was wirtten and tested with an ESP32 using an I2C connection but should work fine on other micropython devices.
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

_please consider adding this section_

## First steps

Copy ssd1306.py and ssd1306_tools.py onto your device and safe them.
'''
import ssd1306_tools

## Functions




Please feel invited to contribute and improve!
