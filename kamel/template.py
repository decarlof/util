#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Arun data sets.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
import json
import collections

def read_aps_2bm_custom(fname, sino):

    # Read APS 2-BM raw data in temporary array to fix an acquisition error. 
    # All data (proj,dark and white) are stored in the proj array while flat/dark/theta arrays are invalid
    tproj, tflat, tdark, ttheta = dxchange.read_aps_2bm(fname, sino=sino)

    # Extracting from the tproj array proj, flat, dark and theta
    ndark = 10
    nflat = 10
    last_projection = tproj.shape[0] - nflat - ndark
    proj = tproj[0:last_projection, :, :]
    flat = tproj[last_projection:last_projection+nflat, :, :]
    dark = tproj[last_projection+nflat:last_projection+nflat+ndark, :, :]
    theta_size = proj.shape[0]
    theta = np.linspace(0. , np.pi, theta_size)
    
    return proj, flat, dark, theta

def read_rot_centers(fname):
    try:
        with open(fname) as json_file:
            json_string = json_file.read()
            dictionary = json.loads(json_string)

        return collections.OrderedDict(sorted(dictionary.items()))
    except Exception as error: 
        print("ERROR: the json file containing the rotation axis locations is missing")
        return None

    
if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Dinc/'

    # Set path to the file containing the rotation axis positions.
    jfname = "arun.json"

       
    sample_detector_distance = 5       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 0.65e-4    # Detector pixel size in cm
    monochromator_energy = 27.0        # Energy of incident wave in keV
    alpha = 1e-02                      # Phase retrieval coeff.
    zinger_level = 1000                # Zinger level for projections
    zinger_level_w = 1000              # Zinger level for white
    
    dictionary = read_rot_centers(jfname)
    
    for key in dictionary:
        dict2 = dictionary[key]
        for h5name in dict2:
            prefix = 'exp_'
            fname = top + prefix + h5name + '/proj_' + h5name + '.hdf'
            rot_center = dict2[h5name]
            ##print(fname, rot_center)

            # Select sinogram range to reconstruct.
            sino = None
            
            start = 1000
            end = 1001
            sino = (start, end)

            # Read APS 2-BM raw data.
            if (int(key) > 6):            
                proj, flat, dark, theta = read_aps_2bm_custom(fname, sino=sino)
            else:
                proj, flat, dark, theta = dxchange.read_aps_2bm(fname, sino=sino)
            
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
            #rot_center = tomopy.find_center(data, theta, init=rot_center, ind=start, tol=0.5)
            print(h5name, rot_center)

            data = tomopy.minus_log(data)

            # Reconstruct object using Gridrec algorithm.
            rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

            # Mask each reconstructed slice with a circle.
            rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

            # Write data as stack of TIFs.
            ##fname = top +'full_rec/' + prefix + h5name + '/recon'
            fname = top +'slice_rec/' + prefix + h5name + '_recon'
            print("Rec: ", fname)
            dxchange.write_tiff_stack(rec, fname=fname)
