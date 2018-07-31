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
import dxchange.reader as dxreader


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

    ##grp = '/'.join(['exchange', dataset])
    grp = dataset

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
    
    data_size = get_dx_dims(h5fname, 'Prefiltered_images')
    ssino = int(data_size[1] * nsino)

    # Select sinogram range to reconstruct
    sino = None
        
    start = ssino
    end = start + 1
    sino = (start, end)

    # Read APS 32-BM raw data
    ##proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
        
    # Flat-field correction of raw data
    ##data = tomopy.normalize(proj, flat, dark, cutoff=1.4)
    data, theta = read_aps_7bm(h5fname, sino=sino)

    # remove stripes
    #data = tomopy.remove_stripe_fw(ndata,level=5,wname='sym16',sigma=1,pad=True)

    # find rotation center
    rot_center = tomopy.find_center_vo(data)   

    return rot_center

def read_aps_7bm(fname, proj=None, sino=None):
    """
    Read APS 7-BM standard data format.

    Parameters
    ----------
    fname : str
        Path to hdf5 file.

    proj : {sequence, int}, optional
        Specify projections to read. (start, end, step)

    sino : {sequence, int}, optional
        Specify sinograms to read. (start, end, step)

    Returns
    -------
    ndarray
        3D tomographic data.

    array
        Projection angles in radian.
    """
    # tomo_grp = '/'.join(['exchange', 'data'])
    # theta_grp = '/'.join(['exchange', 'theta'])
    tomo_grp = 'Prefiltered_images'
    theta_grp = '/'.join(['exchange', 'theta'])
    tomo = dxreader.read_hdf5(fname, tomo_grp, slc=(proj, sino))
    theta = dxreader.read_hdf5(fname, theta_grp, slc=(proj, ))
 
    if (theta is None):
        ##theta_size = dxreader.read_dx_dims(fname, 'data')[0]
        theta_size = get_dx_dims(fname, 'Prefiltered_images')[0]
        #logger.warn('Generating "%s" [0-180] deg angles for missing "exchange/theta" dataset' % (str(theta_size)))
        print('Generating "%s" [0-180] deg angles for missing "exchange/theta" dataset' % (str(theta_size)))
        theta = np.linspace(0. , np.pi, theta_size)
    else:
        theta = theta * np.pi / 180.

    return tomo, theta

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
        print(os.listdir(top))
        
        h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top)))

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

