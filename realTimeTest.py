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
import audioVisualization as avi


def extract(data, frame_count, nb_channels, frame_rate, q, nb_of_points=128):
    """
    Extracts and plots the audio spectrum of audio data
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
    :return
    The array of frequencies
    The array of corresponding intensities
    """
    data = struct.unpack('{n}h'.format(n=nb_channels * frame_count), data)
    data = np.array(data)

    # Calculate the Fourier Transform coefficients
    fft_array = np.fft.fft(data, nb_of_points)

    # Calculate the power in each frequency
    intensities = []
    for coef in fft_array:
        intensities.append(abs(coef))
    #print(intensities)

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(fft_array))
    freqs_in_hertz = []
    for freq in freqs:
        freqs_in_hertz.append(abs(freq * frame_rate))
    #print(freqs_in_hertz)

    q.put(freqs_in_hertz)
    q.put(intensities)


##
# Plays a wave file and extracts the audio spectrum at the same time
##
def play_and_extract(wav_file):
    wf = wave.open(wav_file, 'r')
    nb_channels = wf.getnchannels()
    frame_rate = wf.getframerate()

    # Create a queue for the extract thread and the display thread
    q = queue.Queue()

    # instantiate PyAudio
    pyau = pyaudio.PyAudio()

    # define callback
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)

        # Create the extract thread
        extract_thread = threading.Thread(target=extract,
                                          args=(data, frame_count, nb_channels, frame_rate, q, 512))
        extract_thread.start()

        # Block until extracting is done and queue is empty
        extract_thread.join()
        freqs = q.get()
        intensities = q.get()

        # Process the extracted data for displaying
        freqs, intensities = avi.avg_custom_range_one_chunk(freqs, intensities)
        intensities = avi.rescale_intensity(intensities)
        print(freqs, intensities)
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
        time.sleep(1)

    # stop stream
    stream.stop_stream()
    stream.close()
    wf.close()

    # close PyAudio
    pyau.terminate()

play_and_extract("stress.wav")