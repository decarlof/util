#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find rotation axis location for all datasets in a folder.
"""

from __future__ import print_function

import os
import sys
import json
import argparse
import numpy as np

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


def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x
    

def find_rotation_axis(h5fname, nsino):
    
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

    # find rotation center
    rot_center = tomopy.find_center_vo(data)   

    return rot_center


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("nsino", nargs='?', type=restricted_float, default=0.5, help="location of the sinogram used by find center (0 top, 1 bottom): 0.5 (default 0.5)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    fname = args.fname
    nsino = float(args.nsino)

    if os.path.isfile(fname):       
        rot_center = find_rotation_axis(fname, nsino)
        print(fname, rot_center)
        
    elif os.path.isdir(fname):
        # Add a trailing slash if missing
        top = os.path.join(fname, '')
    
        # Set the file name that will store the rotation axis positions.
        jfname = top + "rotation_axis.json"

        h5_file_list = filter(lambda x: x.endswith('.h5'), os.listdir(top))

        print("Found: ", h5_file_list)
        print("Determining the rotation axis location ...")
        
        dic_centers = {}
        i=0
        for fname in h5_file_list:
            h5fname = top + fname
            rot_center = find_rotation_axis(h5fname, nsino)
            case =  {fname : rot_center}
            print(case)
            dic_centers[i] = case
            i += 1

        # Save json file containing the rotation axis
        json_dump = json.dumps(dic_centers)
        f = open(jfname,"w")
        f.write(json_dump)
        f.close()
        print("Rotation axis locations save in: ", jfname)
    
    else:
        print("Directory or File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])

