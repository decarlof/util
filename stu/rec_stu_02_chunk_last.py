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
    dictionary = {192: {"0192": 1278.5}, 193: {"0193": 1278.5}, 194: {"0194": 1278.5}, 195: {"0195": 1278.5}, 196: {"0196": 1278.5}, 197: {"0197": 1278.5}, 198: {"0198": 1278.5}, 199: {"0199": 1278.5}, 200: {"0200": 1278.5},
    201: {"0201": 1280.0}, 202: {"0202": 1280.0}, 203: {"0203": 1280.0}, 204: {"0204": 1280.0}, 205: {"0205": 1280.0}, 206: {"0206": 1280.0}, 207: {"0207": 1280.0}, 208: {"0208": 1280.0}, 209: {"0209": 1280.0}, 210: {"0210": 1280.5}, 
    211: {"0211": 1280.0}, 212: {"0212": 1280.0}, 213: {"0213": 1280.0}, 214: {"0214": 1280.0}, 215: {"0215": 1280.0}, 216: {"0216": 1280.0}, 217: {"0217": 1280.0}, 218: {"0218": 1280.0}, 219: {"0219": 1280.0}, 220: {"0220": 1280.5}, 
    221: {"0221": 1285.5}, 222: {"0222": 1285.5}, 223: {"0223": 1285.5}, 224: {"0224": 1285.5}, 225: {"0225": 1285.5}, 226: {"0226": 1285.5}, 227: {"0227": 1285.5}, 228: {"0228": 1285.5}, 229: {"0229": 1285.5}, 230: {"0230": 1283.5}, 
    231: {"0231": 1284.5}, 232: {"0232": 1284.0}, 233: {"0233": 1277.0}, 234: {"0234": 1277.0}, 235: {"0235": 1277.0}, 236: {"0236": 1277.0}, 237: {"0237": 1277.0}, 238: {"0238": 1277.0}, 239: {"0239": 1277.0}, 240: {"0240": 1277.0}, 
    241: {"0241": 1278.5}, 242: {"0242": 1278.5}, 243: {"0243": 1278.5}, 244: {"0244": 1278.5}, 245: {"0245": 1278.5}, 246: {"0246": 1278.5}, 247: {"0247": 1278.5}, 248: {"0248": 1278.5}, 249: {"0249": 1278.5}, 250: {"0250": 1278.5}, 
    251: {"0251": 1282.5}, 252: {"0252": 1282.5}, 253: {"0253": 1282.5}, 254: {"0254": 1282.5}, 255: {"0255": 1282.5}, 256: {"0256": 1282.5}, 257: {"0257": 1282.5}, 258: {"0258": 1281.0}, 259: {"0259": 1282.5}, 260: {"0260": 1282.5}, 
    261: {"0261": 1278.0}, 262: {"0262": 1278.0}, 263: {"0263": 1285.0}, 265: {"0265": 1278.0}, 266: {"0266": 1278.0}, 267: {"0267": 1278.0}, 268: {"0268": 1278.0}, 269: {"0269": 1278.0}, 270: {"0270": 1278.0}, 
    271: {"0271": 1278.5}, 272: {"0272": 1278.5}, 273: {"0273": 1278.5}, 274: {"0274": 1278.5}, 275: {"0275": 1278.5}, 276: {"0276": 1278.5}, 277: {"0277": 1278.5}, 278: {"0278": 1278.5}, 279: {"0279": 1278.5}, 280: {"0280": 1278.5}, 
    281: {"0281": 1273.5}, 282: {"0282": 1273.5}, 283: {"0283": 1273.5}, 284: {"0284": 1273.5}, 285: {"0285": 1273.5}, 286: {"0286": 1273.5}, 287: {"0287": 1273.5}, 288: {"0288": 1273.5}, 289: {"0289": 1273.5}, 290: {"0290": 1273.5}, 
    291: {"0291": 1280.0}, 292: {"0292": 1280.0}, 293: {"0293": 1280.0}, 294: {"0294": 1280.0}, 295: {"0295": 1280.0}, 296: {"0296": 1280.0}, 297: {"0297": 1280.0}, 298: {"0298": 1280.0}, 299: {"0299": 1280.0}, 300: {"0300": 1280.0},
    301: {"0301": 1280.0}, 302: {"0302": 1280.0}, 303: {"0303": 1280.0}, 304: {"0304": 1280.0}} 

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
