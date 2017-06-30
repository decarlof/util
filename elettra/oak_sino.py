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
from skimage.measure import compare_ssim as ssim
import scipy.ndimage as ndi
import scipy
import tomopy.util.dtype as dtype
import tomopy.util.mproc as mproc

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

    fname = '/local/dataraid/elettra/Oak_16bit_slice343_all_repack.h5'
    
    # Read the hdf raw data.
    sino, sflat, sdark, th = dxchange.read_aps_32id(fname)

    proj = np.swapaxes(sino,0,1)
    flat = np.swapaxes(sflat,0,1)
    dark = np.swapaxes(sdark,0,1)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0], ang1=0.0, ang2=180.0)

    print(proj.shape, dark.shape, flat.shape, theta.shape)

    # Flat-field correction of raw data.
    ndata = tomopy.normalize(proj, flat, dark)
    #slider(ndata)
    # Find rotation center.
    #rot_center = tomopy.find_center(ndata, theta, init=1024, ind=0, tol=0.5)
    rot_center = 980

    binning = 1
    ndata = tomopy.downsample(ndata, level=int(binning))
    rot_center = rot_center/np.power(2, float(binning))    

    ndata = tomopy.minus_log(ndata)
    
    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(ndata, theta, center=rot_center, algorithm='gridrec')
    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/recon')

if __name__ == "__main__":
    main(sys.argv[1:])
