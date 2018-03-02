#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example to reconstruct with gridrec the HZG nano tomography projections.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    top = '/local/dataraid/JenBauer/'
    h5ext = '.h5'
    
    
#    1: {"HA_UTK1_WB_30mmGlass_200mm_2mic_001": 1024.0}, 
#                  2: {"HA_UTK1_WB_30mmGlass_200mm_2mic_002": 1024.0}, 
#                  3: {"HA_UTK1_WB_30mmGlass_200mm_2mic_003": 1024.0}, 
#                  4: {"HA_UTK1_WB_30mmGlass_200mm_2mic_004": 1024.0}, 
#                  5: {"HA_UTK1_WB_30mmGlass_200mm_2mic_005": 1024.0}, 
#                  6: {"HA_UTK1_WB_30mmGlass_200mm_2mic_006": 1024.0},
#                  7: {"HA_UTK2_deco_25keV_300mm_001": 1024.0},
#                  8: {"HA_UTK2_deco_25keV_300mm_002": 1024.0},
#                  9: {"HA_UTK2_deco_25keV_300mm_003": 1024.0},
    dictionary = {10: {"UTK3_WB_30mmGlass_200mm_2mic_001": 972.0},
                  11: {"UTK3_WB_30mmGlass_200mm_2mic_002": 972.0},
                  12: {"UTK3_WB_30mmGlass_200mm_2mic_003": 972.0},
                  13: {"UTK3_WB_30mmGlass_200mm_2mic_004": 972.0},
                  14: {"UTK2_25keV_300mm_001": 903},
                  15: {"UTK2_25keV_300mm_002": 920.5},
                  16: {"UTK2_25keV_300mm_003": 930.0},
                  17: {"UTK2_WB_Glass30mm_001": 958.0},
                  18: {"UTK2_WB_Glass30mm_002": 955.0},
                  19: {"UTK2_WB_Glass30mm_003": 955.0}}

    prefix = ''
    for key in sorted(dictionary):
        dict2 = dictionary[key]
        for h5name in dict2:
            fname = top + h5name + h5ext 
            rot_center = dict2[h5name]
            print('fname', key,fname, rot_center)

            sample_detector_distance = 18.8e2
            detector_pixel_size_x = 19.8e-7
            monochromator_energy = 11.0

            # Set the [start, end] index of the blocked projections.
            ##miss_projs = [0, 2]


            # Select the sinogram range to reconstruct.
            sino = None
            
            start = 600
            end = 601
            sino = (start, end)

            # Read the APS raw data.
            proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=sino)

            # Remove the missing angles from data.
            ##proj = np.concatenate((proj[0:miss_projs[0], :, :], proj[miss_projs[1] + 1:-1, :, :]), axis=0)
            ##theta = np.concatenate((theta[0:miss_projs[0]], theta[miss_projs[1] + 1:-1]))

            # Flat-field correction of raw data.
            if key in (10, 11, 12, 13):
                data = proj / 10000.
            else:
                data = tomopy.normalize(proj, flat, dark)
            
            #data = tomopy.remove_stripe_ti(data,2)
            #data = tomopy.remove_stripe_sf(proj,10)

            # Find rotation center.
            #rot_center = tomopy.find_center(proj, theta, emission=False, init=1024, ind=0, tol=0.5)
            
            print("Center of rotation: ", rot_center)

            data = tomopy.minus_log(data)

            # Reconstruct object using Gridrec algorithm.
            rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

            # Mask each reconstructed slice with a circle.
            rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

            # Write data as stack of TIFs.
            ##fname = top +'full_rec/' + prefix + h5name + '/recon'
            fname = top +'slice_rec/' + prefix + h5name + '_recon'
            dxchange.write_tiff_stack(rec, fname=fname)
