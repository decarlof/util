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
import dxchange
import numpy as np
import scipy.ndimage as ndi
import matplotlib.pyplot as plt


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

    fname = top + template

    # Read the tiff raw data.
    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)

    particle_bed_reference = particle_bed_location(rdata[0], plot=False)

    print("Particle bed location: ", particle_bed_reference)
    print("Laser on?: ", laser_on(rdata, particle_bed_reference))
    print("Shutter closed on image: ", shutter_off(rdata))
if __name__ == "__main__":
    main(sys.argv[1:])
