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
#    im = imageio.imread("/local/decarlo/conda/tomopy_decarlof/tomopy/data/lena.tif")
    im = imageio.imread("/local/decarlo/conda/util/elettra/img/SMALLTOMATO.jxr")
    print(imageio.help())
    imageio.imwrite("./test.jxr", im, flags=1)
    imageio.imwrite("./test.tiff", im)
    imageio.imwrite("./test.png", im)
    imageio.imwrite("./test100.jpeg", im, X=100)
    imageio.imwrite("./test50.jpeg", im, flag='JPEG_QUALITYBAD')


if __name__ == "__main__":
    main(sys.argv[1:])
