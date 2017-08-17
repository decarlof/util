#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Arun data sets.
"""

from __future__ import print_function

import os
import sys
import json
import argparse
import numpy as np

import tomopy
import dxchange

def find_rotation_axis(h5fname, nsino):
    
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

    # find rotation center
    rot_center = tomopy.find_center_vo(data)   

    return rot_center


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("top", help="top directory where the hdf5 datasets are located: /data/")
    parser.add_argument("nsino", nargs='?', const=1, type=int, default=1, help="index of the sinogram to use for finding center: 1024 (default 1)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    top = args.top
    nsino = int(args.nsino)

    # Set the file name that will store the rotation axis positions.
    jfname = top + "rotation_axis.json"

    h5_file_list = filter(lambda x: x.endswith('.h5'), os.listdir(top))

    dic_centers = {}
    i=0
    for fname in h5_file_list:
        h5fname = top + fname
        rot_center = find_rotation_axis(h5fname, nsino)
        case =  {fname : rot_center}
        print(case)
        dic_centers[i] = case
        i += 1

    json_dump = json.dumps(dic_centers)
    f = open(jfname,"w")
    f.write(json_dump)
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])

