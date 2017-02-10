# piEqualizer
## An audio visualizer for the Raspberry Pi Sense Hat's LED display

piEqualizer plays a wav file while displaying the equalizer on the Sense Hat's LED display.

### Installing
You will need a Raspberry Pi (I only tested it on the Pi 3) and the Pi's [Sense Hat](https://www.raspberrypi.org/products/sense-hat/).

piEqualizer uses NumPy, OpenCV and pyAudio which you can install with `pip`.

### Usage
`python main.py song.wav`

### To do
* better stability (sometimes crashes at the beginning of a song)
* improve visualization
* automatic conversion with ffmpeg to accept mp3, ogg, m4a, etc.
* selecting between different visualization modes with the Sense Hat's joystick
* switching to Python 3 would be nice (it is complicated to install OpenCV on it unfortunately)
