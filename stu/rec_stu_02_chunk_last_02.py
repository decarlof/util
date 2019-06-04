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
    top = '/local/decarlo/data/'

    # Auto generated dictionary by find_center to contain {exp_number : center of rotation}
    dictionary = {212: {"0212": 1280.0}, 213: {"0213": 1280.0}, 214: {"0214": 1280.0}, 215: {"0215": 1280.0}, 216: {"0216": 1280.0}, 217: {"0217": 1280.0}, 218: {"0218": 1280.0}, 219: {"0219": 1280.0}, 220: {"0220": 1280.5}, 
    221: {"0221": 1285.5}, 222: {"0222": 1285.5}, 223: {"0223": 1285.5}} 

    sample_detector_distance = 60      # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 0.65e-4    # Detector pixel size in cm
    monochromator_energy = 24.9        # Energy of incident wave in keV

    # Select sinogram range to reconstruct.
    sino_start = 0
    sino_end = 1400

    chunks = 8          # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction
    for key in dictionary:
        dict2 = dictionary[key]
        for key2 in dict2:
            prefix = 'exp_'
            index = key2
            fname = top + prefix + index + '/proj_' + index + '.hdf'
            rot_center = dict2[key2]
            #print(fname, rot_center)

            nSino_per_chunk = (sino_end - sino_start)/chunks
            print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            
            strt = 0
            for iChunk in range(0,chunks):
                print('\n  -- chunk # %i' % (iChunk+1))
                sino_chunk_start = sino_start + nSino_per_chunk*iChunk 
                sino_chunk_end = sino_start + nSino_per_chunk*(iChunk+1)
                print('\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                
                if sino_chunk_end > sino_end: 
                    break

                sino = (sino_chunk_start, sino_chunk_end)
                
                # Read APS 32-ID raw data.
                proj, flat, dark, theta = dxchange.read_aps_32id(fname, sino=sino)

                # Flat-field correction of raw data.
                proj = tomopy.normalize(proj, flat, dark)

                # remove stripes
                #proj = tomopy.remove_stripe_fw(proj,level=5,wname='sym16',sigma=1,pad=True)
                proj = tomopy.remove_stripe_ti(proj,2)
                proj = tomopy.remove_stripe_sf(proj,10)

                # phase retrieval
                #data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=8e-3,pad=True)

                # Find rotation center
                #rot_center = tomopy.find_center(proj, theta, init=rot_center, ind=start, tol=0.5)
                print(index, rot_center)

                proj = tomopy.minus_log(proj)

                # Reconstruct object using Gridrec algorithm.
                rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

                # Mask each reconstructed slice with a circle.
                rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

                # Write data as stack of TIFs.
                recfname = top +'full_rec/' + prefix + index + '/recon'
                print("Rec: ", recfname)
                dxchange.write_tiff_stack(rec, fname=recfname, start=strt)
                strt += proj.shape[1]
