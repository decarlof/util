#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python example of how to read am images.
"""

from __future__ import print_function
import numpy as np
import imageio
import sys

  
def main(arg):

    #print(imageio.help('JPEG-XR-FI'))
    im = imageio.imread("/Users/decarlo/Downloads/Original/bike_orig.bmp")
    imageio.imsave("/Users/decarlo/Desktop/data/test.jxr", im)
    imageio.imsave("/Users/decarlo/Desktop/data/test.tiff", im)
    imageio.imsave("/Users/decarlo/Desktop/data/test.png", im)
    imageio.imsave("/Users/decarlo/Desktop/data/test100.jpeg", im, Xc=100)
    imageio.imsave("/Users/decarlo/Desktop/data/test50.jpeg", im, flag='JPEG_QUALITYBAD')


if __name__ == "__main__":
    main(sys.argv[1:])
