#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct multiple data sets.
"""

from __future__ import print_function

import os
import sys
import json
import argparse
import numpy as np
import collections

import h5py
import tomopy
import dxchange
   
def get_dx_dims(fname, dataset):
    """
    Read array size of a specific group of Data Exchange file.
    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.
    Returns
    -------
    ndarray
        Data set size.
    """

    grp = '/'.join(['exchange', dataset])

    with h5py.File(fname, "r") as f:
        try:
            data = f[grp]
        except KeyError:
            return None

        shape = data.shape

    return shape

def read_rot_centers(fname):

    try:
        with open(fname) as json_file:
            json_string = json_file.read()
            dictionary = json.loads(json_string)

        return collections.OrderedDict(sorted(dictionary.items()))

    except Exception as error: 
        print("ERROR: the json file containing the rotation axis locations is missing")
        print("ERROR: run find_centers.py to create one first")
        return None
        
def rec_full(h5fname, nsino, rot_center):
    
    sample_detector_distance = 30       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 2.93e-4     # Detector pixel size in cm (1.17e-4)
    monochromator_energy = 25.74        # Energy of incident wave in keV
    alpha = 1e-02                       # Phase retrieval coeff.

    data_size = get_dx_dims(h5fname, 'data')
    print(data_size)
    print("FULL")
 
class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        return self.start <= other <= self.end   
    
def rec_slice(h5fname, nsino, rot_center):
    
    sample_detector_distance = 30       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 2.93e-4     # Detector pixel size in cm (1.17e-4)
    monochromator_energy = 25.74        # Energy of incident wave in keV
    alpha = 1e-02                       # Phase retrieval coeff.

    # Select sinogram range to reconstruct
    sino = None
        
    start = nsino
    end = start + 1
    sino = (start, end)

    # Read APS 32-BM raw data
    proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
        
    # Flat-field correction of raw data
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    data = tomopy.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

    # phase retrieval
    # data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)

    data = tomopy.minus_log(data)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    #fname = os.path.dirname(h5fname) + '/' + os.path.splitext(os.path.basename(h5fname))[0]+ '_slice_rec/' + 'recon'
    fname = os.path.dirname(h5fname) + '/' + 'slice_rec/' + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]
    dxchange.write_tiff_stack(rec, fname=fname)
    print("Rec: ", fname)
        
def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the hdf5 datasets are located: /data/")
    parser.add_argument("nsino", nargs='?', type=float, choices=[Range(0.0, 1.0)], default=0.5, help="location of the sinogram used by find center (0 top, 1 bottom): 0.6 (default 0.5)")
    parser.add_argument("type", nargs='?', type=str, default="slice", help="reconstruction type: full (default slice)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    top = args.top
    nsino = int(args.nsino)

    slice = False
    if args.type == "slice":
        slice = True
        
    # Load the the rotation axis positions.
    jfname = top + "rotation_axis.json"
    
    print (jfname)
    dictionary = read_rot_centers(jfname)
    print(dictionary)
    
    for key in dictionary:
        dict2 = dictionary[key]
        for h5name in dict2:
            rot_center = dict2[h5name]
            fname = top + h5name
            if slice:             
                rec_slice(fname, nsino, rot_center)
            else:
                rec_full(fname, nsino, rot_center)

if __name__ == "__main__":
    main(sys.argv[1:])

