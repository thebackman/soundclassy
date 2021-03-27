""" red or green """

import sys
from blinkt import set_pixel, set_brightness, show, clear
import time

def red_or_green(color)

    set_brightness(0.1)

    # get the color 
    if color == "red":
        r = 190
        g = 0
        b = 0
    if color == "green":
        r = 45
        g = 175
        b = 20 

    clear()
    for i in range(8):
        set_pixel(i, r, g, b)
    show()
    time.sleep(1)
    clear()

if __name__ == "__main__":
    red_or_green("green")