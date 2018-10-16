#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

import pygame

def drawEyeBalls(draw, x,y,squint=False):

    
    x0 = x-2
    y0 = y-2
    x1 = x+2
    y1 = y+2
    

    if squint:
        y1-=1
    
    draw.ellipse([x0,y0,x1,y1], fill=1, outline=1)
    
    x0=x0+8
    x1=x1+8
    draw.ellipse([x0,y0,x1,y1], fill=1, outline=1)


def drawEyeBrow(draw, mode, isRightEye):

    x0 = 0
    y0 = 0
    x1 = 7
    y1 = 1
        
    if isRightEye:
        x0=15-x0
        x1=15-x1
        
    if mode==0:
        draw.line([x0,y0,x1,y1],fill=1)
    elif mode==1:
        y1-=1
        draw.line([x0,y0,x1,y1],fill=1)
    elif mode==-1:
        y1+=1
        draw.line([x0,y0,x1,y1],fill=1)
    
    
def test(device):
    device.contrast(100)
    
    #Eye brows up and down
    for i in [0,1,0,1,0,1,0,1,0]:
        with canvas(device) as draw:
            drawEyeBalls(draw,4,4,squint=False)
            drawEyeBrow(draw, i, isRightEye=False)
            drawEyeBrow(draw, i, isRightEye=True)
            time.sleep(0.3)
    
    
    time.sleep(1)
    
    
        
    #Eye round
    for i in range(3):
        for (x,y) in zip([5,5,4,3,3,3,4,5],[4,5,5,5,4,3,3,3,4]):
            with canvas(device) as draw:
                drawEyeBalls(draw,x,y,squint=False)
                drawEyeBrow(draw, 0, isRightEye=False)
                drawEyeBrow(draw, 0, isRightEye=True)
                time.sleep(0.1)
    
    
    
    #Left center left center
    for i in range(2):
        with canvas(device) as draw:
            drawEyeBalls(draw,3,5,squint=False)
            drawEyeBrow(draw, -1, isRightEye=False)
            drawEyeBrow(draw, -1, isRightEye=True)
            time.sleep(0.3)
            
        with canvas(device) as draw:
            drawEyeBalls(draw,3,5,squint=False)
            drawEyeBrow(draw, 0, isRightEye=False)
            drawEyeBrow(draw, 0, isRightEye=True)
            time.sleep(0.3)
            
    

    
def demo(n, block_orientation, rotate):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
    print("Created device")

    
    pygame.init()
    pygame.mixer.music.load("durin.wav")
    pygame.mixer.music.play()


    time.sleep(1)
    
    pygame.mixer.music.load("mellon.wav")
    pygame.mixer.music.play()


    test(device)
    
    #device.contrast(100)
    #with canvas(device) as draw:
        #draw.ellipse([2,2,6,6], fill=1, outline=1)
     #   drawEyeBalls(draw, x=3,y=5,squint=True)
      #  drawEyeBrow(draw, -1, False)
       # drawEyeBrow(draw, -1, True)
        #draw.line([0,7,8,7],fill=0)
        #draw.rectangle(device.bounding_box, outline="white", fill="black")

    #time.sleep(1)
    #for x in range(256):
    #    with canvas(device) as draw:
    #        text(draw, (0, 0), chr(x), fill="white")
    #        time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=2, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate)
    except KeyboardInterrupt:
        pass
