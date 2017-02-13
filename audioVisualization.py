#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  audioVisualization.py
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

from matrix import Display
import numpy as np

display = Display()
display.set_rotation(90)


def avg_and_rescale(magnitudes):   
    # Custom slices following a logarithmic progression
    # that is closer to human hearing 
    slice1 = magnitudes[:7]
    slice2 = magnitudes[8:15]
    slice3 = magnitudes[16:31]
    slice4 = magnitudes[32:63]
    slice5 = magnitudes[64:127]
    slice6 = magnitudes[128:255]
    slice7 = magnitudes[256:511]
    slice8 = magnitudes[512:]
    
    mags_avged = [sum(slice1/8), sum(slice2/8),
                  sum(slice3/16), sum(slice4/32),
                  sum(slice5/64), sum(slice6/128),
                  sum(slice7/256), sum(slice8/512)]
                  
    # Rescale, mag_max determined by trial and error
    mag_max = 5.8
    mag_scaled = []
    for i in mags_avged:
        mag_scaled.append((i / mag_max) * 255)
        
    return mag_scaled
    
    
def avg_and_rescale_2(magnitudes):   
    # Custom slices following a logarithmic progression
    # that is closer to human hearing 
    slice1 = magnitudes[:7]
    slice2 = magnitudes[8:15]
    slice3 = magnitudes[16:31]
    slice4 = magnitudes[32:63]
    slice5 = magnitudes[64:127]
    slice6 = magnitudes[128:255]
    slice7 = magnitudes[256:511]
    slice8 = magnitudes[512:767]
    
    mags_avged = [sum(slice1/len(slice1)), sum(slice2/len(slice2)),
                  sum(slice3/len(slice3)), sum(slice4/len(slice4)),
                  sum(slice5/len(slice5)), sum(slice6/len(slice6)),
                  sum(slice7/len(slice7)), sum(slice8/len(slice8))]
                  
    # Rescale, mag_max determined by trial and error
    mag_max = 6.3
    mag_scaled = []
    for i in mags_avged:
        mag_scaled.append((i / mag_max) * 255)
        
    return mag_scaled
    
    
def avg_and_rescale_3(magnitudes):   
    # Custom slices following a logarithmic progression
    # that is closer to human hearing 
    slice1 = magnitudes[:7]
    slice2 = magnitudes[8:15]
    slice3 = magnitudes[16:31]
    slice4 = magnitudes[32:63]
    slice5 = magnitudes[64:127]
    slice6 = magnitudes[128:255]
    slice7 = magnitudes[256:511]
    slice8 = magnitudes[512:767]
    
    mags_avged = [sum(slice1/len(slice1)), sum(slice2/len(slice2)),
                  sum(slice3/len(slice3)), sum(slice4/len(slice4)),
                  sum(slice5/len(slice5)), sum(slice6/len(slice6)),
                  sum(slice7/len(slice7)), sum(slice8/len(slice8))]
                  
    # Squaring the magnitudes allows for more dynamic variations
    # This is purely visual
    mags_squared = np.square(mags_avged)
                  
    # Rescale, mag_max determined by trial and error
    mag_max = 36
    mag_scaled = []
    for mag in mags_squared:
        mag_scaled.append((mag / mag_max) * 255)
        
    return mag_scaled
    
    
def avg_and_rescale_4(magnitudes):   
    # Custom slices following a logarithmic progression
    # that is closer to human hearing 
    slice1 = magnitudes[:23]
    slice2 = magnitudes[24:47]
    slice3 = magnitudes[48:79]
    slice4 = magnitudes[80:127]
    slice5 = magnitudes[128:191]
    slice6 = magnitudes[192:255]
    slice7 = magnitudes[256:383]
    slice8 = magnitudes[384:575]
    
    mags_avged = [sum(slice1/len(slice1)), sum(slice2/len(slice2)),
                  sum(slice3/len(slice3)), sum(slice4/len(slice4)),
                  sum(slice5/len(slice5)), sum(slice6/len(slice6)),
                  sum(slice7/len(slice7)), sum(slice8/len(slice8))]
                  
    # Squaring the magnitudes allows for more dynamic variations
    # This is purely visual
    mags_squared = np.square(mags_avged)
                  
    # Rescale, mag_max determined by trial and error
    mag_max = 36
    mag_scaled = []
    for mag in mags_squared:
        mag_scaled.append((mag / mag_max) * 255)
        
    return mag_scaled
   
   
def avg_and_rescale_5(magnitudes):   
    # Custom slices following a logarithmic progression
    # that is closer to human hearing 
    slice1 = magnitudes[:23]
    slice2 = magnitudes[24:47]
    slice3 = magnitudes[48:79]
    slice4 = magnitudes[80:127]
    slice5 = magnitudes[128:191]
    slice6 = magnitudes[192:255]
    slice7 = magnitudes[256:383]
    slice8 = magnitudes[384:575]
    
    mags_avged = [sum(slice1/len(slice1)), sum(slice2/len(slice2)),
                  sum(slice3/len(slice3)), sum(slice4/len(slice4)),
                  sum(slice5/len(slice5)), sum(slice6/len(slice6)),
                  sum(slice7/len(slice7)), sum(slice8/len(slice8))]
                  
    # Squaring the magnitudes allows for more dynamic variations
    # This is purely visual
    mags_squared = np.square(mags_avged)
    
    mags_squared = np.multiply(mags_squared, [0.9, 0.95, 1.0, 1.0, 1.0, 1.0, 1.05, 1.1])
                  
    # Rescale, mag_max determined by trial and error
    mag_max = 30
    mag_scaled = []
    for mag in mags_squared:
        mag_scaled.append((mag / mag_max) * 255)
        
    return mag_scaled
        

def display_eq(magnitudes):
    magnitudes = avg_and_rescale(magnitudes)
    for i in range(8):
        display.set_column(7-i, display.m_three(int(magnitudes[i])))


def display_64(magnitudes, mode):
    float_magnitudes = avg_and_rescale_5(magnitudes)
    int_magnitudes = [int(mag) for mag in float_magnitudes]
    if mode == 0:
        display.set_pixels(Display.rainbow(int_magnitudes))
    elif mode == 1:
        display.set_pixels(Display.fire_bow(int_magnitudes))
    elif mode == 2:
        display.set_pixels(Display.ice_bow(int_magnitudes))
    elif mode == 3:
        display.set_pixels(Display.pink_bow(int_magnitudes))
        

def clear_display():
    display.clear()
