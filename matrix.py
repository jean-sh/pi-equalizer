#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  matrix.py
#  
# MIT License
#
# Copyright (c) 2017 Jean Vincent
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sense_hat import SenseHat
import time
import numpy as np

class Display(SenseHat):
    """
    Class containing additional methods for operating the LED matrix
    """

    def __init__(self):
        SenseHat.__init__(self)
        
        # Color definitions:
        self.black = [0, 0, 0]
        self.indigo = [80, 30, 128]
        self.electric = [30, 115, 128]
        self.lime = [75, 230, 180]
        self.yellow = [215, 215, 90]
        self.orange = [235, 175, 60]
        self.fire = [245, 150, 70]
        self.red = [255, 110, 110]
        self.scarlett = [255, 190, 190]
        self.rainbow = [self.indigo, self.electric, self.lime,
                        self.yellow, self.orange, self.fire, self.red, self.scarlett]

    def set_column(self, col, pixel_list):
        """
        Accepts a column number and a list of 8 pixels and sets	the pixels
        in this column to the values in the list (from bottom to top)
        """
        for x in range(8):
            self.set_pixel(x, col, pixel_list[x])
              
              
    def display_mode_1(self, magnitudes):
        '''
        Returns a 64 pixel list representing one frame
        of the equalizer to display according to
        the list of magnitudes it receives
        
        It's ugly but somewhat fast
        '''
        for mag in magnitudes:
            if mag > 255:
                mag = 255
        zero_p = [0, 0, 0]
        pixels = []
        print("in mode 1")
        for mag in magnitudes:
            full_p = [mag // 3, mag // 2, mag]
            half_p = [mag // 4, mag // 3, mag // 2]
            if mag > 127:
                if mag > 191:
                    if mag > 223:
                        if mag > 239:
                            for i in range(8):
                                #print("> 239")
                                pixels.append(full_p)
                        else:
                            #print("> 223")
                            for i in range(7):
                                pixels.append(full_p)
                            pixels.append(half_p)
                    elif mag > 207:
                        #print("> 207")
                        for i in range(7):
                            pixels.append(full_p)
                        pixels.append(zero_p)
                    else:
                        #print("> 191")
                        for i in range(6):
                            pixels.append(full_p)
                        pixels.append(half_p)
                        pixels.append(zero_p)
                elif mag > 159:
                    if mag > 175:
                        #print("> 175")
                        for i in range(6):
                            pixels.append(full_p)
                        pixels.append(zero_p)
                        pixels.append(zero_p)
                    else:
                        #print("> 159")
                        for i in range(5):
                            pixels.append(full_p)
                        pixels.append(half_p)
                        pixels.append(zero_p)
                        pixels.append(zero_p)
                elif mag > 143:
                    #print("> 143")
                    for i in range(5):
                        pixels.append(full_p)
                    pixels.append(zero_p)
                    pixels.append(zero_p)
                    pixels.append(zero_p)
                else: # mag > 127
                    for i in range(4):
                        pixels.append(full_p)
                    pixels.append(half_p)
                    pixels.append(zero_p)
                    pixels.append(zero_p)
                    pixels.append(zero_p)
                    
            elif mag > 63:
                if mag > 95:
                    if mag > 111:
                        #print("> 111")
                        for i in range(4):
                            pixels.append(full_p)
                        pixels.append(zero_p)
                        pixels.append(zero_p)
                        pixels.append(zero_p)
                        pixels.append(zero_p)
                    else: # mag > 95
                        #print("> 95")
                        pixels.append(full_p)
                        pixels.append(full_p)
                        pixels.append(full_p)
                        pixels.append(half_p)
                        for i in range(4):
                            pixels.append(zero_p)
                elif mag > 79:
                    #print("> 79")
                    pixels.append(full_p)
                    pixels.append(full_p)
                    pixels.append(full_p)
                    for i in range(5):
                        pixels.append(zero_p)
                else: # mag > 63
                    #rint("> 63")
                    pixels.append(full_p)
                    pixels.append(full_p)
                    pixels.append(half_p)
                    for i in range(5):
                        pixels.append(zero_p)
            elif mag > 31:
                if mag > 47:
                    #print("> 47")
                    pixels.append(full_p)
                    pixels.append(full_p)
                    for i in range(6):
                        pixels.append(zero_p)
                else: # mag > 31:
                    #print("> 31")
                    pixels.append(full_p)
                    pixels.append(half_p)
                    for i in range(6):
                        pixels.append(zero_p)
            elif mag > 15:
                #print("> 15")
                pixels.append(full_p)
                for i in range(7):
                    pixels.append(zero_p)
            else:
                #print("> 0")
                pixels.append(half_p)
                for i in range(7):
                    pixels.append(zero_p)
        return pixels
        
     
    def display_mode_2(self, magnitudes):
        '''
        Returns a 64 pixel list representing one frame
        of the equalizer to display according to
        the list of magnitudes it receives
        
        It's ugly but somewhat fast
        '''
        for mag in magnitudes:
            if mag > 255:
                mag = 255
        
        
        pixels = []

        for mag in magnitudes:
            if mag > 127:
                if mag > 191:
                    if mag > 223:
                        if mag > 239:
                            for i in range(8):
                                #print("> 239")
                                pixels.append(self.rainbow[i])
                        else:
                            #print("> 223")
                            for i in range(7):
                                pixels.append(self.rainbow[i])
                            pixels.append([c // 2 for c in self.rainbow[i]])
                    elif mag > 207:
                        #print("> 207")
                        for i in range(7):
                            pixels.append(self.rainbow[i])
                        pixels.append(self.black)
                    else:
                        #print("> 191")
                        for i in range(6):
                            pixels.append(self.rainbow[i])
                        pixels.append([c // 2 for c in self.rainbow[i]])
                        pixels.append(self.black)
                elif mag > 159:
                    if mag > 175:
                        #print("> 175")
                        for i in range(6):
                            pixels.append(self.rainbow[i])
                        pixels.append(self.black)
                        pixels.append(self.black)
                    else:
                        #print("> 159")
                        for i in range(5):
                            pixels.append(self.rainbow[i])
                        pixels.append([c // 2 for c in self.rainbow[i]])
                        pixels.append(self.black)
                        pixels.append(self.black)
                elif mag > 143:
                    #print("> 143")
                    for i in range(5):
                        pixels.append(self.rainbow[i])
                    pixels.append(self.black)
                    pixels.append(self.black)
                    pixels.append(self.black)
                else: # mag > 127
                    for i in range(4):
                        pixels.append(self.rainbow[i])
                    pixels.append([c // 2 for c in self.rainbow[i]])
                    pixels.append(self.black)
                    pixels.append(self.black)
                    pixels.append(self.black)
                    
            elif mag > 63:
                if mag > 95:
                    if mag > 111:
                        #print("> 111")
                        for i in range(4):
                            pixels.append(self.rainbow[i])
                        pixels.append(self.black)
                        pixels.append(self.black)
                        pixels.append(self.black)
                        pixels.append(self.black)
                    else: # mag > 95
                        #print("> 95")
                        pixels.append(self.rainbow[i])
                        pixels.append(self.rainbow[i])
                        pixels.append(self.rainbow[i])
                        pixels.append([c // 2 for c in self.rainbow[i]])
                        for i in range(4):
                            pixels.append(self.black)
                elif mag > 79:
                    #print("> 79")
                    pixels.append(self.rainbow[i])
                    pixels.append(self.rainbow[i])
                    pixels.append(self.rainbow[i])
                    for i in range(5):
                        pixels.append(self.black)
                else: # mag > 63
                    #rint("> 63")
                    pixels.append(self.rainbow[i])
                    pixels.append(self.rainbow[i])
                    pixels.append([c // 2 for c in self.rainbow[i]])
                    for i in range(5):
                        pixels.append(self.black)
            elif mag > 31:
                if mag > 47:
                    #print("> 47")
                    pixels.append(self.rainbow[i])
                    pixels.append(self.rainbow[i])
                    for i in range(6):
                        pixels.append(self.black)
                else: # mag > 31:
                    #print("> 31")
                    pixels.append(self.rainbow[i])
                    pixels.append([c // 2 for c in self.rainbow[i]])
                    for i in range(6):
                        pixels.append(self.black)
            elif mag > 15:
                #print("> 15")
                pixels.append(self.rainbow[i])
                for i in range(7):
                    pixels.append(self.black)
            else:
                #print("> 0")
                pixels.append([c // 2 for c in self.rainbow[i]])
                for i in range(7):
                    pixels.append(self.black)
        return pixels
        
    def display_mode_3(self, magnitudes):
        """
        Takes an array of 8 magnitudes and returns
        the corresponding matrix of 8 8-pixel columns
        """
        pixels = []
        for mag in magnitudes:
            if mag > 255:
                mag = 255
            i = 0
            while mag > 31:
                pixels.append(self.rainbow[i])
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(self.rainbow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(self.black)
                i += 1
        return pixels
    
    
    def display_mode_4(self, magnitudes):
        """
        Takes an array of 8 magnitudes and returns
        the corresponding matrix of eight 8-pixel columns
        """
        pixels = []
        for mag in magnitudes:
            if mag > 255:
                mag = 255
                
            i = 0
            while mag > 31:
                pixels.append(np.divide(self.rainbow[i], (2-(i/8))))
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(self.rainbow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(self.black)
                i += 1
        return pixels
