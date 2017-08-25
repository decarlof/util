#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python example of how to read am images.
"""

from __future__ import print_function
import numpy as np
import imageio
import sys

# see http://programtalk.com/python-examples/imageio.imsave/
# for exmaples

def main(arg):

    #top = '/Users/decarlo/Desktop/util/elettra/img/'
    top = '/local/decarlo/conda/util/elettra/img/'
    print(imageio.help('JPEG-XR-FI'))
    # im = imageio.imread(top + "SMALLTOMATO.jxr")
    # imageio.imsave(top + "test.jxr", im)
    
    im = imageio.imread(top + "lena.tif")
    #imageio.imsave(top + "test_00.jxr", im)

    print(im.shape)
    imageio.imsave(top + "test_00.jxr", im, format='JXR')

    imageio.imsave(top + "test_01.tiff", im)
    imageio.imsave(top + "test_02.png", im)
    print(imageio.imsave(top + "test_03.jpeg", im, progressive=True, optimize=True, baseline=True))
    imageio.imsave(top + "test_04.jpeg", im, flag='JPEG_QUALITYBAD')

if __name__ == "__main__":
    main(sys.argv[1:])
