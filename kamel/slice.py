#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-08/Kamel data sets.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
   
if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/2017-08/Todd/'
    h5name = 'SNDK_10_10_000'
    ext = 'h5'
          
    sample_detector_distance = 30       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 2.93e-4    # Detector pixel size in cm (1.17e-4)
    monochromator_energy = 25.74        # Energy of incident wave in keV
    alpha = 1e-02                      # Phase retrieval coeff.
    zinger_level = 1000                # Zinger level for projections
    zinger_level_w = 1000              # Zinger level for white
    
    
    fname = top + h5name + '.' + ext

    # Select sinogram range to reconstruct.
    sino = None
    
    start = 500
    end = 501
    sino = (start, end)

    # Read APS 32-BM raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=sino)
    
    # zinger_removal
    proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
    flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    #data = tomopy.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)
    ##data = tomopy.prep.stripe.remove_stripe_ti(data,alpha=7)
    ##data = tomopy.prep.stripe.remove_stripe_sf(data,size=51)

    # phase retrieval
    ##data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)

    # Find rotation center
    # rot_center = 955
    rot_center = tomopy.find_center_vo(data)   
    print(h5name, rot_center)

    data = tomopy.minus_log(data, ind=0)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    ##fname = top +'full_rec/' + prefix + h5name + '/recon'

    fname = top + h5name + '_slice_rec/' + 'recon'
    print("Rec: ", fname)
    dxchange.write_tiff_stack(rec, fname=fname)
