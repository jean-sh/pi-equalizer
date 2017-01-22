#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  audiotest.py
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

import matplotlib.pyplot as plt
import itertools

##
# Plots the values from one frame as extracted by 'sound_spectrum.py'
##
def extract_and_plot_values_from_ndarray(one_frame):
    with open(one_frame, "r") as frame:
        list_frame = [line.strip("[] \n") for line in frame]

    values_by_line = []
    for i in list_frame:
        values_by_line.append(i.split("  "))

    values_str = list(itertools.chain.from_iterable(values_by_line))
    print(values_str)

    values = []
    for s in values_str:
        try:
            values.append(float(s))
        except ValueError:
            print("error")
            pass
    print(values)
    plt.plot(values, '.')
    plt.ylabel("valeurs")
    plt.show()



##
# Plots the values from one frame as extracted by 'streaming_extractor_music' from Essentia
##
def extract_and_plot_values_from_mel_bands(frame_file):
    with open(frame_file, "r") as frame:
        s_frame = frame.readline()

    s_values = s_frame.split("    ")
    s_values[0] = s_values[0].strip("[")
    s_values[len(s_values) - 1] = s_values[len(s_values) - 1].strip("\n]")

    values = []
    for i, s in enumerate(s_values):
        values.append(float(s))
    print(values)

    plt.plot(values)
    plt.ylabel("valeurs")
    plt.show()


'''
##
# Plays a wave file
##
import pyaudio
import wave
import time
import sys

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

# instantiate PyAudio
p = pyaudio.PyAudio()


# define callback
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
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
    time.sleep(0.5)

# stop stream
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio
p.terminate()
'''