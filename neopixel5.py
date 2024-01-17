##########################################################################################################
# neopixel5.py 1/17/24 Pico W Lesson 52                                                                  #
# 16 rows x 16 columns LED array = 256 LEDs -> 2D matrix                                                 #
# supplemental power supply to support 64 LEDs at reduced brightness                                     #
# demo1 = expanded homework assignment; demo2 = circle; demo3 = trace perimeter of square                #
##########################################################################################################

from machine import Pin
from math import sin, cos, pi
from neopixel import NeoPixel
import time

neopix_pin = 0
brightness = .05
rows, cols = (16,16)

# define ( (Red), (Green), (Blue), (Orange), (Cyan), (Yellow) ) : tuples
RGBOCY=((int(255*brightness),0,0), (0, int(255*brightness),0), (0,0, int(255*brightness)), (int(255*brightness), int(165*brightness),0),
         (0, int(255*brightness),int(255*brightness)), ((int(255*brightness),int(255*brightness),0))) #R,G,B,Oran,Cyan,Yell
R,G,B,O,C,Y = RGBOCY  # unpack tuples into discrete colors
matrix  = [ [(0,0,0)]*cols for i in range(rows)]

def demo1() ->None:
    '''bouncing balls to and from either end of pixel strip'''
    num_pixels=112
    delay=.03
    np = NeoPixel(Pin(0), num_pixels)
    offset= -1; cnt=0
    try:
        for iteration in range(num_pixels*3):
            offset = -offset if  (cnt in {0, (num_pixels-1)} ) else offset
            np.fill(B)
            np[cnt] = R
            np[(num_pixels-1)-cnt] = G
            np.write()
            cnt+=offset
            time.sleep(delay)
    finally:
        np.fill((0,0,0))
        np.write()
    
def demo2() ->None:
    '''circle on 16x16 pixel array'''
    radius = 8
    delay=.0005
    num_pixels=256
    np = NeoPixel(Pin(0), num_pixels)
    
    for iteration in range(6):
        for degrees in range(0, 361, 10):
            rads = degrees * pi/180
            x=int(radius*cos(rads))
            y= int(radius*sin(rads))
            matrix[7+x][7+y] = R  #draw pixel from offset of center of circle; intellisense is confused
            matrix[7][7] = B   #center of matrix -> blue pixel; intellisense is confused
            index= 7*16+7  # calc index into 2D matrix
            np[index] = matrix[7][7]
            np.write()
            if (7+x) % 2 == 0:  #pixel numbering differs between even and odd rows
                y= -7 if y<-7 else y    # constrain LED to physical array
                index = (7+x)*16 + 7+y  # calculate LED index into 2D matrix[row][column]
                np[index]=R
                np.write()
                time.sleep(delay)
                np.fill((0,0,0))
            else:   #odd row pixel numbering different from even rows
                if x== -8: x=-7             # constrain LED to physical array
                index= (7+x)*16 + (15-7-y)  # calculate LED index into 2D matrix[row][column]
                np[index]=R
                np.write()
                time.sleep(delay)
                np.fill((0,0,0))
    np.fill((0,0,0))
    np.write()

def demo3() ->None:
    '''pixels traverse perimeter of 16x16 square'''
    num_pixels=256
    delay=.01
    np = NeoPixel(Pin(0), num_pixels)

    for iteration in range(4):
        row=0
        for column in range(16):
            matrix[row][column]=R # intellisense is confused
            index=row*16 + column
            np[index]=matrix[row][column]
            np.write()
            time.sleep(delay)
        time.sleep(delay)
        np.fill((0,0,0))
        np.write()
        for row in range(16):
            if row%2 == 0:
                column = 15
            else:  column = 0
            matrix[row][column]=R  # intellisense is confused
            index=16*row + column
            np[index]=matrix[row][column]
            np.write()
            time.sleep(delay)
        np.fill((0,0,0))
        np.write()
        row=15
        for column in range(16):
            matrix[row][column]=R  # intellisense is confused
            index=row*16 + column
            np[index]=matrix[row][column]
            np.write()
            time.sleep(delay)
        time.sleep(delay)
        np.fill((0,0,0))
        np.write()
        for row in range(15,-1, -1):
            if row % 2 == 0:  #even and odd rows are numbered differently
                column = 0
            else:  column = 15
            matrix[row][column]=R  # intellisense is confused
            index=16*row + column
            np[index]=matrix[row][column]
            np.write()
            time.sleep(delay)
        np.fill((0,0,0))
        np.write()

demo1()
demo2()
demo3()
