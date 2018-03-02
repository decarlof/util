#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Stu data sets.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Stu/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {102: {"0102": 1127.7}} 
    #wname='sym16'
    #wname='haar'
    wname='db5'
    sample_detector_distance = 60      # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 0.65e-4    # Detector pixel size in cm
    monochromator_energy = 24.9        # Energy of incident wave in keV

    for key in dictionary:
        dict2 = dictionary[key]
        for key2 in dict2:
            prefix = 'exp_'
            index = key2
            fname = top + prefix + index + '/proj_' + index + '.hdf'
            rot_center = dict2[key2]
            #print(fname, rot_center)

            # Select sinogram range to reconstruct.
            sino = None
            
            start = 300
            end = 401
            sino = (start, end)
            
            # Read APS 32-ID raw data.
            proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=sino)

            # Flat-field correction of raw data.
            data = tomopy.normalize(proj, flat, dark)

            for sigma in range (1,100):
                # remove stripes
                proj = tomopy.remove_stripe_fw(data,level=5,wname=wname,sigma=sigma,pad=True)
                #proj = tomopy.prep.stripe.remove_stripe_ti(proj,alpha=7)
                #proj = tomopy.prep.stripe.remove_stripe_sf(proj,size=51)

                # phase retrieval
                #data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=8e-3,pad=True)

                # Find rotation center
                #rot_center = tomopy.find_center(proj, theta, init=rot_center, ind=start, tol=0.5)
                print(index, rot_center)

                proj = tomopy.minus_log(proj)

                # Reconstruct object using Gridrec algorithm.
                rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

                # Mask each reconstructed slice with a circle.
                rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

                # Write data as stack of TIFs.
                ##fname = top +'full_rec/' + prefix + index + '/recon'
                fname = top +'rec_slice_' + wname +'/' + prefix + index + '_slice' + str(start) + '_recon_' + str(sigma)
                print("Rec: ", fname)
                dxchange.write_tiff_stack(rec, fname=fname)
