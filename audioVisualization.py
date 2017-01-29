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

import audioExtraction as aex
import matplotlib.pyplot as plt
import math

##
# Not used
##
def avg_linear_range(freq_data, intensity_data, nb_of_points=8):
    length = len(freq_data)
    size = length // nb_of_points

    freq_avg = []
    for n in range(nb_of_points):
        f = sum(freq_data[n*size:(n+1)*size]) // size
        freq_avg.append(f)

    intens_avg = []
    for j, frame_intensities in enumerate(intensity_data):
        frame_avg = []
        for n in range(nb_of_points):
            i = sum(frame_intensities[n*size:(n+1)*size]) // size
            frame_avg.append(i)
        intens_avg.append(frame_avg)
    return freq_avg, intens_avg


def avg_custom_range(freq_data, intensity_data):
    """
    Averages intensities in 8 groups in ranges growing as 2.25^n
    :param
    freq_data:
    intensity_data:
    :return:
    """
    length = len(freq_data)
    custom_freqs = [58, 130, 292, 657, 1478, 3325, 7482, 16834]

    # Discard the last half, which only repeats the first half of the array
    for idx, f in enumerate(intensity_data):
        intensity_data[idx] = f[1:(length // 2) + 1]

    # Calculate frequency boundaries
    boundaries = []
    for i in range(len(custom_freqs) - 1):
        b = math.sqrt((custom_freqs[i] * custom_freqs[i+1]))
        boundaries.append(b)
    boundaries.append(22050)

    # Calculate averages
    intens_avg = []
    for frame in intensity_data:
        frame_avg = []
        for bd in boundaries:
            domain = []
            i = 0
            while freq_data[i] < bd:
                domain.append(frame[i])
                i += 1
            frame_avg.append(sum(domain) / len(custom_freqs))
        intens_avg.append(frame_avg)

    return custom_freqs, intens_avg


def avg_custom_range_one_chunk(freq_data, intensity_data):
    """
    Averages intensities in 8 groups in ranges growing as 2.25^n
    :param
    freq_data:
    intensity_data:
    :return:
    """
    length = len(freq_data)
    custom_freqs = [58, 130, 292, 657, 1478, 3325, 7482, 16834]

    # Discard the last half, which only repeats the first half of the array
    intensity_data = intensity_data[1:(length // 2) + 1]

    # Calculate frequency boundaries
    boundaries = []
    for i in range(len(custom_freqs) - 1):
        # Using the geometric mean feels better than arithmetic mean here
        b = math.sqrt((custom_freqs[i] * custom_freqs[i+1]))
        boundaries.append(b)
    boundaries.append(22050)

    # Calculate averages
    intens_avg = []
    i = 0
    for bd in boundaries:
        domain = []
        while freq_data[i] < bd:
            domain.append(intensity_data[i])
            i += 1
        intens_avg.append(sum(domain) / len(custom_freqs))

    return custom_freqs, intens_avg


def bar_plot(freq_data, intensity_data):
    plt.ylim(0, 256)
    plt.bar(freq_data, intensity_data, 1000)
    #plt.yscale("symlog")
    plt.show()


def rescale_intensity(intensity_data):
    # Nothing clever, found through trial and error to get a pleasing visual result
    i_max = 1600000
    i_rescaled = []
    for i in intensity_data:
        i_rescaled.append((i / i_max) * 200 + 55)

    return i_rescaled


freq, intensity = aex.audio_spectrum("stress.wav", nb_of_points=512)
print(intensity)
freq, intensity = avg_custom_range_one_chunk(freq, intensity)
print(freq, intensity)
'''
for f in intensity[6:]:
    plt.loglog(freq, f)
    plt.ylim(0, 220)
    plt.show()
'''