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
        
def rec_full(h5fname, rot_center):
    
    sample_detector_distance = 30       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 2.93e-4     # Detector pixel size in cm (1.17e-4)
    monochromator_energy = 25.74        # Energy of incident wave in keV
    alpha = 1e-02                       # Phase retrieval coeff.

    data_size = get_dx_dims(h5fname, 'data')
    print(int(data_size[1]))

    # Select sinogram range to reconstruct.
    sino_start = 0
    sino_end = data_size[1]

    chunks = 16         # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction

    nSino_per_chunk = (sino_end - sino_start)/chunks
    print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            
    strt = 0

    for iChunk in range(0,chunks):
        print('\n  -- chunk # %i' % (iChunk+1))
        sino_chunk_start = sino_start + nSino_per_chunk*iChunk 
        sino_chunk_end = sino_start + nSino_per_chunk*(iChunk+1)
        print('\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                
        if sino_chunk_end > sino_end: 
            break

        sino = (int(sino_chunk_start), int(sino_chunk_end))
        # Read APS 32-BM raw data.
        proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
        
        # zinger_removal
        #proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
        #flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

        # Flat-field correction of raw data.
        data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

        # remove stripes
        data = tomopy.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

        # phase retrieval
        data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)

        print(h5name, rot_center)
        data = tomopy.minus_log(data)

        # Reconstruct object using Gridrec algorithm.
        rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

        # Mask each reconstructed slice with a circle.
        rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

        # Write data as stack of TIFs.
        fname = os.path.dirname(h5fname) + '/' + os.path.splitext(os.path.basename(h5fname))[0]+ '_full_rec/' + 'recon'
        print("Rec: ", fname)
        dxchange.write_tiff_stack(rec, fname=fname, start=strt)
        strt += data.shape[1]
     
def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x
    
def rec_slice(h5fname, nsino, rot_center):
    
    sample_detector_distance = 30       # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 2.93e-4     # Detector pixel size in cm (1.17e-4)
    monochromator_energy = 25.74        # Energy of incident wave in keV
    alpha = 1e-02                       # Phase retrieval coeff.

    data_size = get_dx_dims(h5fname, 'data')
    ssino = int(data_size[1] * nsino)

    # Select sinogram range to reconstruct
    sino = None
        
    start = ssino
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

    fname = os.path.dirname(h5fname) + '/' + 'slice_rec/' + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]
    dxchange.write_tiff_stack(rec, fname=fname)
    print("Rec: ", fname)
        
def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the hdf5 datasets are located: /data/")
    parser.add_argument("nsino", nargs='?', type=restricted_float, default=0.5, help="location of the sinogram used by find center (0 top, 1 bottom): 0.6 (default 0.5)")
    parser.add_argument("type", nargs='?', type=str, default="slice", help="reconstruction type: full (default slice)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    top = args.top
    nsino = float(args.nsino)

    slice = False
    if args.type == "slice":
        slice = True
        
    # Load the the rotation axis positions.
    jfname = top + "rotation_axis.json"
    
    dictionary = read_rot_centers(jfname)
    
    for key in dictionary:
        dict2 = dictionary[key]
        for h5name in dict2:
            rot_center = dict2[h5name]
            fname = top + h5name
            if slice:             
                rec_slice(fname, nsino, rot_center)
            else:
                rec_full(fname, rot_center)

if __name__ == "__main__":
    main(sys.argv[1:])

