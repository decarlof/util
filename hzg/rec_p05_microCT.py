#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct p05 microCT data
"""

from __future__ import print_function

import tomopy
import dxchange
import p05tools as p05

#for p05tools:
# git clone https://github.com/decarlof/p05tools.git
# cd p05tools
# python setup.py install

if __name__ == '__main__':


    sample_name = 'INF_T1_200mPsBr_005a_s01a'
            
    sample_detector_distance = 60
    detector_pixel_size_x = 0.65e-4
    monochromator_energy = 27.4

#    sample_detector_distance = 49.998800
#    detector_pixel_size_x = 1.3094170e-4
#    monochromator_energy = 24.998484
       
    # Set path to the micro-CT data to reconstruct.
    raw_dir = '/local/decarlo/data/hzg/microtomography/fabian_wilde/' + sample_name + '/' 
    fname =  raw_dir + sample_name + 'scan.log'

    scanlog_content = p05.file.parse_scanlog(fname)
    print(scanlog_content)
    
    # Read raw data.
    proj, flat, dark, theta = p05.reco.get_rawdata(scanlog_content, raw_dir, verbose=True)

    print(proj.shape, flat.shape, dark.shape, theta.shape)
    
    # Select the sinogram range to reconstruct.
    start = 1024
    end = 1025
    proj = proj[:, [start,end], :]
    flat = flat[:, [start,end], :]
    dark = dark[:, [start,end], :]   

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark)

    # remove stripes    
    data = tomopy.prep.stripe.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

#    # phase retrieval
    #data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=8e-3,pad=True)

    # Set rotation center.
    rot_center = 1552
    print(rot_center)
    
    data = tomopy.minus_log(data)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name = 'parzen', nchunk=1)

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    fname='/local/decarlo/data/hzg/microtomography/fabian_wilde/recon_dir/recon'
    dxchange.write_tiff_stack(rec, fname=fname)

