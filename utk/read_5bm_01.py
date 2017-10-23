#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the APS 5-BM data as original xmt.
xmt are 16 bit unsigned integer tiff file that requires a byte swap before
being processed.
"""

from __future__ import print_function
import os
import sys
import argparse
import fnmatch
from os.path import expanduser
import tomopy
import dxchange
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
import matplotlib.widgets as wdg
import matplotlib.pyplot as plt

import skimage as ski
import skimage.segmentation as seg
import skimage.morphology as morth
import scipy.ndimage as ndi
import scipy
import cv2

class slider():
    def __init__(self, data):
        self.data = data

        ax = pl.subplot(111)
        pl.subplots_adjust(left=0.25, bottom=0.25)

        self.frame = 0
        self.l = pl.imshow(self.data[self.frame,:,:], cmap='gray') 

        axcolor = 'lightgoldenrodyellow'
        axframe = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
        self.sframe = wdg.Slider(axframe, 'Frame', 0, self.data.shape[0]-1, valfmt='%0.0f')
        self.sframe.on_changed(self.update)

        pl.show()

    def update(self, val):
        self.frame = int(np.around(self.sframe.val))
        self.l.set_data(self.data[self.frame,:,:])

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the tiff images are located: /data/")
    parser.add_argument("start", nargs='?', const=0, type=int, default=0, help="index of the first image: 10001 (default 0)")

    args = parser.parse_args()

    top = args.top

    # Select the sinogram range to reconstruct.
    start = 290
    end = 294

    print(top)
    # Read the Australian Synchrotron Facility data
    proj, flat, dark = dxchange.read_aps_5bm(top)
#    proj, flat, dark = dxchange.read_aps_5bm(fname, sino=(start, end))

    slider(proj)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    slider(proj)


if __name__ == "__main__":
    main(sys.argv[1:])
