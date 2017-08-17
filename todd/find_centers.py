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
#import collections
import os

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Todd/'

    # Set the file name that will store the rotation axis positions.
    jfname = "todd.json"

    h5_file_list = filter(lambda x: x.endswith('.h5'), os.listdir(top))

    dic_centers = {}
    i=0
    for fname in h5_file_list:
        h5fname = top + fname
        
        # Select sinogram range to reconstruct.
        sino = None
        
        start = 500
        end = 501
        sino = (start, end)

        # Read APS 32-BM raw data.
        proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
        
        # Flat-field correction of raw data.
        data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

        # remove stripes
        data = tomopy.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

        # find rotation center
        rot_center = tomopy.find_center_vo(data)   
        case =  {fname : rot_center}
        print(case)
        dic_centers[i] = case
        i = i + 1

    print (dic_centers)

    
        
    json_dump = json.dumps(dic_centers)
    f = open(jfname,"w")
    f.write(json_dump)
    f.close()



