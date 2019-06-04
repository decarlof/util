#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

This script is to fix a data collection error in the 2017-06/Arun data sets.
All data (proj,dark and white) were stored in the proj hdf tag and the 
flat/dark/theta tages are invalid for all data sets from proj file index > 6
The script generates new hdf files with the corrected data exchange formatting
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
import json
import collections
import os
import dxfile.dxtomo as dx

def read_aps_2bm_custom(fname, sino=None):

    # Read APS 2-BM raw data in temporary array to fix an acquisition error. 
    # All data (proj,dark and white) are stored in the proj array while flat/dark/theta arrays are invalid
    tproj, tflat, tdark, ttheta = dxchange.read_aps_2bm(fname, sino=sino)

    # Extracting from the tproj array proj, flat, dark and theta
    ndark = 10
    nflat = 10
    last_projection = tproj.shape[0] - nflat - ndark
    proj = tproj[0:last_projection, :, :]
    flat = tproj[last_projection:last_projection+nflat, :, :]
    dark = tproj[last_projection+nflat:last_projection+nflat+ndark, :, :]
    theta_size = proj.shape[0]
    #theta = np.linspace(0. , np.pi, theta_size)
    theta = np.linspace(0. , 180.0, theta_size)
    
    return proj, flat, dark, theta


def save_dx(fname, proj, flat, dark, theta):

    sample_name = fname
    experiment_prosal = 'GUP-53902'
    experiment_title = 'Investigating the Phase and Kirkendall Pore Evolution in Ti-coated Ni Wires using X-Ray Tomographic Microscopy'
    experimenter_name = 'Ashley Paz y Puente'
    experimenter_role = 'PI'
    experimenter_affiliation = 'Northwestern University, University of Cincinnati'
    experimenter_phone = '847-467-5416'
    experimenter_email = 'ashleyewh2012@u.northwestern.edu'
    experimenter_facility_user_id = '233967'
  
    instrument_name = '2-BM micro-CT'
    instrument_comment = 'A Hutch'  

    attenuator_name = 'filter'
    attenuator_description = '1mm C, 4mm Glass, 1mm Si'

    monochromator_name = 'DMM'
    monochromator_description = '2.657mrad USArm; 1.349_monoY -9.999'

    detector_name = 'PCO.edge'
    detector_shutter_mode = 'rolling'
    detector_exposure_time = 0.020
    detector_description = 'sample to detector distance = 50 mm'
    objective_magnification = 10

    scintillator_name = 'LuAG' 
    scintillator_scintillating_thickness = 20
    sample_detector_distance = 0.050

    # Open DataExchange file
    f = dx.File(fname, mode='w') 

    # Write the Data Exchange HDF5 file.
    f.add_entry(dx.Entry.sample( name={'value':sample_name}))
    
    f.add_entry(dx.Entry.experiment( proposal={'value':experiment_prosal}))
    f.add_entry(dx.Entry.experiment( title={'value':experiment_title}))

    f.add_entry(dx.Entry.experimenter(name={'value':experimenter_name}))
    f.add_entry(dx.Entry.experimenter(role={'value':experimenter_role}))
    f.add_entry(dx.Entry.experimenter(affiliation={'value':experimenter_affiliation}))
    f.add_entry(dx.Entry.experimenter(phone={'value':experimenter_phone}))
    f.add_entry(dx.Entry.experimenter(email={'value':experimenter_email}))
    f.add_entry(dx.Entry.experimenter(facility_user_id={'value':experimenter_facility_user_id}))

    f.add_entry(dx.Entry.instrument(name={'value':instrument_name}))
    f.add_entry(dx.Entry.instrument(comment={'value':instrument_comment}))

    f.add_entry(dx.Entry.monochromator( name={'value':monochromator_name}))
    f.add_entry(dx.Entry.monochromator( description={'value':monochromator_description}))

    f.add_entry(dx.Entry.attenuator( name={'value':attenuator_name}))
    f.add_entry(dx.Entry.attenuator( description={'value':attenuator_description}))


    f.add_entry(dx.Entry.detector(name={'value':detector_name}))
    f.add_entry(dx.Entry.detector(description={'value':detector_description}))
    f.add_entry(dx.Entry.detector(exposure_time={'value':detector_exposure_time}))
    f.add_entry(dx.Entry.detector(shutter_mode={'value':detector_shutter_mode}))

    f.add_entry(dx.Entry.objective(magnification={'value':objective_magnification}))

    f.add_entry(dx.Entry.scintillator(name={'value':scintillator_name}))
    f.add_entry(dx.Entry.scintillator(scintillating_thickness={'value':scintillator_scintillating_thickness, 'units':'um'}))

    f.add_entry(dx.Entry.data(data={'value': proj, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))
    f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

    f.close()

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Dinc/all/'

    h5_file_list = filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top))
    
    for fname in h5_file_list:
        
        rfname = top + fname
        dxfname = top + "dx_" + fname

        proj, flat, dark, theta = read_aps_2bm_custom(rfname)
        save_dx(dxfname, proj, flat, dark, theta)
        print("done: ", rfname, dxfname)
