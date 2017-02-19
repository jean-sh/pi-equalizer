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
 
Install the API with `sudo apt install sense-hat`. Install the other modules with `pip`. To play files other than wav, `ffmpeg` is needed.


### Usage
`python path_to_folder/main.py audio_file`
