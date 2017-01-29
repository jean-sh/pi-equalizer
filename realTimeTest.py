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

import pyaudio
import wave
import numpy as np
import time
import struct
import threading
import queue
import math
import audioVisualization as avi
from matrix import Matrix

d = Matrix()
d.set_rotation(270)


def extract(data, frame_count, nb_channels, nb_of_points, q):
    """
    Extracts the audio spectrum from audio data
    :param
    data:
    The audio data to extract the spectrum from
    frame_count:
    The number of frames corresponding to the data
    nb_channels:
    The number of channels of the audio data
    frame_rate:
    The frame rate of the audio data
    nb_of_points:
    The number of points to calculate the Fast Fourier Transform
    q:
    The thread queue to put the intensities in
    """
    data = np.array(struct.unpack('{n}h'.format(n=nb_channels * frame_count), data))

    # Calculate the Fourier Transform coefficients
    fft_array = np.fft.fft(data, nb_of_points)

    # Calculate the power in each frequency
    intensities = []
    for coef in fft_array:
        intensities.append(abs(coef))

    q.put(intensities)


def calculate_frequency_ranges(data, frame_count, frame_rate, nb_channels, nb_of_points, q):
    """
    
    :param
    data:
    The audio data to extract the spectrum from
    frame_count:
    The number of frames corresponding to the data
    nb_channels:
    The number of channels of the audio data
    frame_rate:
    The frame rate of the audio data
    nb_of_points:
    The number of points to calculate the Fast Fourier Transform
    :q
    The thread queue to put the frequencies in
    """
    data = struct.unpack('{n}h'.format(n=nb_channels * frame_count), data)
    data = np.array(data)

    # Calculate the Fourier Transform coefficients
    fft_array = np.fft.fft(data, nb_of_points)

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(fft_array))
    freqs_hertz = []
    for freq in freqs:
        freqs_hertz.append(abs(freq * frame_rate))
    
    #
    length = len(freqs_hertz)
    custom_freqs = [58, 130, 292, 657, 1478, 3325, 7482, 16834]
    
    # Calculate frequency boundaries
    boundaries = []
    for i in range(len(custom_freqs) - 1):
        # Using the geometric mean feels better than arithmetic mean here
        b = math.sqrt((custom_freqs[i] * custom_freqs[i+1]))
        boundaries.append(b)
    boundaries.append(22050)

    q.put(freqs_hertz)
    q.put(boundaries)


def display(freq_ranges, freq_hertz, intensities):
    intensities = avi.avg_and_rescale(freq_ranges, freq_hertz, intensities)
    for i in range(len(freq_ranges)):
        d.set_column(i, d.mode_one(int(intensities[i])))


##
# Plays a wave file and extracts the audio spectrum at the same time
##
def play_and_extract(wav_file):
    wf = wave.open(wav_file, 'rb')
    nb_channels = wf.getnchannels()
    frame_rate = wf.getframerate()
    nb_of_points = 128
    global first_time
    first_time = True
    global freq_ranges
    freq_ranges = []
    global freqs_hertz
    freqs_hertz = []

    # Create a queue for the extract thread and the display thread
    q = queue.Queue()

    # instantiate PyAudio
    pyau = pyaudio.PyAudio()

    # define callback
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)

        # Calculate the frequency groups ONCE
        global first_time
        global freq_ranges
        global freqs_hertz
        if first_time:
            frequency_thread = threading.Thread(target=calculate_frequency_ranges,
                                                args=(data, frame_count, frame_rate, nb_channels, nb_of_points, q))
            frequency_thread.start()
            frequency_thread.join()
            freqs_hertz = q.get()
            freq_ranges = q.get()
            first_time = False

        # Create the extract thread
        extract_thread = threading.Thread(target=extract,
                                          args=(data, frame_count, nb_channels, nb_of_points, q))
        extract_thread.start()

        # Block until extracting is done and queue is empty
        extract_thread.join()
        intensities = q.get()
        
        # Process the extracted data for displaying
        display_thread = threading.Thread(target=display,
                                          args=(freq_ranges, freqs_hertz, intensities))
        display_thread.start()
        display_thread.join()
        return data, pyaudio.paContinue

    # open stream using callback
    stream = pyau.open(format=pyau.get_format_from_width(wf.getsampwidth()),
                       channels=nb_channels,
                       rate=frame_rate,
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
    pyau.terminate()

play_and_extract("stress.wav")
