#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct p05 microCT data
"""

from __future__ import print_function

import tomopy
import dxchange
import p05tools as p05
import sirtfilter

# p05tools:
# git clone https://github.com/decarlof/p05tools.git
# cd p05tools
# python setup.py install

# sirtfilter:
# conda install -c http://dmpelt.gitlab.io/sirtfilter/ sirtfilter# conda install -c astra-toolbox astra-toolbox
if __name__ == '__main__':

    sample_name = 'INF_T1_200mPsBr_005a_s01a'
            
    sample_detector_distance = 60
    detector_pixel_size_x = 0.65e-4
    monochromator_energy = 27.4
       
    # Set path to the micro-CT data to reconstruct.
    raw_dir = '/replace_this_with_data_dir_path/' + sample_name + '/' 
    fname =  raw_dir + sample_name + 'scan.log'

    scanlog_content = p05.file.parse_scanlog(fname)
    print(scanlog_content)
    
    # Read raw data.
    prj, flat, dark, theta = p05.reco.get_rawdata(scanlog_content, raw_dir, verbose=True)

    print(prj.shape, flat.shape, dark.shape, theta.shape)
    
    # Select the sinogram range to reconstruct.
    start = 1024
    end = 1024
    prj = prj[:, [start,end], :]
    flat = flat[:, [start,end], :]
    dark = dark[:, [start,end], :]   

    # Flat-field correction of raw data.
    data = tomopy.normalize(prj, flat, dark)

    # remove stripes    
    data = tomopy.prep.stripe.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

#    # phase retrieval
    #data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=8e-3,pad=True)

    # Set rotation center.
    rot_center = 1552
    print(rot_center)
    
    data = tomopy.minus_log(data)

    # Use test_sirtfbp_iter = True to test which number of iterations is suitable for your dataset
    # Filters are saved in .mat files in "./¨
    test_sirtfbp_iter = True
    if test_sirtfbp_iter:
        nCol = data.shape[2]
        output_name = './test_iter/'
        num_iter = [50,100,150]
        filter_dict = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
        for its in num_iter:
            tomopy_filter = sirtfilter.convert_to_tomopy_filter(filter_dict[its], nCol)
            rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
            output_name_2 = output_name + 'sirt_fbp_%iiter_slice_' % its
            dxchange.write_tiff_stack(data, fname=output_name_2, start=start, dtype='float32')

    # Reconstruct object using sirt-fbp algorithm:
    num_iter = 100
    nCol = data.shape[2]
    sirtfbp_filter = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
    tomopy_filter = sirtfilter.convert_to_tomopy_filter(sirtfbp_filter, nCol)
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)

    # Reconstruct object using Gridrec algorithm.
#    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', nchunk=1)
    
    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    fname='/replace_this_with_data_dir_path/sirtfbp_recon'
    dxchange.write_tiff_stack(rec, fname=fname)

