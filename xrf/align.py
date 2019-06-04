#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to align the XRF tomography projections.
"""

from __future__ import print_function

import os
import sys
import tomopy
import dxchange as dx
import numpy as np
import argparse
import shutil

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("dname", help="directory containing multiple datasets: /data/")
    parser.add_argument("--iters", nargs='?', type=int, default=10, help="number of iteration for alignment (default 7)")

    args = parser.parse_args()
    dname = args.dname
    iters = args.iters

    if os.path.isdir(dname):
        # Add a trailing slash if missing
        top = os.path.join(dname, '')
        print("DNAME:", dname)

    h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top)))    

    prj = np.zeros((61, 101, 151), dtype='float32')

    for m in range(len(h5_file_list)):
        print(h5_file_list[m])
        # Read the XRF raw data.
        # prj += dx.read_hdf5(os.path.join(top, h5_file_list[m]), dataset='/exchange/data').astype('float32').copy()
        # ang = dx.read_hdf5(os.path.join(top, h5_file_list[4]), dataset='/exchange/theta').astype('float32').copy()
        # ang *= np.pi / 180.
        proj, flat, dark, theta = dx.read_aps_32id(top+h5_file_list[m])
        prj += proj

    proj, flat, dark, theta = dx.read_aps_32id(top+h5_file_list[0])
    ang = theta

    # Clean folder.
    try:
        shutil.rmtree('tmp/iters')
    except:
        pass

    prj = tomopy.remove_nan(prj, val=0.0)
    prj = tomopy.remove_neg(prj, val=0.0)
    prj[np.where(prj == np.inf)] = 0.0
    
    print (prj.min(), prj.max())

    prj, sx, sy, conv = tomopy.align_joint(prj, ang, iters=100, pad=(0, 0),
                        blur=True, rin=0.8, rout=0.95, center=None,
                        algorithm='pml_hybrid',
                        upsample_factor=100,
                        save=True, debug=True)



    # rot_center = (cprj.shape[2]) / 2.0
    # print("Center of rotation: ", rot_center)

    # # Reconstruct object using Gridrec algorithm.
    # rec = tomopy.recon(cprj, theta, center=rot_center, algorithm='gridrec')

    # # Mask each reconstructed slice with a circle.
    # rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # # Write data as stack of TIFs.
    # fname='./recon_dir/recon'
    # dxchange.write_tiff_stack(rec, fname)

if __name__ == "__main__":
    main(sys.argv[1:])
