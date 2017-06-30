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

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="full path to hdf file: /data/data.hdf")

    args = parser.parse_args()

    fname = args.fname

    # Read the hdf rec data.
    ##rec_elettra = dxchange.reader.read_hdf5(fname, 'reconstruction/slices')
    ##slider(rec_elettra)
    
    
    # Read the hdf raw data.
    sino, sflat, sdark, th = dxchange.read_aps_32id(fname)

    proj = np.swapaxes(sino,0,1)
    flat = np.swapaxes(sflat,0,1)
    dark = np.swapaxes(sdark,0,1)

#    slider(proj)
#    slider(flat)
#    slider(dark)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0], ang1=0.0, ang2=190.0)

    print(theta)
    print(proj.shape, dark.shape, flat.shape, theta.shape)


    flat = np.ones((flat.shape[0], flat.shape[1], flat.shape[2]))
    dark = np.zeros((dark.shape[0], dark.shape[1], dark.shape[2]))
    
    # Flat-field correction of raw data.
    ndata = tomopy.normalize(proj, flat, dark)
    ndata = ndata / np.amax(ndata)
    slider(ndata)
    # Find rotation center.
    #rot_center = tomopy.find_center(ndata, theta, init=1024, ind=0, tol=0.5)
    rot_center = 980

    binning = 1
    ndata = tomopy.downsample(ndata, level=int(binning))
    rot_center = rot_center/np.power(2, float(binning))    

    ndata = tomopy.minus_log(ndata)

    rec_method = None
    rec_method = 'gridrec'
    if rec_method == 'sirf-fbp':
        # Reconstruct object using sirt-fbp algorithm.
        # Use test_sirtfbp_iter = True to test which number of iterations is suitable for your dataset
        # Filters are saved in .mat files in "./¨
        test_sirtfbp_iter = True
        if test_sirtfbp_iter:
            nCol = ndata.shape[2]
            output_name = './test_iter/'
            num_iter = [50,100,150]
            filter_dict = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
            for its in num_iter:
                tomopy_filter = sirtfilter.convert_to_tomopy_filter(filter_dict[its], nCol)
                rec = tomopy.recon(ndata, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
                output_name_2 = output_name + 'sirt_fbp_%iiter_slice_' % its
                dxchange.write_tiff_stack(rec, fname=output_name_2, start=start, dtype='float32')

        # Reconstruct object using sirt-fbp algorithm:
        num_iter = 100
        nCol = ndata.shape[2]
        print("sirt-fbp")
        sirtfbp_filter = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
        tomopy_filter = sirtfilter.convert_to_tomopy_filter(sirtfbp_filter, nCol)
        rec = tomopy.recon(ndata, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
        # Mask each reconstructed slice with a circle.
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname='recon_dir/recon')

    elif rec_method == 'sirt':
        print("sirt")
        # Reconstruct object using sirt algorithm.
        rec = tomopy.recon(proj, theta, center=rot_center, algorithm='sirt', num_iter=50)
        # Mask each reconstructed slice with a circle.
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname='recon_dir/recon')

    elif rec_method == 'gridrec':
        print("gridrec")
        # Reconstruct object using Gridrec algorithm.
        rec = tomopy.recon(ndata, theta, center=rot_center, algorithm='gridrec')
        # Mask each reconstructed slice with a circle.
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname='recon_dir/recon')

    else: # None
        return

if __name__ == "__main__":
    main(sys.argv[1:])
