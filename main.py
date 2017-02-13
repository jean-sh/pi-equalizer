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
import time
import multiprocessing as mp
import audioVisualization as auVi
import audioExtraction as auEx
from sense_hat import SenseHat


def main(args):
    if len(args) != 2:
        print("usage: ./main.py <audio file path>")
    else:
        wav_path = args[1]
        path, filename = os.path.split(wav_path)
        filename, extension = os.path.splitext(filename)
        tmp_file_created = False

        joystick = SenseHat()

        pool = mp.Pool(processes=3)
        q = mp.Queue(64)

        try:  # Handle KeyboardInterrupt exception
            
            # Convert compressed formats to a temp wav file
            if extension != ".wav":
                fnull = open(os.devnull, "w")
                pieq_tmp = os.path.expanduser("~") + "/.pieq_tmp/"
                wav_path = pieq_tmp + filename + ".wav"
                
                if not os.path.isfile(wav_path):
                    print("Decompressing...")
                    sp.call(["mkdir", "-p", pieq_tmp])
                    sp.call(["ffmpeg", "-i", args[1], wav_path], stdout=fnull, stderr=sp.STDOUT)
                tmp_file_created = True

            wf = wave.open(wav_path, 'rb')
            nb_channels = wf.getnchannels()
            frame_rate = wf.getframerate()

            # instantiate PyAudio
            pyau = pyaudio.PyAudio()

            # define callback
            def callback(in_data, frame_count, time_info, status):
                data = wf.readframes(frame_count)
                q.put_nowait(data)
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
            nb_of_modes = 6
            mode = 0
            while stream.is_active():
                # This creates a delay so that audio and display are synchronized
                while q.qsize() < 30: 
                    time.sleep(0.05)
                    break
                q_data = q.get(0.1)
                    
                # Calculate and display
                magnitudes = pool.apply(auEx.calculate_magnitudes, (q_data, 1024, nb_channels))
                pool.apply_async(auVi.display_eq, (magnitudes, mode))
                
                # Watch for joystick events and change mode accordingly
                event = joystick.stick.get_events()
                if event != []:
                    if event[0].direction == "right" and event[0].action == "released":
                        mode += 1
                    elif event[0].direction == "left" and event[0].action == "released":
                        mode -= 1
                    elif (event[0].direction == "up" or event[0].direction == "down") \
                    and event[0].action == "released":
                        mode = 0
                    mode %= nb_of_modes

            # stop stream
            stream.stop_stream()
            stream.close()
            wf.close()
           
            # close PyAudio
            pyau.terminate()
            
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            # Delete temp wav file if necessary
            if tmp_file_created:
                os.remove(wav_path)
            auVi.clear_display()
            q.close()
            pool.terminate()         
                
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
