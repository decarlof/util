#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to align the XRF tomography projections.
"""

from __future__ import print_function

import sys
import tomopy
import dxchange
import numpy as np
import argparse

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="hdf file name of a single dataset: /data/sample.h5")
    parser.add_argument("--iters", nargs='?', type=int, default=10, help="number of iteration for alignment (default 7)")

    args = parser.parse_args()
    fname = args.fname
    iters = args.iters
    
    # Read the XRF raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(fname)

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark)

    data = tomopy.minus_log(data)
    data = tomopy.remove_nan(data, val=0.0)
    data = tomopy.remove_neg(data, val=0.00)
    data[np.where(data == np.inf)] = 0.00
    
    fdir = fname + '_aligned' + '/align_iter_' + str(iters)
    print(fdir)
    cprj, sx, sy, conv = tomopy.align_seq(data, theta, fdir=fdir, iters=iters, pad=(4, 4), blur=True, save=True, debug=True)

    np.save(fdir + '/shift_x', sx)
    np.save(fdir + '/shift_y', sy)

    rot_center = (cprj.shape[2]) / 2.0
    print("Center of rotation: ", rot_center)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(cprj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    fname='./recon_dir/recon'
    dxchange.write_tiff_stack(rec, fname)

if __name__ == "__main__":
    main(sys.argv[1:])
