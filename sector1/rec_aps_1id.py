#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the APS 1-ID tomography data as original tiff.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
import sirtfilter

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/segment/sector1/microCT/'

    sname = 'g120f5'
    fname = top + sname + '/' + sname + '_'

    sample_detector_distance = 10      # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 1.2e-4     # Detector pixel size in cm
    monochromator_energy = 61.332    # Energy of incident wave in keV

    # Select the sinogram range to reconstruct.
    start = 600
    end = 900

    # Read the APS 1-ID raw data.
    proj, flat, dark = dxchange.read_aps_1id(fname, sino=(start, end))

    print(proj.shape, flat.shape, dark.shape)
    
    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0], ang1=0.0, ang2=360.0)

    # Flat-field correction of raw data.
    ndata = tomopy.normalize(proj, flat, dark)

    ndata = tomopy.remove_stripe_ti(ndata)
    ndata = tomopy.remove_stripe_sf(ndata)
    
    # phase retrieval
    # ndata = tomopy.prep.phase.retrieve_phase(ndata, pixel_size=detector_pixel_size_x, dist=sample_detector_distance, energy=monochromator_energy, alpha=8e-3, pad=True)

    # Find rotation center.
    #rot_center = tomopy.find_center(ndata, theta, init=1024, ind=0, tol=0.5)
    rot_center = 576

    binning = 0
    ndata = tomopy.downsample(ndata, level=int(binning))
    rot_center = rot_center/np.power(2, float(binning))    

    ndata = tomopy.minus_log(ndata)

    rec_method = None

    #rec_method = 'sirf-fbp'
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
        dxchange.write_tiff_stack(rec, fname=top + 'recon' + '/recon')

    elif rec_method == 'sirt':
        print("sirt")
        # Reconstruct object using sirt algorithm.
        rec = tomopy.recon(proj, theta, center=rot_center, algorithm='sirt', num_iter=50)
        # Mask each reconstructed slice with a circle.
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname=top + 'recon' + '/recon')

    else: #rec_method == 'gridrec':
        print("gridrec")
        # Reconstruct object using Gridrec algorithm.
        rec = tomopy.recon(ndata, theta, center=rot_center, algorithm='gridrec')
        # Mask each reconstructed slice with a circle.
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname=top + 'recon' + '/recon')


