#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  realTimeTest.py
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


##
# Plays a wave file
##
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import time
import struct


wf = wave.open("heaven30.wav", 'r')

# instantiate PyAudio
p = pyaudio.PyAudio()


# define callback
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    
    nb_of_channels = wf.getnchannels()

    nb_of_points = 128
    data = struct.unpack('{n}h'.format(n=nb_of_channels * frame_count), data)
    data = np.array(data)

    # Calculate the Fourier Transform coefficients
    fft_array = np.fft.fft(data, nb_of_points)

    # Calculate the power in each frequency
    intensities = []
    for coef in fft_array:
        intensities.append(abs(coef))

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(fft_array))

    return (data, pyaudio.paContinue)

# open stream using callback
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream
stream.start_stream()

# wait for stream to finish
while stream.is_active():
    time.sleep(0.1)

# stop stream
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio
p.terminate()

