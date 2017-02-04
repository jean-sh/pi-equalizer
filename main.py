#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
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

import sys
import pyaudio
import wave
import numpy as np
import time
import multiprocessing as mp
import math
import audioVisualization as auvi
import audioExtraction as auex


def main(args):
    if len(args) != 2:
        print("usage: ./main.py <wav file path>")
    else:
        pool = mp.Pool(processes=2)
        
        wf = wave.open(args[1], 'rb')
        nb_channels = wf.getnchannels()
        frame_rate = wf.getframerate()

        # instantiate PyAudio
        pyau = pyaudio.PyAudio()

        # define callback
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            
            # Calculating magnitudes
            magnitudes = pool.apply(auex.calculate_magnitudes, (data, frame_count, nb_channels))
            
            # Displaying the eq
            auvi.display_64(magnitudes)

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

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
