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

from matrix import Matrix

display = Matrix()
display.set_rotation(270)


def avg_and_rescale(intensities):   
    # Custom slices following a logarithmic progression
    # that is closer to human hearing 
    slice1 = intensities[:7]
    slice2 = intensities[8:15]
    slice3 = intensities[16:31]
    slice4 = intensities[32:63]
    slice5 = intensities[64:127]
    slice6 = intensities[128:255]
    slice7 = intensities[256:511]
    slice8 = intensities[512:]
    
    intens_avg = [sum(slice1/8), sum(slice2/8),
                  sum(slice3/16), sum(slice4/32),
                  sum(slice5/64), sum(slice6/128),
                  sum(slice7/256), sum(slice8/512)]
    # Rescale
    i_max = 6
    i_rescaled = []
    for i in intens_avg:
        i_rescaled.append((i / i_max) * 255)
    return i_rescaled
    

def display_eq(intensities):
    intensities = avg_and_rescale(intensities)
    for i in range(8):
        display.set_column(7-i, display.mode_three(int(intensities[i])))
