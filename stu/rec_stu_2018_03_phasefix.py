
from __future__ import print_function

import os
import sys
import tomopy
import dxchange
import dxfile.dxtomo as dx
import numpy as np

sample_detector_distance = 3        # Propagation distance of the wavefront in cm
detector_pixel_size_x = 1.17e-4     # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
monochromator_energy = 22.7         # Energy of incident wave in keV
alpha = 1e-02                       # Phase retrieval coeff.
zinger_level = 800                  # Zinger level for projections
zinger_level_w = 1000               # Zinger level for white

h5fname = '/local/dataraid/Stu/all_hdf_03/proj_0208.hdf'
fname = '/local/dataraid/Stu/all_hdf_03/proj_0208p.hdf'

# Read APS 32-BM raw data.
proj, flat, dark, theta = dxchange.read_aps_32id(h5fname)
    
# zinger_removal
proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

# Flat-field correction of raw data.
data = tomopy.normalize(proj, flat, dark, cutoff=0.8)

# remove stripes
data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)

#data = tomopy.remove_stripe_ti(data, alpha=1.5)
data = tomopy.remove_stripe_sf(data, size=150)

# phase retrieval
data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)



# Open DataExchange file
f = dx.File(fname, mode='w') 

# Write the Data Exchange HDF5 file.

f.add_entry(dx.Entry.data(data={'value': data, 'units':'counts'}))
f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))

theta = theta / np.pi * 180.0 
f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

