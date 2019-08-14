#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy example script to reconstruct a single data set.
"""
from __future__ import print_function

import os
import sys
import time
import gc
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
# git clone https://gitlab.com/dmpelt/sirtfilter.git
# cd sirtfilter/
# python setup.py install

#import sirtfilter


def file_base_name(file_name):
    if '.' in file_name:
        separator_index = file_name.index('.')
        base_name = file_name[:separator_index]
        return base_name
    else:
        return file_name

def path_base_name(path):
    file_name = os.path.basename(path)
    return file_base_name(file_name)


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


def rec_sirtfbp(data, theta, rot_center, start=0, test_sirtfbp_iter = False):

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


def reconstruct(h5fname, sino, rot_center, binning, algorithm='gridrec', options=None, num_iter=100, dark_file=None,
                sample_detector_distance=10,       # Propagation distance of the wavefront in cm
                detector_pixel_size_x=2.247e-4,    # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
                monochromator_energy=35,           # Energy of incident wave in keV
                alpha=1e-01,                       # Phase retrieval coeff.
                zinger_level=500,                  # Zinger level for projections
                zinger_level_w=1000,
                alpha_ti=1.5,
                sf_size=150,
                fw_wname='sym16', fw_level=7,
                retrieve_phase=False,
               ):

    print("Raw data: ", h5fname)
    print("Center: ", rot_center)

    # Read APS 32-BM raw data.
    print('Reading Data.. ', end='')
    t0 = time.time()
    proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
    if dark_file is not None:
        proj_, flat, dark, theta_ = dxchange.read_aps_32id(dark_file, sino=sino)
        del proj_, theta_
    print('Done in {:.0f} sec'.format(time.time() - t0))

    # zinger_removal
    print('Removing Outliers.. ', end='')
    t0 = time.time()
    proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
    flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)
    print('Done ({:.0f} sec)'.format(time.time() - t0))

    # Flat-field correction of raw data.
    print('Normalizing Data.. ', end='')
    t0 = time.time()
    ##data = tomopy.normalize(proj, flat, dark, cutoff=0.8)
    data = tomopy.normalize(proj, flat, dark)
    print('Done ({:.0f} sec)'.format(time.time() - t0))

    # Free up Memory
    del proj, flat, dark

    # Garbage Collection
    gc.collect()

    # remove stripes
    print('Removing Stripes.. ', end='')
    t0 = time.time()
    #data = tomopy.remove_stripe_fw(data, level=fw_level, wname=fw_wname, sigma=1, pad=True)

    #data = tomopy.remove_stripe_ti(data, alpha=alpha_ti)
    print('sf_size = {}'.format(sf_size))
    #data = tomopy.remove_stripe_sf(data, size=sf_size)
    print('Done ({:.0f} sec)'.format(time.time() - t0))

    # phase retrieval
    if retrieve_phase:
        data = tomopy.prep.phase.retrieve_phase(data, pixel_size=detector_pixel_size_x, dist=sample_detector_distance,
                                                energy=monochromator_energy, alpha=alpha, pad=True)

    print('Taking minus Log and removing Nans and negative values.. ', end='')
    t0 = time.time()
    data = tomopy.minus_log(data)

    data = tomopy.remove_nan(data, val=0.0)
    data = tomopy.remove_neg(data, val=0.00)
    data[np.where(data == np.inf)] = 0.00
    print('Done ({:.0f} sec)'.format(time.time() - t0))

    if binning > 0:
        rot_center = rot_center/np.power(2, float(binning))
        data = tomopy.downsample(data, level=binning)
        data = tomopy.downsample(data, level=binning, axis=1)

    # Reconstruct object.
    print('Reconstructing using {}.. '.format(algorithm), end='')
    t0 = time.time()
    if algorithm == 'sirtfbp':
        rec = rec_sirtfbp(data, theta, rot_center)
    elif algorithm == "astra_fbp":
        options = {'proj_type':'linear', 'method':'FBP'}
        rec = tomopy.recon(data, theta, center=rot_center, algorithm=tomopy.astra, options=options, ncore=1)
    elif algorithm == "astra_fbp_cuda":
        options = {'proj_type':'cuda', 'method':'FBP_CUDA'}
        rec = tomopy.recon(data, theta, center=rot_center, algorithm=tomopy.astra, options=options, ncore=1)
    elif algorithm == "astra_sirt":
        extra_options = {'MinConstraint':0}
        options = {'proj_type':'cuda', 'method':'SIRT_CUDA', 'num_iter':num_iter, 'extra_options':extra_options}
        rec = tomopy.recon(data, theta, center=rot_center, algorithm=tomopy.astra, options=options)
    elif algorithm == tomopy.astra:
        rec = tomopy.recon(data, theta, center=rot_center, algorithm=tomopy.astra, options=options)
    else:
        try:
            rec = tomopy.recon(data, theta, center=rot_center, algorithm=algorithm, filter_name='parzen')
        except:
            rec = tomopy.recon(data, theta, center=rot_center, algorithm=algorithm)
    print('Done ({:.0f} sec)'.format(time.time() - t0))

    # Mask each reconstructed slice with a circle.
    print('Masking.. ', end='')
    t0 = time.time()
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
    print('Done ({:.0f} sec)'.format(time.time() - t0))

    del data
    gc.collect()

    return rec


def rec_full(h5fname, rot_center, algorithm, binning, options, num_iter, dark_file, dtype, s_):

    data_shape = get_dx_dims(h5fname, 'data')

    # Select sinogram range to reconstruct.
    sino_start = 0
    sino_end = data_shape[1]

    chunks = 2          # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction

    nSino_per_chunk = (sino_end - sino_start)/chunks
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
        rec = reconstruct(h5fname, sino, rot_center, binning, algorithm, options, num_iter, dark_file)
        rec = rec[s_]

        if iChunk == 0:
            rec_all = np.zeros((sino_end - sino_start, rec.shape[1], rec.shape[2]), dtype=np.float16)

        rec_all[strt:strt+rec.shape[0]] = np.asarray(rec, dtype=np.float16)

        # Clean up
        del rec
        gc.collect()

        strt += sino[1] - sino[0]


    # Write data as stack of TIFs.
    rec = rec_all

    fname = os.path.dirname(h5fname) + os.sep + os.path.splitext(os.path.basename(h5fname))[0]+ '_full_rec/' + os.sep + algorithm + os.sep + 'recon'
    print("Saving Reconstructed Data to {}.. ".format(iChunk, chunks, fname))
    t0 = time.time()

    # Convert to uint16
    if dtype == 'uint16':
        rec = rec - rec.min()
        rec *= 65535/rec.max()

    dxchange.write_tiff_stack(rec, fname=fname, dtype=dtype)

    print('Done ({:.0f} sec)'.format(time.time() - t0))

    # Clean Up
    del rec
    gc.collect()



def rec_slice(h5fname, nsino, rot_center, algorithm, binning, options, num_iter, dark_file, suffix=None, **kwargs):

    t0 = time.time()
    data_shape = get_dx_dims(h5fname, 'data')
    ssino = int(data_shape[1] * nsino)

    # Select sinogram range to reconstruct
    sino = None

    start = ssino
    end = start + 1
    sino = (start, end)

    rec = reconstruct(h5fname, sino, rot_center, binning, algorithm, options, num_iter, dark_file, **kwargs)

    #fname = os.path.dirname(h5fname) + os.sep + 'slice_rec/' + path_base_name(h5fname) + os.sep + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]  + '_' +
    fname = os.path.dirname(h5fname) + os.sep + 'slice_rec/' + path_base_name(h5fname) + os.sep + os.path.splitext(os.path.basename(h5fname))[0]  + '_' + algorithm + '_' + '{}'.format(start) + suffix

    dxchange.write_tiff_stack(rec, fname=fname)
    print("Rec: ", fname)
    print("Slice: ", start)
    print('Done ({:.0f} sec)'.format(time.time() - t0))


def rec_try(h5fname, nsino, rot_center, center_search_width, algorithm, binning, dark_file):

    data_shape = get_dx_dims(h5fname, 'data')
    print(data_shape)
    ssino = int(data_shape[1] * nsino)

    center_range = (rot_center-center_search_width, rot_center+center_search_width, 0.5)
    #print(sino,ssino, center_range)
    #print(center_range[0], center_range[1], center_range[2])

    # Select sinogram range to reconstruct
    sino = None

    start = ssino
    end = start + 1
    sino = (start, end)

    # Read APS 32-BM raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)
    if dark_file is not None:
        print('Reading white/dark from {}'.format(dark_file))
        proj_, flat, dark, theta_ = dxchange.read_aps_32id(dark_file, sino=sino)
        del proj_, theta_

    print(proj.shape, flat.shape, dark.shape)

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    # data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)


    print("Raw data: ", h5fname)
    print("Center: ", rot_center)

    data = tomopy.minus_log(data)

    data = tomopy.remove_nan(data, val=0.0)
    data = tomopy.remove_neg(data, val=0.00)
    data[np.where(data == np.inf)] = 0.00

    stack = np.empty((len(np.arange(*center_range)), data_shape[0], data_shape[2]))

    index = 0
    for axis in np.arange(*center_range):
        stack[index] = data[:, 0, :]
        index = index + 1

    # Reconstruct the same slice with a range of centers.
    rec = tomopy.recon(stack, theta, center=np.arange(*center_range), sinogram_order=True, algorithm='gridrec', filter_name='parzen', nchunk=1)

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    index = 0
    # Save images to a temporary folder.
    #fname = os.path.dirname(h5fname) + os.sep + 'try_rec/' + path_base_name(h5fname) + os.sep + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]
    fname = os.path.dirname(h5fname) + os.sep + 'centers/' + path_base_name(h5fname) + os.sep + 'recon_' + os.path.splitext(os.path.basename(h5fname))[0]
    for axis in np.arange(*center_range):
        rfname = fname + '_' + str('{0:.2f}'.format(axis) + '.tiff')
        dxchange.write_tiff(rec[index], fname=rfname, overwrite=True)
        index = index + 1

    print("Reconstructions: ", fname)



def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("--axis", nargs='?', type=str, default="0", help="Rotation axis location (pixel): 1024.0 (default 1/2 image horizontal size)")
    parser.add_argument("--bin", nargs='?', type=int, default=0, help="Reconstruction binning factor as power(2, choice) (default 0, no binning)")
    parser.add_argument("--method", nargs='?', type=str, default="gridrec", help="Reconstruction algorithm: sirtfbp (default gridrec)")
    parser.add_argument("--type", nargs='?', type=str, default="slice", help="Reconstruction type: full, slice, try (default slice)")
    parser.add_argument("--srs", nargs='?', type=int, default=10, help="+/- center search width (pixel): 10 (default 10). Search is in 0.5 pixel increments")
    parser.add_argument("--nsino", nargs='?', type=restricted_float, default=0.5, help="Location of the sinogram to reconstruct (0 top, 1 bottom): 0.5 (default 0.5)")
    parser.add_argument("--options", nargs='?', type=str, default=None, help="Options for astra-toolbox")
    parser.add_argument("--num_iter", nargs='?', type=int, default=100, help="Number of iteratios for SIRT etc.")
    parser.add_argument("--dark_file", nargs='?', type=str, default=None, help="H5 File to use for Dark and White Images")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    fname = args.fname
    algorithm = args.method
    rot_center = float(args.axis)
    binning = int(args.bin)

    nsino = float(args.nsino)

    rec_type = args.type
    center_search_width = args.srs

    # Options for using tomopy.astra
    options = args.options
    num_iter = args.num_iter

    # Dark/White File
    dark_file = args.dark_file

    if os.path.isfile(fname):

        print("Reconstructing a single file")
        # Set default rotation axis location
        if rot_center == 0:
            data_shape = get_dx_dims(fname, 'data')
            rot_center =  data_shape[2]/2
        if rec_type == "try":
            rec_try(fname, nsino, rot_center, center_search_width, algorithm=algorithm, binning=binning, dark_file=dark_file)
        elif rec_type == "full":
            rec_full(fname, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file)
        else:
            rec_slice(fname, nsino, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file)

    elif os.path.isdir(fname):
        print("Reconstructing a folder containing multiple files")
        # Add a trailing slash if missing
        top = os.path.join(fname, '')

        # Load the the rotation axis positions.
        jfname = top + "rotation_axis.json"

        dictionary = read_rot_centers(jfname)

        for key in dictionary:
            dict2 = dictionary[key]
            for h5fname in dict2:
                rot_center = dict2[h5fname]
                fname = top + h5fname
                print("Reconstructing ", h5fname)
                # Set default rotation axis location
                if rot_center == 0:
                    data_shape = get_dx_dims(fname, 'data')
                    rot_center =  data_shape[2]/2
                if rec_type == "try":
                    rec_try(fname, nsino, rot_center, center_search_width, algorithm=algorithm, binning=binning, dark_file=dark_file)
                elif rec_type == "full":
                    rec_full(fname, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file)
                else:
                    rec_slice(fname, nsino, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file)
    else:
        print("Directory or File Name does not exist: ", fname)


def rec(fname, rot_center=0, binning=0, algorithm='gridrec', rec_type='slice',
        center_search_width=10, nsino=0.5, options=None, num_iter=100, dark_file=None,
        dtype='uint16', s_=np.s_[:, :, :], suffix=None, **kwargs):

    t0 = time.time()

    rot_center = float(rot_center)
    if os.path.isfile(fname):

        #print("Reconstructing a single file")
        # Set default rotation axis location
        if rot_center == 0:
            data_shape = get_dx_dims(fname, 'data')
            rot_center =  data_shape[2]/2
        if rec_type == "try":
            rec_try(fname, nsino, rot_center, center_search_width, algorithm=algorithm, binning=binning, dark_file=dark_file)
        elif rec_type == "full":
            rec_full(fname, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file, dtype=dtype, s_=s_)
        else:
            rec_slice(fname, nsino, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file, suffix=suffix, **kwargs)

    elif os.path.isdir(fname):
        print("Reconstructing a folder containing multiple files")
        # Add a trailing slash if missing
        top = os.path.join(fname, '')

        # Load the the rotation axis positions.
        jfname = top + "rotation_axis.json"

        dictionary = read_rot_centers(jfname)

        for key in dictionary:
            dict2 = dictionary[key]
            for h5fname in dict2:
                rot_center = dict2[h5fname]
                fname = top + h5fname
                print("Reconstructing ", h5fname)
                # Set default rotation axis location
                if rot_center == 0:
                    data_shape = get_dx_dims(fname, 'data')
                    rot_center =  data_shape[2]/2
                if rec_type == "try":
                    rec_try(fname, nsino, rot_center, center_search_width, algorithm=algorithm, binning=binning, dark_file=dark_file)
                elif rec_type == "full":
                    rec_full(fname, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file, dtype=dtype, s_=s_)
                else:
                    rec_slice(fname, nsino, rot_center, algorithm=algorithm, binning=binning, options=options, num_iter=num_iter, dark_file=dark_file)
    else:
        print("Directory or File Name does not exist: ", fname)

    print('All Done ({:.0f} minutes)\n'.format((time.time() - t0)/60))

if __name__ == "__main__":
    main(sys.argv[1:])
