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

import time
from matrix import Matrix


matrix = Matrix()


def volume_to_pixels(v):
	px = int(v * 2.55)
	return [px, px, px]


def main(args):
	
	matrix.set_rotation(180)
	matrix.low_light = True
	i = 0
	while i < 8: 
		matrix.set_column(i, [(100, 0, 0), (100, 0, 0), (100, 0, 0), 
		(100, 0, 0), (100, 0, 0), (100, 0, 0), (100, 0, 0), (100, 0, 0)])
		time.sleep(1)
		i += 1
	
	time.sleep(2)
	matrix.clear(volume_to_pixels(10))
	time.sleep(1)
	matrix.clear(volume_to_pixels(0))
	
	
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
