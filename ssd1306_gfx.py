# MicroPython SSD1306 OLED simple functions library
# Built upon SSD1306 OLED driver:
# https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
# for more complex graphical tools look at the GFX micropython library
#
# Written by Felix Schladt 2022
#
# Contribute to this project on Github:
#
# https://github.com/FelixSchladt/Micropython-SSD1306-GFX
#

from ssd1306 import *
import machine

class SSD1306_GFX:

    ########################################
    #                                      #
    #  GFX class with shape functions      #
    #                                      #
    ########################################

    # Some basic functions are provided through the inherited FrameBuffer class
    # this includes: line, rect, pixel, fill, text and more
    #
    # http://docs.micropython.org/en/latest/pyboard/library/framebuf.html


    ### Draw rectangle ###
    # draw a solid rectangle
    #
    # x0, y0  -> first coordinate
    # x1 , y1   -> second coordinate
    # color   -> 0 = black , 1 = colored | optional

    def rectangle(self, x0, y0, x1 , y1, color = 1):
        self.fill_rect(x0 if x1-x0 >= 0 else x1, y0 if y1-y0 >= 0 else y1, x0-x1 if x1-x0 < 0 else x1, y0-y1 if y1-y0 < 0 else y1, color)


    ### Draw frame ###
    # draw a hollow frame
    #
    # x0, y0  -> start coordinate
    # width   -> width in pixel
    # height  -> height in pixel
    # width -> width of the frame in pixel | optional
    # color   -> 0 = black , 1 = colored | optional

    def frame(self, x0 = 0, y0 = 0, x1 = None, y1 = None, width = 1, color = 1):
        x1 = self.display_width-1 if x1 is None else x1
        y1 = self.display_height-1 if y1 is None else y1

        self.rectangle( x0, y0, (x0 - width) if x0 > x1 else (x0 + width), y1, color )
        self.rectangle( x1, y0, (x1 + width) if x0 > x1 else (x1 - width), y1, color )

        self.rectangle( x0, y0, x1, (y0 + width) if y0 < y1 else (y0 - width), color)
        self.rectangle( x0, y1, x1, (y1 - width) if y0 < y1 else (y1 + width), color)


    ### Draw line ###
    # draw a line between two points. Based on the Bresenham algorithm
    #
    # x0, y0  -> start coordinate
    # x1, y1  -> end coordinate
    # width   -> width in pixel
    # color   -> 0 = black , 1 = colored | optional

    def line_wide(self, x0 = 0 , y0 = 0 , x1 = None, y1 = None, width = 1, color = 1):
        x1 = self.display_width-1 if x1 is None else x1
        y1 = self.display_height-1 if y1 is None else y1
        for offset in range(0, width, 1 if 0 < width else -1):
            self.line( x0 + offset, y0 + offset, x1 + offset, y1+ offset, color)


    ### Draw line horizontal ###
    # draw a horizontal line spannign the total display
    #
    # y       -> start point (x = 0, y = ?)
    # color   -> 0 = black , 1 = colored | optional

    def line_horizontal(self, y, x0 = 0, x1 = None, width = 1, color = 1):
        x1 = self.display_width-1 if x1 is None else x1
        for offset in range(0, width, 1 if 0 < width else -1):
            self.hline(x0, y + offset, x1-x0, color)


    ### Draw line vertical ###
    # draw a vertical line spannign the total display
    #
    # y       -> start point (x = ?, y = 0)
    # color   -> 0 = black , 1 = colored  | optional

    def line_vertical(self, x, y0 = 0, y1 = None, width = 1, color = 1):
        y1 = self.display_height-1 if y1 is None else y1
        for offset in range(0, width, 1 if 0 < width else -1):
            self.vline(x + offset, y0, y1-y0, color)


    ### Draw filled triangle ###
    # draw a solid triangle between 3 coordinates
    #
    # x0, y0  -> first coordinate
    # x1, y1  -> second coordinate
    # x2, y2  -> third coordinate
    # color   -> 0 = black , 1 = colored  | optional

    def triangle_filled(self, x0 = 0, y0 = 0, x1 = None, y1 = None, x2 = None, y2 = 0, color = 1):
        x1 = int(self.display_width/2-1) if x1 is None else x1
        y1 = int(self.display_height-1) if y1 is None else y1
        x2 = int(self.display_width-1) if x2 is None else x2

        l0, l1 = self.__bresenham_line(x0, y0, x1, y1), self.__bresenham_line(x1, y1, x2, y2)
        for y in l0:
            self.line_horizontal(y, min(l0[y]), min(l1[y])+1, color)
            self.line_horizontal(y, max(l0[y]), max(l1[y])+1, color)


    ### Draw triangle ###
    # draw a hollow triangle between 3 coordinates
    #
    # x0, y0  -> first coordinate
    # x1, y1  -> second coordinate
    # x2, y2  -> third coordinate
    # width   -> width in pixel # Does not yet work as expected due to limitations in the line algorithm
    # color   -> 0 = black , 1 = colored  | optional

    def triangle(self, x0 = 0, y0 = 0, x1 = None, y1 = None, x2 = None, y2 = 0, width = 1, color = 1):
        def g_ofs(current, values):
            return (current + 1) if min(values) == current else ((current - 1) if max(values) == current else current)

        x1 = int(self.display_width/2-1) if x1 is None else x1
        y1 = int(self.display_height-1) if y1 is None else y1
        x2 = int(self.display_width-1) if x2 is None else x2

        self.line(x0, y0, x1, y1, color)
        self.line(x0, y0, x2, y2, color)
        self.line(x1, y1, x2, y2, color)

        if width is not 1: # Not working properly yet
            xl, yl = [x0, x1, x2], [y0, y1, y2]
            self.triangle(g_ofs(x0 , [x0, x1, x2]), g_ofs(y0 , [y0, y1, y2]), g_ofs(x1 , [x0, x1, x2]), g_ofs(y1 , [y0, y1, y2]), g_ofs(x2 , [x0, x1, x2]), g_ofs(y2 , [y0, y1, y2]), width-1, color)


    ### Draw hollow circle ###
    # draw a circle with a given radius around center
    #
    # x0, y0  -> center
    # r       -> radius in pixel
    # width   -> width in pixel
    # color   -> 0 = black , 1 = colored  | optional

    def circle(self, x0 = None, y0 = None, r = None, width = 1, color =1):
        x0 = (self.display_width/2-1) if x0 is None else x0
        y0 = (self.display_height/2-1) if y0 is None else y0
        r = (self.display_height/2-1) if r is None else r
        width -= 1

        icoordinates = self.__bresenham_circle(x0, y0, (r-width))
        for y in icoordinates:
            for x in range(0, len(icoordinates[y])):
                self.pixel(icoordinates[y][x], y , color)

        if width is not 0:
            ocoordinates = self.__bresenham_circle(x0, y0, r)
            for y in ocoordinates:
                if min(icoordinates) > y or y > max(icoordinates):
                    self.line_horizontal(y, min(ocoordinates[y]), max(ocoordinates[y])+1, color)
                else:
                    self.line_horizontal(y, min(ocoordinates[y]), min(icoordinates[y])+1, color)
                    self.line_horizontal(y, max(icoordinates[y]), max(ocoordinates[y])+1, color)
                for x in range(0, len(ocoordinates[y])):
                   self.pixel(ocoordinates[y][x], y , color)


    ### Draw filled circle ###
    # draw a solid circle with a given radius around center
    #
    # x0, y0  -> center
    # r       -> radius in pixel
    # color   -> 0 = black , 1 = colored  | optional

    def circle_filled(self, x0 = None, y0 = None, r = None, color = 1):
        x0 = (self.display_width/2-1) if x0 is None else x0
        y0 = (self.display_height/2-1) if y0 is None else y0
        r = (self.display_height/2-1) if r is None else r

        coordinates = self.__bresenham_circle(x0, y0, r)
        for y in coordinates:
            self.line_horizontal(y, min(coordinates[y]), max(coordinates[y])+1, color)


    ### Progress bar ###
    # Displays percentage visually in a bar
    #
    # y     -> height of the bar on the display
    # percent -> progress in percent | int 75 = 75%
    # symbol  -> choose symbol to be displayed | optional
    # color   -> 0 = black , 1 = colored | optional

    def progress_bar(self, y, percent, symbol = "=", color = 0):
        self.text("|", 0, y)
        self.text("|", self.display_width-5, y)
        print((self.display_width- 10 - (self.display_width-10) % 8))
        for i in range(0, ((self.display_width- 10)*(percent/100) - ((self.display_width-10)*(percent/100)) % 8), 8):
            self.text(symbol, i + 5, y)


    ### private sub class of line ###
    # Line drawing based upon the bresenham algorithm
    def __bresenham_line(self, x0 , y0 , x1, y1):
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
        n = {}
        for x in range(dx + 1):
            if n.get(int(y0 + x*xy + y*yy)) is None:
                n[int(y0 + x*xy + y*yy)] = [int(x0 + x*xx + y*yx)]
            else:
                n[int(y0 + x*xy + y*yy)].append(int(x0 + x*xx + y*yx))
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
        return n

    ### private sub class of circle ###
    # Circle drawing based upon the bresenham algorithm
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

        n = {}
        for i in L:
            if n.get(int(y0+i[1])) is None:
                n[int(y0+i[1])] = [int(x0+i[0])]
            else:
                n[int(y0+i[1])].append(int(x0+i[0]))
        return n


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

