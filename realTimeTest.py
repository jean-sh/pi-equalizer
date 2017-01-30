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
import multiprocessing as mp
import Queue
import math
import audioVisualization as avi
import cv2
from matrix import Matrix
d = Matrix()
d.set_rotation(270)


def extract(data, frame_count, nb_channels):
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
    q:
    The thread queue to put the intensities in
    """
    data = np.array(struct.unpack('{n}h'.format(n=nb_channels * frame_count), data))
    windowed_data = np.multiply(data, np.hanning(len(data)))
    # Calculate the Fourier Transform coefficients
    dft_array = cv2.dft(np.float32(windowed_data))
    # Return the power in each frequency
    magnitudes = np.add(np.sqrt((dft_array*dft_array).sum(axis=1)), 10)
    log_mag = np.log10(magnitudes)
    print(max(log_mag))

    return log_mag


def calculate_frequency_ranges(data, frame_count, frame_rate, nb_channels):
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
    :return
    The frequencies array and the boundaries of the frequency group for displaying
    """
    
    data = np.array(struct.unpack('{n}h'.format(n=nb_channels * frame_count), data))
    # Calculate the Fourier Transform coefficients
    dft_array = cv2.dft(np.float32(data))

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(dft_array))
    freqs_hertz = []
    for freq in freqs:
        freqs_hertz.append(abs(freq * frame_rate))
    
    #
    length = len(freqs_hertz)
    custom_freqs = [58, 130, 292, 657, 1478, 3325, 7482, 16834]
    
    # Calculate frequency boundaries
    boundaries = []
    for i in range(len(custom_freqs) - 1):
        # Using the geometric mean seems better than arithmetic mean here
        b = math.sqrt((custom_freqs[i] * custom_freqs[i+1]))
        boundaries.append(b)
    boundaries.append(22050)

    return freqs_hertz, boundaries


def display(freq_ranges, freq_hertz, intensities):
    intensities = avi.avg_and_rescale(freq_ranges, freq_hertz, intensities)
    for i in range(8):
        d.set_column(7-i, d.mode_two(int(intensities[i])))


##
# Plays a wave file and extracts the audio spectrum at the same time
##
def play_and_extract(wav_file):
    wf = wave.open(wav_file, 'rb')
    nb_channels = wf.getnchannels()
    frame_rate = wf.getframerate()
    global first_time
    first_time = True
    global freq_ranges
    freq_ranges = []
    global freqs_hertz
    freqs_hertz = []
    global round_nb
    round_nb = 1

    # Create a queue for the extract thread and the display thread
    q = Queue.Queue()

    # instantiate PyAudio
    pyau = pyaudio.PyAudio()

    # define callback
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)

        # Calculate the frequency groups ONCE
        global first_time
        global freq_ranges
        global freqs_hertz
        global round_nb
        if first_time:
            freqs_hertz, freq_ranges = calculate_frequency_ranges(data, frame_count, frame_rate, nb_channels)
            first_time = False

        if round_nb > 10:
            intensities = extract(data, frame_count, nb_channels)
            # Process the extracted data for displaying
            display_thread = threading.Thread(target=display,
                                              args=(freq_ranges, freqs_hertz, intensities))
            display_thread.start()
        else:
            round_nb += 1
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
        time.sleep(0.2)

    # stop stream
    stream.stop_stream()
    stream.close()
    wf.close()

    # close PyAudio
    pyau.terminate()

play_and_extract("partymono.wav")
