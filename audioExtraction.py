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
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import struct

def audio_spectrum():
    wav_file = wave.open("stressmono.wav", 'r')
    data = wav_file.readframes(1000)
    wav_file.close()
    data = struct.unpack('{n}h'.format(n=1000), data)
    data = np.array(data)

    w = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(w))
    print(freqs.min(), freqs.max())

audio_spectrum()


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