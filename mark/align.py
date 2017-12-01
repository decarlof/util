#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python example of how to read am images.
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
import skimage.feature as sf
import skimage.exposure as se
from scipy import ndimage as ndi

import scipy.ndimage as ndi
import scipy
import alignment


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
    parser.add_argument("start", nargs='?', const=1, type=int, default=1, help="index of the first image: 1000 (default 1)")

    args = parser.parse_args()

    top = args.top
    index_start = int(args.start)

    template = os.listdir(top)[0]

    nfile = len(fnmatch.filter(os.listdir(top), '*.tif'))
    index_end = index_start + nfile
    ind_tomo = range(index_start, index_end)
    
    fname = top + template

    print (nfile, index_start, index_end, fname)


    # Select the sinogram range to reconstruct.
    start = 0
    end = 480
    sino=(start, end)

    # Read the tiff raw data.
    ndata = dxchange.read_tiff_stack(fname, ind=ind_tomo, slc=(sino, None))
 
    # Normalize to 1 using the air counts
    ndata = tomopy.normalize_bg(ndata, air=5)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(ndata.shape[0])

    ndata = tomopy.minus_log(ndata)

    # Set binning and number of iterations
    binning = 2
    iters = 21

    print("Original", ndata.shape)
    ndata = tomopy.downsample(ndata, level=binning, axis=1)
    ndata = tomopy.downsample(ndata, level=binning, axis=2)
    print("Processing:", ndata.shape)

    fdir = 'aligned' + '/noblur_iter_' + str(iters) + '_bin_' + str(binning) 

    print(fdir)
    cprj, sx, sy, conv = alignment.align_seq(ndata, theta, fdir=fdir, iters=iters, pad=(10, 10), blur=False, save=True, debug=True)

    np.save(fdir + '/shift_x', sx)
    np.save(fdir + '/shift_y', sy)

    # Write aligned projections as stack of TIFs.
    dxchange.write_tiff_stack(cprj, fname=fdir + '/radios/image')


if __name__ == "__main__":
    main(sys.argv[1:])
