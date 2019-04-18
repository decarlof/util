
"""
Module for importing MIC HDF data files.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


import os
import sys
import numpy as np
import argparse
import dxchange
from pylab import *
import dxfile.dxtomo as dx

__author__ = "Francesco De Carlo"
__copyright__ = "Copyright (c) 2018, UChicago Argonne, LLC."
__version__ = "0.0.1"
__docformat__ = 'restructuredtext en'
__all__ = ['read_projection',
           'read_elements',
           'find_index']


def find_index(a_list, element):
    try:
        return a_list.index(element)
    except ValueError:
        return None

def read_elements(h5fname):
    b_elements = dxchange.read_hdf5(h5fname, "MAPS/channel_names")
    elements = []

    for i, e in enumerate(b_elements):
        elements.append(e.decode('utf-8'))
    return(elements)

def read_projection(fname, element, theta_index):
    """
    Reads a projection for a given element from an hdf file.

    Parameters
    ----------
    fname : str
        String defining the file name
    element : 
        String defining the element to select
    theta_index :
        index where theta is saved under in the hdf MAPS/extra_pvs_as_csv tag.
        For unknown reason 2-ID-E and the Bio Nano proble save this information 
        in different index location (663 and 657)

    Returns
    -------
    float
        projection angle
    ndarray
        projection
    """

    projections = dxchange.read_hdf5(fname, "MAPS/XRF_roi")
    theta = float(dxchange.read_hdf5(fname, "MAPS/extra_pvs_as_csv")[theta_index].split(b',')[1])
    elements = read_elements(fname)

    try:
        if find_index(elements, element) != None:
            return projections[find_index(elements, element),:, :], theta
        else:
            raise TypeError
    except TypeError:
        print("**** ERROR: Element %s does exist in the file: %s " % (element, fname))
        return None

def write_dxfile(fname, proj, theta, element):
    experimenter_affiliation="Argonne National Laboratory" 
    instrument_name="2-ID-E XRF"  
    sample_name = "test data set"

    flat = ones([1, proj.shape[1], proj.shape[2]]) * np.nanmax(proj)
    dark = zeros([1, proj.shape[1], proj.shape[2]])

    # Open DataExchange file
    f = dx.File(fname, mode='w')
     
    # Write the Data Exchange HDF5 file.
    f.add_entry(dx.Entry.experimenter(affiliation={'value': experimenter_affiliation}))
    f.add_entry(dx.Entry.instrument(name={'value': instrument_name}))
    f.add_entry(dx.Entry.sample(name={'value': sample_name}))

    f.add_entry(dx.Entry.data(data={'value': proj, 'element': element, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))
    f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

    f.close()


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("--element", nargs='?', type=str, default="Ca", help="element selection (default Si)")
    parser.add_argument("--output_fname", nargs='?', type=str, default="./data", help="output file path and prefix (default ./tmp/data)")
    parser.add_argument("--output_fformat", nargs='?', type=str, default="hdf", help="output file format: hdf or tiff (default hdf)")
    parser.add_argument("--theta_index", nargs='?', type=int, default=657, help="theta_index: 2-ID-E: 663; 2-ID-E prior 2017: 657; BNP 8; (default 657)")

    args = parser.parse_args()

    fname = args.fname
    element = args.element
    out = args.output_fname
    fformat = args.output_fformat
    theta_index = args.theta_index

    if os.path.isfile(fname):    

        proj, theta = read_projection(fname, element, theta_index)
        print ("theta:", theta)
        print ("projection shape", proj.shape)

    elif os.path.isdir(fname):
        # Add a trailing slash if missing
        top = os.path.join(fname, '')

        h5_file_list = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(top)))

        # elements = read_elements(top+h5_file_list[0])
        # print ("Elements in the files: ", elements)

        proj, theta = read_projection(top+h5_file_list[0], element, theta_index) 
        print("\n (element, theta.shape, proj.shape)", element, len(h5_file_list), proj.shape)
        data = zeros([len(h5_file_list), proj.shape[0], proj.shape[1]])
        theta = zeros([len(h5_file_list)])

        for i, fname in enumerate(h5_file_list):
            proj, theta_image = read_projection(top+fname, element, theta_index) 
            data[i, :, :] = proj
            theta[i] = theta_image
            if fformat == "tiff":
                dxchange.write_tiff(proj, out + "_" + element + ".tiff")
        if fformat == "hdf":
            write_dxfile(out + "_" + element + ".h5", data, theta, element)
    else:
        print("Directory or File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])
