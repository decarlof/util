#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct the APS 1-ID tomography data as original tiff.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    fname = '/local/dataraid/sector1/g120f5/g120f5_'

    sample_detector_distance = 60      # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 1.2e-4     # Detector pixel size in cm
    monochromator_energy = 50.0        # Energy of incident wave in keV

    # Select the sinogram range to reconstruct.
    start = 100
    end = 101

    # Read the APS 1-ID raw data.
    proj, flat, dark = dxchange.read_aps_1id(fname, sino=(start, end))

    print(proj.shape, flat.shape, dark.shape)
    
    # Set data collection angles as equally spaced between 0-180 degrees.
    theta = tomopy.angles(proj.shape[0], ang1=0.0, ang2=360.0)

    # Flat-field correction of raw data.
    proj = tomopy.normalize(proj, flat, dark)

    proj = tomopy.remove_stripe_ti(proj)
    proj = tomopy.remove_stripe_sf(proj)
    
    # phase retrieval
    proj = tomopy.prep.phase.retrieve_phase(proj, pixel_size=detector_pixel_size_x, dist=sample_detector_distance, energy=monochromator_energy, alpha=8e-3, pad=True)
    
    
    # Find rotation center.
    #rot_center = tomopy.find_center(proj, theta, init=1024, ind=0, tol=0.5)
    rot_center = 580
    print("Center of rotation: ", rot_center)

    proj = tomopy.minus_log(proj)

    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')
    ##rec = tomopy.recon(proj, theta, center=rot_center, algorithm='sirt', num_iter=50)
    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/recon')
