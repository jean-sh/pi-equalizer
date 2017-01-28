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


def linear_average(freq_data, intensity_data, nb_of_points=8):
    length = len(freq_data)
    size = length // nb_of_points

    freq_avg = []
    for n in range(nb_of_points):
        f = sum(freq_data[n*size:(n+1)*size]) // size
        freq_avg.append(f)

    inten_avg = []
    for j, frame_intensities in enumerate(intensity_data):
        frame_avg = []
        for n in range(nb_of_points):
            i = sum(frame_intensities[n*size:(n+1)*size]) // size
            frame_avg.append(i)
        inten_avg.append(frame_avg)
    return freq_avg, inten_avg


def bar_plot(freq_data, intensity_data):
    plt.ylim(0, 256)
    plt.bar(freq_data, intensity_data, 1000)
    #plt.yscale("symlog")
    plt.show()


def rescale_intensity(intensity_data):
    max_global = 0
    for f in intensity_data:
        max_in_f = max(f)
        if max_in_f > max_global:
            max_global = max_in_f

    i_rescaled = []
    for f in intensity_data:
        f_rescaled = []
        for i in f:
            f_rescaled.append((i / max_global) * 200 + 55)
        i_rescaled.append(f_rescaled)

    return i_rescaled

'''
freq, intensity = aex.complete_audio_spectrum("stressmono3.wav")
freq, intensity = linear_average(freq, intensity)
intensity = rescale_intensity(intensity)

for f in intensity:
    bar_plot(freq, f)
'''