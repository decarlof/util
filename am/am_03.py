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

def shutter_off(image, alpha=0.7, plot=False):
    flat_sum = np.sum(image[0, :, :])
    nimages = image.shape[0]
    for index in range(nimages):
        image_sum = np.sum(image[index, :, :])
        if image_sum < alpha * flat_sum :
            return index
    return None

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

def scale_to_one(ndata):
    ndata_max = np.amax(ndata)
    ndata_min = np.amin(ndata)
    nimages = ndata.shape[0]
    for index in range(nimages):
        # normalize between [0,1]
        ndata_max = np.amax(ndata[index, :, :])
        ndata_min = np.amin(ndata[index, :, :])
        ndata[index, :, :] = (ndata[index, :, :] - ndata_min) / (ndata_max - ndata_min)
    return ndata

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

def sharpening(ndata):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    nimages = ndata.shape[0]
    for index in range(nimages):
        ndata[index, :, :] = cv2.filter2D(ndata[index, :, :], -1, kernel)
    return ndata
   
def circle_detection(ndata):
    nimages = ndata.shape[0]
    for index in range(nimages):
        ndata[index, :, :] = cv2.filter2D(ndata[index, :, :], -1, kernel)
    return ndata


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the tiff images are located: /data/")
    parser.add_argument("start", nargs='?', const=1, type=int, default=0, help="index of the first image: 100 (default 0)")

    args = parser.parse_args()

    top = args.top
    index_start = int(args.start)

    template = os.listdir(top)[1]

    nfile = len(fnmatch.filter(os.listdir(top), '*.tiff'))
    index_end = index_start + nfile
    ind_tomo = range(index_start, index_end)

    fname = top + template

    # Read the tiff raw data.
    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)

    # View the data
    slider(rdata)

    # Apply the sobel filter
    ndata = scale_to_one(rdata)
    ndata = sobel_stack(ndata)
    slider(ndata)

    blur_radius = 3.0
    threshold = .04
    nddata = label(ndata, blur_radius, threshold)
    slider(ndata)

    # http://www.scipy-lectures.org/packages/scikit-image/auto_examples/plot_labels.html

if __name__ == "__main__":
    main(sys.argv[1:])
