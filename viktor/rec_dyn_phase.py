#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct a single data set.
"""
from __future__ import print_function

import os
import sys
import json
import argparse
import collections

import h5py
import tomopy
import tomopy.util.dtype as dtype
import dxchange

import numpy as np

# sirtfilter:
# conda install -c astra-toolbox astra-toolbox
# conda install -c http://dmpelt.gitlab.io/sirtfilter/ sirtfilter
import sirtfilter
   
def get_dx_dims(fname, dataset):
    """
    Read array size of a specific group of Data Exchange file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.

    Returns
    -------
    ndarray
        Data set size.
    """

    grp = '/'.join(['exchange', dataset])

    with h5py.File(fname, "r") as f:
        try:
            data = f[grp]
        except KeyError:
            return None

        shape = data.shape

    return shape


def restricted_float(x):

    x = float(x)
    if x < 0.0 or x >= 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x


def read_rot_centers(fname):

    try:
        with open(fname) as json_file:
            json_string = json_file.read()
            dictionary = json.loads(json_string)

        return collections.OrderedDict(sorted(dictionary.items()))

    except Exception as error: 
        print("ERROR: the json file containing the rotation axis locations is missing")
        print("ERROR: run: python find_center.py to create one first")
        exit()


def rec_sirtfbp(data, theta, rot_center, start=0, test_sirtfbp_iter = True):

    # Use test_sirtfbp_iter = True to test which number of iterations is suitable for your dataset
    # Filters are saved in .mat files in "./¨
    if test_sirtfbp_iter:
        nCol = data.shape[2]
        output_name = './test_iter/'
        num_iter = [50,100,150]
        filter_dict = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
        for its in num_iter:
            tomopy_filter = sirtfilter.convert_to_tomopy_filter(filter_dict[its], nCol)
            rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
            output_name_2 = output_name + 'sirt_fbp_%iiter_slice_' % its
            dxchange.write_tiff_stack(data, fname=output_name_2, start=start, dtype='float32')

    # Reconstruct object using sirt-fbp algorithm:
    num_iter = 100
    nCol = data.shape[2]
    sirtfbp_filter = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
    tomopy_filter = sirtfilter.convert_to_tomopy_filter(sirtfbp_filter, nCol)
    rec = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
    
    return rec


def reconstruct(h5fname, sino, rot_center, binning, algorithm='gridrec'):

    sample_detector_distance = 31      # Propagation distance of the wavefront in cm
    detector_pixel_size_x = 1.17e-4    # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
    monochromator_energy = 65    # Energy of incident wave in keV
    # used pink beam

    alpha = 1e-5*2**4                       # Phase retrieval coeff.
    zinger_level = 800                  # Zinger level for projections
    zinger_level_w = 1000               # Zinger level for white

    # Read APS 2-BM raw data.
    # DIMAX saves 3 files: proj, flat, dark
    # when loading the data set select the proj file (larger size)

    fname = os.path.splitext(h5fname)[0]    
 
    fbase = fname.rsplit('_', 1)[0]
    fnum = fname.rsplit('_', 1)[1]
    fext = os.path.splitext(h5fname)[1]  

    fnum_flat = str("%4.4d" % (int(fnum)+1))
    fnum_dark = str("%4.4d" % (int(fnum)+2))

    fnproj = fbase + '_' + fnum + fext
    fnflat = fbase + '_' + fnum_flat + fext
    fndark = fbase + '_' + fnum_dark + fext
    
    print('proj', fnproj)
    print('flat', fnflat)
    print('dark', fndark)
    # Read APS 2-BM DIMAX raw data.
    proj, dum, dum2, theta = dxchange.read_aps_32id(fnproj, sino=sino)
    dum3, flat, dum4, dum5 = dxchange.read_aps_32id(fnflat, sino=sino)
    #flat, dum3, dum4, dum5 = dxchange.read_aps_32id(fnflat, sino=sino)          
    dum6, dum7, dark, dum8 = dxchange.read_aps_32id(fndark, sino=sino)

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)        
    
    # zinger_removal
    proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
    flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

    # Flat-field correction of raw data.
    ##data = tomopy.normalize(proj, flat, dark, cutoff=0.8)
    data = tomopy.normalize(proj, flat, dark)

    # remove stripes
    #data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)

    #data = tomopy.remove_stripe_ti(data, alpha=1.5)
    data = tomopy.remove_stripe_sf(data, size=150)

    # phase retrieval
    data = tomopy.prep.phase.retrieve_phase(data,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)

    print("Raw data: ", h5fname)
    print("Center: ", rot_center)

    data = tomopy.minus_log(data)

    data = tomopy.remove_nan(data, val=0.0)
    data = tomopy.remove_neg(data, val=0.00)
    data[np.where(data == np.inf)] = 0.00

    rot_center = rot_center/np.power(2, float(binning))
    data = tomopy.downsample(data, level=binning) 
    data = tomopy.downsample(data, level=binning, axis=1)

    # padding 
    N = data.shape[2]
    data_pad = np.zeros([data.shape[0],data.shape[1],3*N//2],dtype = "float32")
    data_pad[:,:,N//4:5*N//4] = data
    data_pad[:,:,0:N//4] = np.tile(np.reshape(data[:,:,0],[data.shape[0],data.shape[1],1]),(1,1,N//4))
    data_pad[:,:,5*N//4:] = np.tile(np.reshape(data[:,:,-1],[data.shape[0],data.shape[1],1]),(1,1,N//4))

    data = data_pad
    rot_center = rot_center+N//4

    nframes = 1 
    nproj = 1500
    theta = np.linspace(0, np.pi*nframes, nproj*nframes, endpoint=False)
    rec = np.zeros(
            (nframes, data.shape[1], data.shape[2], data.shape[2]), dtype='float32')
    for time_frame in range(0, nframes):
        rec0 = tomopy.recon(data[time_frame*nproj:(time_frame+1)*nproj], theta[time_frame*nproj:(
               time_frame+1)*nproj], center=rot_center, algorithm='gridrec')
        # Mask each reconstructed slice with a circle.
        rec[time_frame] = tomopy.circ_mask(rec0, axis=0, ratio=0.95)
    rec = rec[:,:,N//4:5*N//4,N//4:5*N//4]

        
    print("Algorithm: ", algorithm)
    
    return rec
      

def rec_full(h5fname, rot_center, algorithm, binning):
    
    data_shape = get_dx_dims(h5fname, 'data')

    # Select sinogram range to reconstruct.
    sino_start = 600
    sino_end = 728#data_shape[1]

    chunks = 16          # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction

    nSino_per_chunk = (sino_end - sino_start)//chunks
    print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            

    strt = 0
    for iChunk in range(0,chunks):
        print('\n  -- chunk # %i' % (iChunk+1))
        sino_chunk_start = np.int(sino_start + nSino_per_chunk*iChunk)
        sino_chunk_end = np.int(sino_start + nSino_per_chunk*(iChunk+1))
        print('\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                
        if sino_chunk_end > sino_end: 
            break

        sino = (int(sino_chunk_start), int(sino_chunk_end))
        # Reconstruct.
        rec = reconstruct(h5fname, sino, rot_center, binning, algorithm)

        nframes = 8
        # Write data as stack of TIFs.
        for time_frame in range(0, nframes):
            fname = os.path.dirname(os.path.abspath(h5fname)) + '/' + os.path.splitext(
                os.path.basename(h5fname))[0] + '_rec_full/' + 'recon' + str(time_frame) + '_'
            print("Reconstructions: ", fname)
            dxchange.write_tiff_stack(rec[time_frame], fname=fname, start=strt)
        strt += (sino[1] - sino[0])/pow(2, binning)                
    

def rec_slice(h5fname, nsino, rot_center, algorithm, binning):
    
    data_shape = get_dx_dims(h5fname, 'data')
    ssino = int(data_shape[1] * nsino)

    # Select sinogram range to reconstruct
    sino = None
        
    start = ssino
    end = start + 1
    sino = (start, end)

    rec = reconstruct(h5fname, sino, rot_center, binning, algorithm)

    nframes = 8
    for time_frame in range(0, nframes):
        fname = os.path.dirname(os.path.abspath(h5fname)) + '/' + os.path.splitext(os.path.basename(
            h5fname))[0] + '_rec_slice/' + 'recon' + str(time_frame) + '_'
        dxchange.write_tiff_stack(rec[time_frame], fname=fname)
    print("Rec: ", fname)
    print("Slice: ", start)

    fname = os.path.dirname(h5fname) + '/' + 'slice_rec/' + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]
    dxchange.write_tiff_stack(rec, fname=fname)
    print("Rec: ", fname)
    print("Slice: ", start)
    
       
def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="File name of the dimax projection file (larger file with lower index number in a group of 3): /data/sample_0001.h5")
    parser.add_argument("--axis", nargs='?', type=str, default="0", help="Rotation axis location (pixel): 1024.0 (default 1/2 image horizontal size)")
    parser.add_argument("--bin", nargs='?', type=int, default=0, help="Reconstruction binning factor as power(2, choice) (default 0, no binning)")
    parser.add_argument("--method", nargs='?', type=str, default="gridrec", help="Reconstruction algorithm: sirtfbp (default gridrec)")
    parser.add_argument("--type", nargs='?', type=str, default="slice", help="Reconstruction type: full, slice (default slice)")
    parser.add_argument("--nsino", nargs='?', type=restricted_float, default=0.5, help="Location of the sinogram to reconstruct (0 top, 1 bottom): 0.5 (default 0.5)")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    fname = args.fname
    algorithm = args.method
    rot_center = float(args.axis)
    binning = int(args.bin)

    nsino = float(args.nsino)

    rec_type = args.type

    if os.path.isfile(fname):    

        print("Reconstructing a single file")   
        # Set default rotation axis location
        if rot_center == 0:
            data_shape = get_dx_dims(fname, 'data')
            rot_center =  data_shape[2]/2
        if rec_type == "full":
            rec_full(fname, rot_center, algorithm=algorithm, binning=binning)
        else:
            rec_slice(fname, nsino, rot_center, algorithm=algorithm, binning=binning)

    else:
        print("Directory or File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])

