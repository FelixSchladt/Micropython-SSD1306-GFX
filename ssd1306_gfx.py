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
    # color   -> 0 = black , 1 = colored | optional
        
    def rect(self, x0, y0, x1 , y1, color = 1):
        for x in range(x0 if x0<x1 else x1, x1+1 if x0<x1 else x0+1):
            for y in range(y0 if y0<y1 else y1, y1+1 if y0<y1 else y0+1):
                self.pixel(x, y , color)
    
    
    ### Draw frame ###
    # draw a hollow frame
    #
    # x0, y0  -> start coordinate
    # width   -> width in pixel
    # height  -> height in pixel
    # f_width -> width of the frame in pixel | optional
    # color   -> 0 = black , 1 = colored | optional
   
    def frame(self, x0 = 0, y0 = 0, x1 = None, y1 = None, f_width = 1, color = 1):
        
        print(x0, y0, x1, y1)
        
        x1 = self.display_width-1 if x1 is None else x1
        y1 = self.display_height-1 if y1 is None else y1
        
        print(x0, y0, x1, y1)
        
        self.rect( x0, y0, (x0-f_width) if x0 > x1 else (x0 + f_width), y1 )
        self.rect( x1, y0, (x1-f_width) if x0 < x1 else (x1 + f_width), y1 )
        
        self.rect( x0, y0, x1, (y0 + f_width) if y0 < y1 else (y0 - f_width))
        self.rect( x0, y1, x1, (y1 - f_width) if y1 > y0 else (y1 + f_width))
    
    
    ### Fill display ###
    # Fill the whole display with color or turn it off
    #
    # color   -> 0 = black , 1 = colored | optional
    
    def fill(self, color = 0):
        self.rect(0, 0, self.display_width-1, self.display_height-1, color)
    
    
    ### Draw line ###
    # draw a line between two points. Based on the Bresenham algorythm
    #
    # x0, y0  -> start coordinate
    # x1, y1  -> end coordinate
    # color   -> 0 = black , 1 = colored | optional
    
    def line(self, x0 , y0 , x1, y1, color = 1):
        for c in self.__bresenham_line(self, x0 , y0 , x1, y1):
            self.pixel(c[0], c[1], color)
    
    ### private sub class of line ###
    def __bresenham_line(self, x0 , y0 , x1, y1, color = 1):
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
            yield x0 + x*xx + y*yx, y0 + x*xy + y*yy
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
    
    
    ### private sub class of circle ###
    def __bresenham_circle(self, x0, y0, r): 
        x, y, p = 0, r, 1-r

        L = []
        L.append((x, y))

        for x in range(int(r)):
            if p < 0:
                p = p + 2 * x + 3
            else:
                y -= 1
                p = p + 2 * x + 3 - 2 * y

            L.append((x, y))

            if x >= y: break

        N = L[:]
        for i in L:
            N.append((i[1], i[0]))

        L = N[:]
        for i in N:
            L.append((-i[0], i[1]))
            L.append((i[0], -i[1]))
            L.append((-i[0], -i[1]))
        
        for i in L:
            yield int(x0+i[0]), int(y0+i[1])
    
    ### Draw line horizontal ###
    # draw a horizontal line spannign the total display
    #
    # y       -> start point (x = 0, y = ?)
    # color   -> 0 = black , 1 = colored | optional
    
    def line_h(self, y, x0 = 0, x1 = None, color = 1):
        x1 = self.display_width-1 if x1 is None else x1
        for x in range(x0, x1, 1 if x1 > x0 else -1):
            self.pixel(x, y , color)
    
    
    ### Draw line vertical ###
    # draw a vertical line spannign the total display
    #
    # y       -> start point (x = ?, y = 0)
    # color   -> 0 = black , 1 = colored  | optional
    
    def line_v(self, x, y0 = 0, y1 = None, color = 1):
        y1 = self.display_height-1 if y1 is None else y1
        for y in range(y0, y1, 1 if y1 > y0 else -1):
            self.pixel(x, y , color)
    
    def triangle(self, x0, y0, x1, y1, x2, y2, f_width = 1, color = 1):
        self.line()
    
     
    

    
    def circle(self, x0 = None, y0 = None, r = None, f_width = 1, color =1): 
        x0 = (self.display_width/2-1) if x0 is None else x0
        y0 = (self.display_height/2-1) if y0 is None else y0
        r = (self.display_height/2-1) if r is None else r
        
        #f_width not working
        
        ###potential fix for missing pixels in multiwidth circles -Y fill gap between the inner and outer circle
        for c in self.__bresenham_circle(x0, y0, r):
            self.pixel(c[0], c[1], color)

    
    def circle_filled(self, x0 = None, y0 = None, r = None, color =1): #Leaves pixels inside circle blank because of the algorythm
        x0 = (self.display_width/2-1) if x0 is None else x0
        y0 = (self.display_height/2-1) if y0 is None else y0
        r = (self.display_height/2-1) if r is None else r
        ##potential fix is to only draw one circle and fill the rest with lines
        
        for g in range(r, 0, -1):
            for c in self.__bresenham_circle(x0, y0, g):
                self.pixel(c[0], c[1], color)

   
        
    
    
    
    ### Progress bar ###
    # Displays percentage visually in a bar
    #
    # y     -> height of the bar on the display
    # percent -> progress in percent | int 75 = 75%
    # symbol  -> choose preffered symbol to be displayed | optional
    # color   -> 0 = black , 1 = colored | optional
    
    def progress_bar(self, y, percent, symbol = "=", color = 0):
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
# Attention: I do not have the possibility to test SPI
# this is written in best faith but without any testing done...
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
    #oled_tools.fill(1)
    #oled_tools.text("Test TEXT", 10, 20, 0)
    oled_tools.frame(10, 10, 120, 62, 5)
    #oled_tools.circle(63,31,31)
    #oled_tools.circle_filled()
    #oled_tools.line_h(63)
    
    #oled_tools.progress_bar(10, 75)
    
    oled_tools.show() # Draws the content of the buffeer onto the Display !!!
    
    
