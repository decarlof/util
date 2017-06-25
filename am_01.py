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

import skimage as ski
import skimage.segmentation as seg
import skimage.morphology as morth
import scipy.ndimage as ndi

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

def particle_bed_location(image, plot=False):
    edge = np.sum(image, axis=1)
    x = np.arange(0, edge.shape[0], 1)
    y = ndi.gaussian_filter(edge/float(np.amax(edge)), 5)
    if plot:
        plt.plot(x, y)
        plt.show()
    return np.abs(y - 0.5).argmin()

def laser_on(rdata, particle_bed_ref, alpha=0.8):
    nimages = rdata.shape[0]
    status = np.empty(nimages)

    for index in range(nimages):
        ndata = rdata[index]
        edge = np.sum(ndata, axis=1)
        y = ndi.gaussian_filter(edge/float(np.amax(edge)), 5)
        particle_bed = np.abs(y - 0.5).argmin()

        if particle_bed_ref >= particle_bed :
            status[index] = False
        else:
            status[index] = True
            particle_bed_ref = particle_bed_ref * alpha
    return status

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the tiff images are located: /data/")
    parser.add_argument("start", nargs='?', const=1, type=int, default=1, help="index of the first image: 10001 (default 1)")

    args = parser.parse_args()

    top = args.top
    index_start = int(args.start)

    template = os.listdir(top)[1]

    nfile = len(fnmatch.filter(os.listdir(top), '*.tif'))
    index_end = index_start + nfile
    ind_tomo = range(index_start, index_end)

#    print("1:", ind_tomo)
    fname = top + template

    # Read the tiff raw data.
#    print("2: ", index_start, index_end, fname)
    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)
    particle_bed_reference = particle_bed_location(rdata[0], plot=False)
    print("Particle bed location: ", particle_bed_reference)

    cdata = rdata[:, 0:particle_bed_reference, :]

    # Set the [start, end] index of the blocked images, flat and dark.
    flat_range = [0, 1]
    data_range = [1, nfile-19]
    #data_range = [100, 120]
    dark_range = [nfile-19, nfile]

    flat = cdata[flat_range[0]:flat_range[1], :, :]
    proj = cdata[data_range[0]:data_range[1], :, :]
    dark = cdata[dark_range[0]:dark_range[1], :, :]

    ndata = tomopy.normalize(proj, flat, dark)
    ndata = tomopy.normalize_bg(ndata, air=ndata.shape[2]/2.5)

    # normalize between [0,1]
    ##ndata_max = np.amax(ndata)
    ##ndata_min = np.amin(ndata)
    ##ndata = (ndata - ndata_min) / (ndata_max - ndata_min)
 
    ndata_max = np.amax(ndata)
    ndata_min = np.amin(ndata)
    #print(ndata_min, ndata_max)
    nimages = ndata.shape[0]
    #print(np.amin(ndata[0, :, :]), np.amax(ndata[0, :, :]))
    for index in range(nimages):
        # normalize between [0,1]
        ndata_max = np.amax(ndata[index, :, :])
        ndata_min = np.amin(ndata[index, :, :])
        ndata[index, :, :] = (ndata[index, :, :] - ndata_min) / (ndata_max - ndata_min)
        print(np.amin(ndata[index, :, :]), np.amax(ndata[index, :, :]))
        ndata[index, :, :] = (ndata[index, :, :])
        #ndata[index, :, :] = chan_vese(ndata[index, :, :])
        #ndata[index, :, :] = seg.find_boundaries(ndata[index, :, :])
        #ndata[index, :, :] = ski.feature.canny(ndata[index, :, :])
        ###ndata[index, :, :] = ski.filters.sobel(ndata[index, :, :])
        ##ndata[index, :, :] = ski.img_as_float(ndata[index, :, :])
        #tr = ski.filters.threshold_mean(ndata[index, :, :])
        ##tr = ski.filters.threshold_li(ndata[index, :, :])
        ###imin = np.amin(ndata[index, :, :])
        ###imax = np.amax(ndata[index, :, :])
        ###print(imin, imax, (imax+imin)/2.0)
        ###ndata[index, :, :] = (ndata[index, :, :] > 0)
        ###radius = 15
        ###selem = morth.disk(radius)
        ###local_otsu = ski.filters.rank.otsu(ndata[index, :, :], selem)
        ###threshold_global_otsu = ski.filters.threshold_otsu(ndata[index, :, :])
        #ndata[index, :, :] = ski.filters.threshold_local(ndata[index, :, :], 7)
        #ndata[index, :, :] = ski.filters.rank.threshold(ndata[index, :, :], morth.square(3))
        #ndata[index, :, :]  = ndi.gaussian_filter(ndata[index, :, :] , 1)


    for index in range(nimages):
        #ndata[index, :, :] = (ndata[index, :, :])
        #radius = 15
        #selem = morth.disk(radius)
        #local_otsu = ski.filters.rank.otsu(ndata[index, :, :], selem)
        #threshold_global_otsu = ski.filters.threshold_otsu(ndata[index, :, :])
        ndata[index, :, :] = ski.filters.sobel(ndata[index, :, :])
    slider(ndata)

if __name__ == "__main__":
    main(sys.argv[1:])
