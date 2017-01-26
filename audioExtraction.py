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
import scipy as sp
import wave
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import struct

def audio_spectrum(wav_file_path, nb_of_frames=16384, nb_of_points=256):
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
    wav_file.readframes(nb_of_frames)
    data = wav_file.readframes(nb_of_frames)
    sampling_rate = wav_file.getframerate()
    nb_of_channels = wav_file.getnchannels()
    wav_file.close()

    data = struct.unpack('{n}h'.format(n=nb_of_channels * nb_of_frames), data)
    data = np.array(data)

    # Calculate the Fourier Transform coefficients
    fft_array = np.fft.fft(data, nb_of_points)

    # Calculate the power in each frequency
    intensities = []
    for coef in fft_array:
        intensities.append(abs(coef))

    # Calculate the frequencies associated
    freqs = np.fft.fftfreq(len(fft_array))
    freqs_in_hertz = []
    for freq in freqs:
        freqs_in_hertz.append(abs(freq * sampling_rate))

    plt.loglog(freqs_in_hertz, intensities, basex=2, basey=10)
    #plt.xscale("log")
    #plt.yscale("log")
    plt.show()

    return freqs_in_hertz, intensities


audio_spectrum("stressmono3.wav", 32768, 1024)


def audio_to_ndarray(wavfile):
    """
    :param wavfile: the wav audio file to extract the MFCCs (Mel Frequency Cepstral Coefficients) from, must be mono
    :return: a 2-dimensional numpy array, 13 columns and as many lines as frames
    """
    [Fs, x] = audioBasicIO.readAudioFile(wavfile)
    features = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.050*Fs, 0.025*Fs)

    return features[8:20]


def extract_chroma_one_frame(frame):
    """
    Plots values from one frame as extracted by featureExtractionFile from pyAudioAnalysis
    """
    with open(frame, 'r') as f_frame:
        features = f_frame.read()

    values_str = features.split("\t")
    list_values = []
    for s in values_str:
        list_values.append(float(s))

    return list_values

# extract_and_plot_one_frame('features')


def extract_chroma_vector(data_file):
    """
    Extracts the chroma infos of an audio file over time
    :param data_file: file containing chroma infos extracted by featureExtractionFile from pyAudioAnalysis,
    the corresponding columns from the generated file are 22-33
    :return numpy array consisting of all frames, each consisting of 12 values representing their spectral energy
    """

    with open(data_file) as f:
        data = f.read()

    str_all_frames = data.split("\n")
    str_frame_list = []
    for str_frame in str_all_frames:
        str_frame_list.append(str_frame.split("\t"))

    float_frame_list = []
    float_frame_values = []
    for str_frame in str_frame_list:
        for str_value in str_frame:
            try:
                float_frame_values.append(float(str_value))
            except ValueError:
                print(str_value)
        float_frame_list.append(float_frame_values)
        float_frame_values = []

    np_array_frames = np.array(float_frame_list)
    return np_array_frames


# extract_chroma_vector("song_features")


def plot_chroma_one_frame(chroma_values):
    x = range(len(chroma_values))
    plt.bar(x, chroma_values)
    plt.show()


# plot_chroma_one_frame(extract_chroma_one_frame("features"))