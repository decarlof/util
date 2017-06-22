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
    dictionary = {195: {"0195": 1278.5}, 196: {"0196": 1278.5}, 197: {"0197": 1278.5}, 198: {"0198": 1278.5}, 199: {"0199": 1278.5}, 200: {"0200": 1278.5},
    201: {"0201": 1280.0}, 202: {"0202": 1280.0}, 203: {"0203": 1280.0}, 204: {"0204": 1280.0}, 205: {"0205": 1280.0}, 206: {"0206": 1280.0}, 207: {"0207": 1280.0}, 208: {"0208": 1280.0}, 209: {"0209": 1280.0}, 210: {"0210": 1280.5}, 
    211: {"0211": 1280.0}} 

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
