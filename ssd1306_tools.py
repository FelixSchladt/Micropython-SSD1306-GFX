# MicroPython SSD1306 OLED simple functions library
# Built upon SSD1306 OLED driver:
# https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
# for more complex graphical tools look at the GFX micropython library
#
# Written by Felix Schladt May 2021
#
# Contribute to this project on Github:
#

from ssd1306 import *
import machine

class SSD1306_TOOLS:
    
    ########################################
    #                                      #
    #  Tool class with different functions #
    #                                      #
    ########################################
    
    
    ### Draw rectangle ###
    # draw a solid rectangle
    #
    # x0, y0  -> first coordinate
    # width   -> second coordinate
    # color   -> 0 = black , 1 = filled | optional
        
    def rect(self, x0, y0, x1 , y1, color = 1):
        for x in range(x0 if x0<x1 else x1, x1+1 if x0<x1 else x0+1):
            for y in range(y0 if y0<y1 else y1, y1+1 if y0<y1 else y0+1):
                self.pixel(x, y , color)
    
    
    ### Draw line ###
    # draw a line between two points. Based on the Bresenham algorythm
    #
    # x0, y0  -> start coordinate
    # x1, y1  -> end coordinate
    # color   -> 0 = black , 1 = filled | optional
    
    def line(self, x0 , y0 , x1, y1, color = 1):
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            self.pixel( x0 + x*xx + y*yx, y0 + x*xy + y*yy, color)
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
    
    
    ### Draw line horizontal ###
    # draw a horizontal line spannign the total display
    #
    # y       -> start point (x = 0, y = ?)
    # color   -> 0 = black , 1 = filled | optional
    
    def line_h(self, y, x0 = 0, x1 = "width", color = 1):
        x1 = self.display_width-1 if str(x1) else x1
        for x in range(x0, x1, 1 if x1 > x0 else -1):
            self.pixel(x, y , color)
    
    
    ### Draw line vertical ###
    # draw a vertical line spannign the total display
    #
    # y       -> start point (x = ?, y = 0)
    # color   -> 0 = black , 1 = filled  | optional
    
    def line_v(self, x, y0 = 0, y1 = "height", color = 1):
        y1 = self.display_height-1 if str(y1) else y1
        for y in range(y0, y1, 1 if y1 > y0 else -1):
            self.pixel(x, y , color)
    
    
    ### Draw frame ###
    # draw a hollow frame
    #
    # x0, y0  -> start coordinate
    # width   -> width in pixel
    # height  -> height in pixel
    # f_width -> width of the frame in pixel | optional
    # color   -> 0 = black , 1 = filled | optional
   
    def frame(self, x0 = 0, y0 = 0, x1 = "width", y1 = "height", f_width = 1, color = 1):
        x1 = self.display_width-1 if str(x1) else x1
        y1 = self.display_height-1 if str(y1) else y1
    
        self.rect( x0, y0, x0-f_width if x0 > x1 else x0 + f_width, y1 )
        self.rect( x1, y0, x1-f_width if x0 < x1 else x1 + f_width, y1 )
        
        self.rect( x0, y0, x1, (y0 + f_width) if y0 < y1 else (y0 - f_width))
        self.rect( x0, y1, x1, (y1 - f_width) if y1 > y0 else (y1 + f_width))
        
        
    ### Clear display ###
    # Fill the whole display in one color // black = off
    #
    # color   -> 0 = black , 1 = filled | optional
    
    def clear_display(self, color = 0):
        self.rect(0, 0, self.display_width-1, self.display_height-1, color)
    
    
    ### Progress bar ###
    # Displays percentage visually in a bar
    #
    # y     -> height of the bar on the display
    # percent -> progress in percent | int 75 = 75%
    # symbol  -> choose preffered symbol to be displayed | optional
    
    def progress_bar(self, y, percent, symbol = "="):
        self.text("|", 0, y)
        self.text("|", self.display_width-5, y)
        print((self.display_width- 10 - (self.display_width-10) % 8))
        for i in range(0, ((self.display_width- 10)*(percent/100) - ((self.display_width-10)*(percent/100)) % 8), 8):
            self.text(symbol, i + 5, y)
        

### Initialization Class I2C ###
# Returns an object including the I2C connection(self.i2c), inherits the
# functionality of the SSD1306 driver class and of the SSD1306_tools class
#
# scl_pin        -> SCL I/O Pin | int
# sda_pin        -> SDA I/O Pin | int
# display_width  -> display width in pixel | int
# display_height -> display height in pixel | int
#
# Example:
# display_object = SSD1306_TOOLS_I2C(Pin(SCL), Pin(SDA), display width, display height)

class SSD1306_TOOLS_I2C(SSD1306_TOOLS, SSD1306_I2C):
    def __init__(self, scl_pin, sda_pin, display_width, display_height, addr=0x3c, external_vcc=False):
        self.display_width  = display_width
        self.display_height = display_height
        self.i2c = machine.SoftI2C(Pin(scl_pin), Pin(sda_pin))
        
        super().__init__( display_width, display_height, self.i2c, addr, external_vcc)

########################################################
# Attention: I do not have the possibility to use SPI
# this is written in best faith but without any testing....
#
# Please feel free to contribute on github


class SSD1306_TOOLS_SPI( SSD1306_SPI, SSD1306_TOOLS):
    def __init__(self, display_width, display_height, spi, dc, res, cs, external_vcc=False):
        self.display_width  = display_width
        self.display_height = display_height
        
        super().__init__(self, display_width, display_height, spi, dc, res, cs, external_vcc=False)
  

### Testing ####

if __name__ == "__main__":
    
    oled_tools = SSD1306_TOOLS_I2C(22, 21, 128, 64)
    #oled_tools.frame(127, 0, 0, 63, 2)
    #oled_tools.rect(127, 63 , 0 , 63)  
    oled_tools.frame(127, 63, 0, 0, 3)
    #oled_tools.line_h(63)
    
    #oled_tools.progress_bar(10, 75)
    
    oled_tools.show() # Draws the content of the buffeer onto the Display !!!
    
    
