#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the HZG nano tomography data as
original tiff.
"""

from __future__ import print_function
import tomopy
import dxchange
import alignment

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    fname = '/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections_crop/'

    sample_detector_distance = 18.8e2
    detector_pixel_size_x = 19.8e-7
    monochromator_energy = 11.0

    # for scan_renamed_450projections
    proj_start = 0
    proj_end = 451
    flat_start = 0
    flat_end = 93
    dark_start = 0
    dark_end = 10

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

    # Write aligned projections as stack of TIFs.
    dxchange.write_tiff_stack(data, fname='/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections_crop_rotate/radios_org/image')

