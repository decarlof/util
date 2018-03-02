#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to reconstruct with gridrec the HZG nano tomography projections.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/DanielSnyder/'
    h5name = 'proj_12'
    h5ext = '.hdf'
    
    fname = top + h5name + h5ext 

    sample_detector_distance = 18.8e2
    detector_pixel_size_x = 19.8e-7
    monochromator_energy = 11.0

    # Set the [start, end] index of the blocked projections.
    miss_projs = [0, 2]


    # Select the sinogram range to reconstruct.
    start = 300
    end = 302

    # Read the Anka tiff raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=(start, end))

    # Remove the missing angles from data.
    proj = np.concatenate((proj[0:miss_projs[0], :, :], proj[miss_projs[1] + 1:-1, :, :]), axis=0)
    theta = np.concatenate((theta[0:miss_projs[0]], theta[miss_projs[1] + 1:-1]))

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark)

    #proj = tomopy.minus_log(proj)

    # Find rotation center.
    #rot_center = tomopy.find_center(proj, theta, emission=False, init=1024, ind=0, tol=0.5)
    
    rot_center = 1296
    print("Center of rotation: ", rot_center)

    data = tomopy.minus_log(data)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname= top + h5name +'/recon')
