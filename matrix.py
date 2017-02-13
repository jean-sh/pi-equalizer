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
import numpy as np


class Colors:
    black = [0, 0, 0]
    white = [255, 255, 255]

    # Bright
    b_magenta = [255, 0, 255]
    b_violet = [128, 0, 255]
    b_blue = [64, 64, 255]
    b_electric = [0, 128, 255]
    b_cyan = [0, 255, 255]
    b_emerald = [0, 255, 128]
    b_green = [0, 255, 0]
    b_citrus = [128, 255, 0]
    b_yellow = [255, 255, 0]
    b_orange = [255, 128, 0]
    b_red = [255, 0, 0]
    b_fashion = [255, 0, 128]

    # Medium
    m_magenta = [192, 0, 192]
    m_violet = [96, 0, 192]
    m_blue = [48, 48, 192]
    m_electric = [0, 96, 192]
    m_cyan = [0, 192, 192]
    m_emerald = [0, 192, 96]
    m_green = [0, 192, 0]
    m_citrus = [96, 192, 0]
    m_yellow = [192, 192, 0]
    m_orange = [192, 96, 0]
    m_red = [192, 0, 0]
    m_fashion = [192, 0, 96]
    m_white = [128, 128, 128]

    # Dark
    d_magenta = [128, 0, 128]
    d_violet = [96, 0, 128]
    d_blue = [0, 0, 160]
    d_electric = [0, 64, 128]
    d_cyan = [0, 128, 128]
    d_emerald = [0, 128, 64]
    d_green = [0, 128, 0]
    d_citrus = [64, 128, 0]
    d_yellow = [128, 128, 0]
    d_orange = [128, 64, 0]
    d_red = [128, 0, 0]
    d_fashion = [128, 0, 64]
    
    # Desatured
    u_magenta = [128, 96, 128]
    u_violet = [128, 96, 160]
    u_blue = [96, 96, 160]
    u_electric = [96, 128, 160]
    u_cyan = [96, 160, 160]
    u_emerald = [96, 160, 128]
    u_green = [96, 160, 96]
    u_citrus = [128, 160, 96]
    u_yellow = [160, 160, 96]
    u_orange = [160, 128, 96]
    u_red = [160, 96, 96]
    u_fashion = [192, 96, 128]

    # Rainbows
    rainbow = [d_violet, d_blue, m_cyan, m_green, b_yellow, b_orange, b_red, b_red]
    ice_bow = [d_violet, d_blue, m_electric, m_cyan, b_cyan, b_emerald, white, white]
    fire_bow = [white, b_yellow, b_yellow, b_orange, m_orange, b_red, b_red, b_red]
    pink_bow = [u_violet, u_magenta, white, m_magenta, b_magenta, b_fashion, b_fashion, white]
    reverse_bow = [d_red, m_orange, m_yellow, m_green, b_cyan, b_blue, b_violet, b_violet]


class Display(SenseHat):
    """
    Class containing additional methods for operating the LED matrix
    """

    def __init__(self):
        SenseHat.__init__(self)

    def set_column(self, col, pixel_list):
        """
        Accepts a column number and a list of 8 pixels and sets	the pixels
        in this column to the values in the list (from bottom to top)
        """
        for x in range(8):
            self.set_pixel(x, col, pixel_list[x])

    @staticmethod
    def display_m_3(magnitudes):
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
                pixels.append(Colors.rainbow[i])
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(Colors.rainbow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(Colors.black)
                i += 1
        return pixels
    
    @staticmethod
    def rainbow(magnitudes):
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
                pixels.append(np.divide(Colors.rainbow[i], (2 - (i / 8))))
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(Colors.rainbow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(Colors.black)
                i += 1
        return pixels
    
    @staticmethod
    def ice_bow(magnitudes):
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
                pixels.append(np.divide(Colors.ice_bow[i], (2-(i/8))))
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(Colors.ice_bow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(Colors.black)
                i += 1
        return pixels
        
    @staticmethod
    def fire_bow(magnitudes):
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
                pixels.append(np.divide(Colors.fire_bow[i], (2 - (i / 8))))
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(Colors.fire_bow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(Colors.black)
                i += 1
        return pixels
        
    @staticmethod
    def pink_bow(magnitudes):
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
                pixels.append(np.divide(Colors.pink_bow[i], (2 - (i / 8))))
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(Colors.pink_bow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(Colors.black)
                i += 1
        return pixels
        
    @staticmethod
    def reverse_bow(magnitudes):
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
                pixels.append(np.divide(Colors.reverse_bow[i], (2 - (i / 8))))
                i += 1
                mag -= 32
            if mag > 0:
                pixels.append(np.floor_divide(Colors.reverse_bow[i], (32 / mag)))
                i += 1
            while i < 8:
                pixels.append(Colors.black)
                i += 1
        return pixels
