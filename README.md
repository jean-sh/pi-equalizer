# piEqualizer
An audio visualizer for the Raspberry Pi Sense Hat's LED display, written in Python.

Work in progress, not functional yet.

Done:
* function to update 1 column of LEDs at a time (the easiest part)

Currently working on:
* extracting the sound spectrum from one chunk of frames at a time
 * close to being done: the correct values are being extracted and plotting gives coherent results
 * need to select the right scale for frequencies and intensities
* making the spectrum into meaningful values (volume over 8 frequency ranges)

Later:
* feeding the values to the LEDs for displaying
* synchronizing the display with audio (since this is not in real-time for now)
* making the display eye-pleasing
