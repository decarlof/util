#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to align the HZG nano tomography projections.
"""

from __future__ import print_function
import tomopy
import dxchange
import alignment
import numpy as np

if __name__ == '__main__':
    # Set path to the micro-CT data to align.
    fname = '/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections_crop'
    
    # Set for scan_renamed_450projections
    proj_start = 0
    proj_end = 451
    flat_start = 0
    flat_end = 93
    dark_start = 0
    dark_end = 10
    
    # Set binning and number of iterations
    binning = 4
    iters = 7

    # Selec ranges
    ind_tomo = range(proj_start, proj_end)
    ind_flat = range(flat_start, flat_end)
    ind_dark = range(dark_start, dark_end)

    # Read the Anka tiff raw data.
    proj, flat, dark = dxchange.read_anka_topotomo(fname, ind_tomo, ind_flat, ind_dark)

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark)

    data = tomopy.minus_log(data)

    print(data.shape)
    data = tomopy.downsample(data, level=binning, axis=1)
    data = tomopy.downsample(data, level=binning, axis=2)
    print(data.shape)
    
    fdir = fname + '_aligned' + '/align_iter_' + str(iters)
    print(fdir)
    cprj, sx, sy, conv = alignment.align_seq(data, theta, fdir=fdir, iters=iters, pad=(10, 10), blur=True, save=True, debug=True)

    np.save(fdir + '/shift_x', sx)
    np.save(fdir + '/shift_y', sy)

    # Write aligned projections as stack of TIFs.
    dxchange.write_tiff_stack(cprj, fname=fdir + '/radios/image')

