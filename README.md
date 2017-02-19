# piEqualizer
## An audio visualizer for the Raspberry Pi Sense Hat's LED display

piEqualizer plays a wav file while displaying the equalizer on the Sense Hat's LED display.

### Installing
You will need a Raspberry Pi (I only tested it on the Pi 3) and the Pi's [Sense Hat](https://www.raspberrypi.org/products/sense-hat/).

piEqualizer uses:
 * the Sense HAT API
 * `pyAudio` for playing wav files
 * `NumPy` for data structures and maths
 * `OpenCV` for its Fourier Transform algorithm, faster than NumPy
 
To install the dependencies with apt:
 * `sudo apt install sense-hat python-pyaudio python-numpy python-opencv ffmpeg`

### Usage
`python path_to_folder/main.py audio_file`
