#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the HZG nano tomography data as
original tiff.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    fname = '/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections/'

    sample_detector_distance = 18.8e2
    detector_pixel_size_x = 19.8e-7
    monochromator_energy = 11.0

    # for scan_renamed_450projections
    proj_start = 1
    proj_end = 450
    flat_start = 1
    flat_end = 93
    dark_start = 1
    dark_end = 10

    ind_tomo = range(proj_start, proj_end)
    ind_flat = range(flat_start, flat_end)
    ind_dark = range(dark_start, dark_end)

    # Select the sinogram range to reconstruct.
    start = 1000
    end = 1002

    # Read the Anka tiff raw data.
    proj, flat, dark = dxchange.read_anka_topotomo(fname, ind_tomo, ind_flat,
                                                 ind_dark, sino=(start, end))

    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0])

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark)

    proj = tomopy.minus_log(proj)

    # Find rotation center.
#    rot_center = tomopy.find_center(proj, theta, emission=False, init=1024,
#                                    ind=0, tol=0.5)
    
    rot_center = 1002
    print("Center of rotation: ", rot_center)

    data = tomopy.minus_log(data)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='/local/decarlo/data/hzg/nanotomography/recon_dir/recon')
