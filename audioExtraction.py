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

import matplotlib.pyplot as plt
import numpy as np
import wave
import struct


def audio_spectrum(wav_file_path, nb_of_frames=2205, nb_of_points=128):
    """
    Extracts and plots the audio spectrum of a wav file from the first frames
    :param
    wav_file_path:
    The wav file to extract the spectrum from
    nb_of_frames:
    The number of frames to extract the spectrum from
    nb_of_points:
    The number of points to calculate the Fast Fourier Transform
    :return
    The array of frequencies
    The array of corresponding intensities
    """

    wav_file = wave.open(wav_file_path, 'r')
    data = wav_file.readframes(nb_of_frames)
    sampling_rate = wav_file.getframerate()
    nb_of_channels = wav_file.getnchannels()
    print(wav_file.tell())
    wav_file.close()

    data = struct.unpack('{n}h'.format(n=nb_of_channels * nb_of_frames), data)
    data = np.array(data)

    # Calculate the Fourier Transform coefficients
    fft_array = np.fft.fft(data, nb_of_points)

    # Calculate the power in each frequency
    intensities = []
    for coef in fft_array:
        intensities.append(abs(coef))
    print(intensities)

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(fft_array))
    freqs_in_hertz = []
    for freq in freqs:
        freqs_in_hertz.append(abs(freq * sampling_rate))
    print(freqs_in_hertz)

    plt.plot(freqs_in_hertz, intensities)
    #plt.xscale("log")
    #plt.yscale("log")
    plt.show()

    return freqs_in_hertz, intensities


# audio_spectrum("test.wav", nb_of_points=2048)


def complete_audio_spectrum(wav_file_path, sample_size=2048, nb_of_points=2048):
    """
    Extracts the audio spectrum of a wav file
    :param
    wav_file_path:
    The wav file to extract the spectrum from
    nb_of_frames:
    The number of frames from which to extract data at a time
    nb_of_points:
    The number of points to calculate the Fast Fourier Transform
    :return
    The array of frequencies
    The array of corresponding intensities
    """

    # Extract all useful data from the wav file
    wav_file = wave.open(wav_file_path, 'r')
    sampling_rate = wav_file.getframerate()
    nb_of_channels = wav_file.getnchannels()
    total_nb_of_frames = wav_file.getnframes()
    data = []
    while wav_file.tell() < total_nb_of_frames - sample_size:
        d = wav_file.readframes(sample_size)
        d = struct.unpack('{n}h'.format(n=nb_of_channels * sample_size), d)
        d = np.array(d)
        data.append(d)
    wav_file.close()

    '''
    # Get the Hanning window
    w = np.hanning(nb_of_points)
    # Apply the window
    for d in data:
        for j in range(len(w)):
            d[j] = d[j] * w[j]
    '''

    # Calculate the Fourier Transform coefficients
    fft_data = []
    for d in data:
        fft_data.append(np.fft.fft(d, nb_of_points))
    # print(fft_data)

    # Calculate the power in each frequency
    intensity_data = []
    for f in fft_data:
        f_intensity = []
        for coef in f:
            f_intensity.append(abs(coef))
        intensity_data.append(f_intensity)
    # print(intensity_data)

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(fft_data[0]))
    # print(freqs)

    freqs_in_hertz = []
    for freq in freqs:
        freqs_in_hertz.append(abs(freq * sampling_rate))
    # print(freqs_in_hertz)
    for f in intensity_data:
        plt.plot(freqs_in_hertz, f)
        plt.ylim(0, 100000)
        #plt.xscale("log")
        #plt.yscale("symlog")
        plt.show()

    return freqs_in_hertz, intensity_data

complete_audio_spectrum("stressmono3.wav")