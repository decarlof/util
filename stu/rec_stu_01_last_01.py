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
    top = '/local/dataraid/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {101: {"0101": 1126.0}, 102: {"0102": 1127.7}, 103: {"0103": 1127.7}, 
                  104: {"0104": 1127.7}, 105: {"0105": 1127.7}, 106: {"0106": 1127.7}, 
                  107: {"0107": 1127.7}, 108: {"0108": 1127.7}, 109: {"0109": 1127.7}, 
                  110: {"0110": 1128.0}, 111: {"0111": 1127.7}} 

    sample_detector_distance = 60      # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 0.65e-4    # Detector pixel size in cm
    monochromator_energy = 24.9        # Energy of incident wave in keV

    for key in dictionary:
        dict2 = dictionary[key]
        for h5name in dict2:
            prefix = 'exp_'
            fname = top + prefix + h5name + '/proj_' + h5name + '.hdf'
            rot_center = dict2[h5name]
            #print(fname, rot_center)

            # Select sinogram range to reconstruct.
            sino = None
            
            ##start = 285
            ##end = 286
            ##sino = (start, end)
            
            # Read APS 32-ID raw data.
            proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=sino)

            # Flat-field correction of raw data.
            proj = tomopy.normalize(proj, flat, dark)

            # remove stripes
            proj = tomopy.remove_stripe_fw(proj,level=5,wname='sym16',sigma=1,pad=True)

            # phase retrieval
            #data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=8e-3,pad=True)

            # Find rotation center
            #rot_center = tomopy.find_center(proj, theta, init=rot_center, ind=start, tol=0.5)
            print(h5name, rot_center)

            proj = tomopy.minus_log(proj)

            # Reconstruct object using Gridrec algorithm.
            rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

            # Mask each reconstructed slice with a circle.
            rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

            # Write data as stack of TIFs.
            fname = top +'full_rec/' + prefix + h5name + '/recon'
            ##fname = top +'slice_rec/' + prefix + h5name + '_recon'
            print("Rec: ", fname)
            dxchange.write_tiff_stack(rec, fname=fname)