class SSD1306_I2C_SETUP(SSD1306_I2C, SSD1306_GFX):
    def __init__(self, scl_pin, sda_pin, display_width, display_height, addr=0x3c, external_vcc=False):
        self.display_width  = display_width
        self.display_height = display_height
        self.i2c = machine.SoftI2C(Pin(scl_pin), Pin(sda_pin))

        super().__init__( display_width, display_height, self.i2c, addr, external_vcc)


### Initialization Class SPI ###
# Attention: I do not have the possibility to test SPI
# this is written in best faith but without any testing done...
#
# Please feel free to contribute on github

class SSD1306_SPI_SETUP( SSD1306_SPI, SSD1306_GFX):
    def __init__(self, display_width, display_height, spi, dc, res, cs, external_vcc=False):
        self.display_width  = display_width
        self.display_height = display_height

        super().__init__(self, display_width, display_height, spi, dc, res, cs, external_vcc=False)


### Testing ####

if __name__ == "__main__":

    ssd1306_display = SSD1306_I2C_SETUP(22, 21, 128, 64)

    #ssd1306_display.fill(1)
    ssd1306_display.line_vertical(63, 0, 53, 1)
    ssd1306_display.circle(None, 27, 26)
    ssd1306_display.triangle()
    #ssd1306_display.frame(0, 0, 127, 63, 4)

    ssd1306_display.show() # Draws the content of the buffeer onto the Display !!!


