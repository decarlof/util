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

        if particle_bed <= particle_bed_ref :
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

def mse(x, y):
    return np.linalg.norm(x - y)

def main(arg):

    top = '/local/dataraid/elettra/rockoil/'
    img_ref = 'Rockoil_slice1021_original_noPhRet.tif'
    img_01 = 'Rockoil_slice1021_q50_noPhRet.tif'
    img_02 = 'Rockoil_slice1021_q100_noPhRet.tif'
    img_03 = 'Rockoil_slice1021_q150_noPhRet.tif'
    img_label = 'Rockoil'
    img_01_label = ' q50'
    img_02_label = ' q100'
    img_03_label = ' q150'
    
    # Read the tiff raw data.
    rdata_01 = dxchange.read_tiff(top + img_01)
    rdata_02 = dxchange.read_tiff(top + img_02)
    rdata_03 = dxchange.read_tiff(top + img_03)
    reference =  dxchange.read_tiff(top + img_ref)



    img = reference
    rows, cols = img.shape

    img_noise = rdata_01

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 4),
                             sharex=True, sharey=True,
                             subplot_kw={'adjustable': 'box-forced'})
    ax = axes.ravel()

    mse_none = mse(reference, reference)
    ssim_none = ssim(reference, reference, data_range=img.max() - img.min())

    mse_noise_01 = mse(reference, rdata_01)
    ssim_noise_01 = ssim(reference, rdata_01, data_range=rdata_01.max() - rdata_01.min())
    mse_noise_02 = mse(reference, rdata_02)
    ssim_noise_02 = ssim(reference, rdata_02, data_range=rdata_02.max() - rdata_02.min())
    mse_noise_03 = mse(reference, rdata_03)
    ssim_noise_03 = ssim(reference, rdata_03, data_range=rdata_03.max() - rdata_03.min())

    label = 'MSE: {:.2f}, SSIM: {:.2f}'
    ax[0].imshow(reference, cmap=plt.cm.gray)
    ax[0].set_xlabel(label.format(mse_none, ssim_none))
    ax[0].set_title('Original')

    ax[1].imshow(rdata_01, cmap=plt.cm.gray)
    ax[1].set_xlabel(label.format(mse_noise_01, ssim_noise_01))
    ax[1].set_title('Compressed'+ img_01_label)

    ax[2].imshow(rdata_02, cmap=plt.cm.gray)
    ax[2].set_xlabel(label.format(mse_noise_02, ssim_noise_02))
    ax[2].set_title('Compressed'+ img_02_label)

    ax[3].imshow(rdata_03, cmap=plt.cm.gray)
    ax[3].set_xlabel(label.format(mse_noise_03, ssim_noise_03))
    ax[3].set_title('Compressed'+ img_03_label)


    plt.suptitle(img_label)
    plt.tight_layout()
    plt.show()

#    slider(rdata)

def main_old(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the tiff images are located: /data/")
    parser.add_argument("start", nargs='?', const=1, type=int, default=1, help="index of the first image: 10001 (default 1)")

    args = parser.parse_args()

    top = args.top
    index_start = int(args.start)

    template = os.listdir(top)[1]

    files = fnmatch.filter(os.listdir(top), '*.tif')
    nfile = len(fnmatch.filter(os.listdir(top), '*.tif'))
    index_end = index_start + nfile - 1
    ind_tomo = range(index_start, index_end)

    fname = top + template

    # Read the tiff raw data.

    rdata = dxchange.read_tiff_stack(fname, ind=ind_tomo)
    reference =  dxchange.read_tiff(top + files[index_end-1])



    img = reference
    rows, cols = img.shape

    img_noise = rdata[0]

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                             sharex=True, sharey=True,
                             subplot_kw={'adjustable': 'box-forced'})
    ax = axes.ravel()

    mse_none = mse(img, img)
    ssim_none = ssim(img, img, data_range=img.max() - img.min())

    mse_noise = mse(img, img_noise)
    ssim_noise = ssim(img, img_noise,
                      data_range=img_noise.max() - img_noise.min())

    label = 'MSE: {:.2f}, SSIM: {:.2f}'

    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].set_xlabel(label.format(mse_none, ssim_none))
    ax[0].set_title('Original')

    ax[1].imshow(img_noise, cmap=plt.cm.gray)
    ax[1].set_xlabel(label.format(mse_noise, ssim_noise))
    ax[1].set_title('Compressed')

    plt.tight_layout()
    plt.show()

#    slider(rdata)

if __name__ == "__main__":
    main(sys.argv[1:])
