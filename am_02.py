#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python example of how to read am images.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
from matplotlib.widgets import Slider
from skimage import data, io, filters
from skimage import feature
from scipy.ndimage import gaussian_filter
import skimage.segmentation as seg
import skimage
from skimage.morphology import square
import scipy

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    top = '/Users/decarlo/Desktop/data/am/'
    template = '102_Ti_T046mm_U18G13_04mps_p70_D100um_100ps_longpath_S10156.tif'
    index_start = 10156
    index_end = 10162

    top = '/Users/decarlo/Desktop/data/Ti_126/'
    template = '126_Ti_T1mm_U18G13_0.3mps_p90_D100um_500ns_across_S10001.tif'
    index_start = 10001
    index_end = 10401

    ind_tomo = range(index_start, index_end)

    fname = top + template
    # Read the tiff raw data.
    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)

    print(rdata[0].shape)
    edge = np.sum(rdata[0], axis=1)
    x = np.arange(0, edge.shape[0], 1)
    y = edge

    print(x.shape)
    print(edge.shape)
    spl = scipy.interpolate.splrep(x,y,k=3) # no smoothing, 3rd order spline
    ddy = scipy.interpolate.splev(x,spl,der=2) # use those knots to get second derivative 

    print("1:", ddy.shape)
    print("2:", min(ddy))
    print("3:", np.argmin(ddy))
    print("4:", np.argmin(ddy[np.argmin(ddy - 0).argmin()]))
    print("5:", ddy[np.argmin(ddy - 0).argmin()])


