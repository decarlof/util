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


def sobel_stack(ndata):
    nimages = ndata.shape[0]
    for index in range(nimages):
        ndata[index, :, :] = ski.filters.sobel(ndata[index, :, :])
    return ndata

def label(ndata, blur_radius=1.0, threshold=1):

    nimages = ndata.shape[0]
    for index in range(nimages):
        ndata[index, :, :] = ndi.gaussian_filter(ndata[index, :, :], blur_radius)
        ndata[index, :, :], nr_objects = scipy.ndimage.label(ndata[index, :, :] > threshold) 
        print ("Image %d contains %d particles" % (index, nr_objects))
        # print(np.amin(ndata[index, :, :]), np.amax(ndata[index, :, :]), np.mean(ndata[index, :, :]))
    return ndata, nr_objects

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the tiff images are located: /data/")
    parser.add_argument("start", nargs='?', const=1, type=int, default=1, help="index of the first image: 10001 (default 1)")

    args = parser.parse_args()

    top = args.top
    index_start = int(args.start)

    template = os.listdir(top)[1]

    nfile = len(fnmatch.filter(os.listdir(top), '*.tiff'))
    index_end = index_start + nfile
    index_end = 10
    ind_tomo = range(index_start, index_end)

    
    fname = top + template

    print (nfile, index_start, index_end, fname)
    # Read the tiff raw data.
    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)
    ndata = rdata

#    slider(ndata)

#    ndata = sobel_stack(rdata)
#    print(ndata[0, :, :])
#    slider(ndata)

#    blur_radius = 2
#    threshold = 0.0000001
#    ndata = label(rdata, blur_radius, threshold)
#    slider(ndata)

    idata = se.rescale_intensity(ndata[0, :, :], out_range=(0, 256))
    distance = ndi.distance_transform_edt(idata)
    local_maxi = sf.peak_local_max(distance, labels=idata, footprint=np.ones((3, 3)), indices=False)
    markers = ndi.label(local_maxi)[0]
    labels = seg.watershed(-distance, markers, mask=idata)
    slider(labels)


if __name__ == "__main__":
    main(sys.argv[1:])
