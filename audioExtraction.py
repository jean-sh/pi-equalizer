#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  audioExtraction.py
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

import numpy as np
import cv2
import struct


def calculate_magnitudes(data, frame_count, nb_channels):
    """
    Takes audio data in wav format, a frame count and the number of channels
    (mono or stereo) and returns an array of magnitude by frequency
    """
    if nb_channels == 2:    # Strip every other sample point to keep only one channel
        data = np.array(struct.unpack('{n}h'.format(n=nb_channels * frame_count), data))[::2]
    else:
        data = np.array(struct.unpack('{n}h'.format(n=nb_channels * frame_count), data))
        
    windowed_data = np.multiply(data, np.hanning(len(data)))
    
    # Calculate the Fourier Transform coefficients
    dft_array = cv2.dft(np.float32(windowed_data))

    # Return the power in each frequency
    magnitudes = np.add(np.sqrt((dft_array*dft_array).sum(axis=1)), 10)
    log_mag = np.log10(magnitudes)
    return log_mag
