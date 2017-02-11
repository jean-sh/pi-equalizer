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
import os
import subprocess as sp
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
        print("usage: ./main.py <audio file path>")
    else:
        tmp_file_exists = False
        path, filename = os.path.split(args[1])
        filename, extension = os.path.splitext(filename)
        
        try: # Handle KeyboardInterrupt exception
            
            # Convert compressed formats to a temp wav file
            if extension != ".wav":
                FNULL = open(os.devnull, "w")
                pieq_tmp = os.path.expanduser("~") + "/.pieq_tmp/"
                wavpath = pieq_tmp + filename + ".wav"
                
                if not os.path.isfile(wavpath):
                    print("Decompressing...")
                    sp.call(["mkdir", "-p", pieq_tmp])
                    sp.call(["ffmpeg", "-i", args[1], wavpath], stdout=FNULL, stderr=sp.STDOUT)
                    tmp_file_exists = True
            else:
                wavpath = args[1]
            
        
            pool = mp.Pool(processes=3)
            q = mp.Queue(64)
            
            wf = wave.open(wavpath, 'rb')
            nb_channels = wf.getnchannels()
            frame_rate = wf.getframerate()

            # instantiate PyAudio
            pyau = pyaudio.PyAudio()

            # define callback
            def callback(in_data, frame_count, time_info, status):
                data = wf.readframes(frame_count)
                try:
                    q.put_nowait(data)
                except:
                    pass
                
                return data, pyaudio.paContinue


            # open stream using callback
            stream = pyau.open(format=pyau.get_format_from_width(wf.getsampwidth()),
                               channels=nb_channels,
                               rate=frame_rate,
                               output=True,
                               stream_callback=callback)
          
            
            # start the stream
            pool.apply_async(stream.start_stream)
            
            # Process the data and display it while the stream is running
            while stream.is_active():
                # This creates a delay so that audio and display are synchronized
                while q.qsize() < 30: 
                    time.sleep(0.05)
                    break
                data = q.get(0.1)

                magnitudes = pool.apply(auex.calculate_magnitudes, (data, 1024, nb_channels))
                pool.apply_async(auvi.display_64, (magnitudes,))

            
            # stop stream
            stream.stop_stream()
            stream.close()
            wf.close()
           
            # close PyAudio
            pyau.terminate()
            
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            q.close()
            pool.terminate()
            auvi.clear_display()
            # Delete temp wav file if necessary
            if tmp_file_exists:
                os.remove(wavpath)
                
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
