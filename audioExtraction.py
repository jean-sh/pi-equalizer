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


def calculate_frequency_ranges(data, frame_count, frame_rate, nb_channels):
    """
    Unused
    """
    
    data = np.array(struct.unpack('{n}h'.format(n=nb_channels * frame_count), data))
    # Calculate the Fourier Transform coefficients
    dft_array = cv2.dft(np.float32(data))

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(dft_array))
    freqs_hertz = []
    for freq in freqs:
        freqs_hertz.append(abs(freq * frame_rate))
    
    # TODO
    length = len(freqs_hertz)
    custom_freqs = [58, 130, 292, 657, 1478, 3325, 7482, 16834]
    
    # Calculate frequency boundaries
    boundaries = []
    for i in range(len(custom_freqs) - 1):
        # Using the geometric mean seems better than arithmetic mean here
        b = np.sqrt((custom_freqs[i] * custom_freqs[i+1]))
        boundaries.append(b)
    boundaries.append(22050)

    return freqs_hertz, boundaries


def calculate_magnitudes(data, frame_count, nb_channels):
    """
    TODO
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
