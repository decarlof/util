#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct 2017-06/Stu data sets.
"""

from __future__ import print_function
import tomopy
import dxchange

if __name__ == '__main__':

    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/Stu/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {1: {"0001": 1122.5}, 2: {"0002": 1122.5}, 3: {"0003": 1122.0}, 4: {"0004": 1122.0}, 5: {"0005": 1122.5}, 6: {"0006": 1122.5}, 7: {"0007": 1122.5}, 8: {"0008": 1122.5}, 9: {"0009": 1122.5}, 10: {"0010": 1122.5},  
    15: {"0015": 1122.5}, 16: {"0016": 1122.5}, 17: {"0017": 1122.5}, 18: {"0018": 1122.5}, 19: {"0019": 1122.5}, 20: {"0020": 1124.5}, 
    21: {"0021": 1122.5}, 22: {"0022": 1122.5}, 23: {"0023": 1122.5}, 24: {"0024": 1122.5}, 25: {"0025": 1122.5}, 26: {"0026": 1122.5}, 27: {"0027": 1122.5}, 28: {"0028": 1122.5}, 29: {"0029": 1122.5}, 30: {"0030": 1122.5}, 
    31: {"0031": 1122.5}, 32: {"0032": 1122.5}, 33: {"0033": 1122.5}, 34: {"0034": 1122.5}, 35: {"0035": 1122.5}, 36: {"0036": 1122.5}, 37: {"0037": 1122.5}, 38: {"0038": 1122.5}, 39: {"0039": 1122.5}, 40: {"0040": 1124.5}, 
    41: {"0041": 1122.5}, 42: {"0042": 1122.5}, 43: {"0043": 1122.5}, 44: {"0044": 1122.5}, 45: {"0045": 1122.5}, 46: {"0046": 1122.5}, 47: {"0047": 1122.5}, 48: {"0048": 1122.5}, 49: {"0049": 1122.5}, 50: {"0050": 1122.5}, 
    51: {"0051": 1122.5}, 56: {"0056": 1122.5}, 77: {"0077": 1122.5}, 92: {"0092": 1122.5}, 98: {"0098": 1122.5}, 99: {"0099": 1122.5}, 100: {"0100": 1122.5},
    101: {"0101": 1129.0}, 102: {"0102": 1131.5}, 103: {"0103": 1130.0}, 104: {"0104": 1131.5}, 105: {"0105": 1129.0}, 106: {"0106": 1131.5}, 107: {"0107": 1129.0}, 108: {"0108": 1129.0}, 109: {"0109": 1132.5}, 110: {"0110": 1132.5}, 
    111: {"0111": 1131.5}, 112: {"0112": 1131.5}, 113: {"0113": 1131.5}, 114: {"0114": 1131.5}, 115: {"0115": 1131.5}, 116: {"0116": 1131.5}, 117: {"0117": 1131.5}, 118: {"0118": 1131.5}, 119: {"0119": 1131.5}, 120: {"0120": 1131.5}} 
    for key in dictionary:
        dict2 = dictionary[key]
        for key2 in dict2:
            prefix = 'exp_'
            index = key2
            fname = top + prefix + index + '/proj_' + index + '.hdf'
            rot_center = dict2[key2]
            #print(fname, rot_center)

            # Select sinogram range to reconstruct.
            sino = None
            
            start = 285
            end = 286
            sino = (start, end)
            
            # Read APS 32-ID raw data.
            proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=sino)

            # Flat-field correction of raw data.
            proj = tomopy.normalize(proj, flat, dark)

            # remove stripes
            proj = tomopy.remove_stripe_fw(proj,level=5,wname='sym16',sigma=1,pad=True)

            # Find rotation center
            #rot_center1 = tomopy.find_center(proj, theta, init=rot_center, ind=start, tol=0.5)
            print(index, rot_center)

            proj = tomopy.minus_log(proj)

            # Reconstruct object using Gridrec algorithm.
            rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

            # Mask each reconstructed slice with a circle.
            rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

            # Write data as stack of TIFs.
            ##fname = top +'rec_' + prefix + index + '/recon'
            fname = top +'rec_slice_' + prefix + '/recon'
            print("Rec: ", fname)
            dxchange.write_tiff_stack(rec, fname=fname)
