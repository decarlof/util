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
import pathlib

import h5py
import tomopy
import tomopy.util.dtype as dtype
import dxchange
import dxchange.reader as dxreader

import numpy as np
from datetime import datetime

import matplotlib.pylab as pl
import matplotlib.widgets as wdg

import log_lib


variableDict = {'fname': 'data.h5',
        'nsino': 0.5,
        'algorithm': 'gridrec',
        'binning': 0,
        'rot_center': 1024,
        'rec_type': 'slice',
        'center_search_width': 10,
        'alpha': 1e-2,                         # Phase retrieval coeff.     
        'sample_detector_distance': 40,        # Propagation distance of the wavefront in cm
        'detector_pixel_size_x' : 0.69e-4,     # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
        'monochromator_energy' : 25,           # Energy of incident wave in keV                   
        'zinger_level' : 800,                  # Zinger level for projections
        'zinger_level_w' : 1000,               # Zinger level for white
        'reverse' : False,                     # True for 180-0 data set
        'auto' : False,                        # True to use autocentering
        'phase' :  False,                      # Use phase retrival    
        'logs_home' : '.',
        'plot' : False
        }


class slider():
    def __init__(self, data, axis):
        self.data = data
        self.axis = axis

        ax = pl.subplot(111)
        pl.subplots_adjust(left=0.25, bottom=0.25)

        self.frame = 0
        self.l = pl.imshow(self.data[self.frame,:,:], cmap='gist_gray') 

        axcolor = 'lightgoldenrodyellow'
        axframe = pl.axes([0.25, 0.1, 0.65, 0.03])
        self.sframe = wdg.Slider(axframe, 'Frame', 0, self.data.shape[0]-1, valfmt='%0.0f')
        self.sframe.on_changed(self.update)

        pl.show()

    def update(self, val):
        self.frame = int(np.around(self.sframe.val))
        self.l.set_data(self.data[self.frame,:,:])
        log_lib.info('%f' % self.axis[self.frame])


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
        log_lib.error("ERROR: the json file containing the rotation axis locations is missing")
        log_lib.error("ERROR: run: python find_center.py to create one first")
        exit()


def reconstruct(variableDict, sino):

    # Read APS 32-BM raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(variableDict['fname'], sino=sino)
        
    if variableDict['reverse']:
        step_size = (theta[1] - theta[0]) 
        theta_size = dxreader.read_dx_dims(variableDict['fname'], 'data')[0]
        theta = np.linspace(np.pi , (0+step_size), theta_size)    # zinger_removal
        log_lib.warning("  *** overwrite theta")

    # zinger_removal
    # proj = tomopy.misc.corr.remove_outlier(proj, variableDict['zinger_level'], size=15, axis=0)
    # flat = tomopy.misc.corr.remove_outlier(flat, variableDict['zinger_level']_w, size=15, axis=0)

    if (variableDict['phase'] is False):
        data = tomopy.normalize(proj, flat, dark)
    # remove stripes
    #data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)

    # data = tomopy.remove_stripe_ti(data, variableDict['alpha']=1.5)
    # data = tomopy.remove_stripe_sf(data, size=150)

    # phase retrieval
    if (variableDict['phase']):
        data = tomopy.prep.phase.retrieve_phase(data,pixel_size=variableDict['detector_pixel_size_x'],dist=variableDict['sample_detector_distance'],energy=variableDict['monochromator_energy'], alpha=variableDict['alpha'],pad=True)

    log_lib.info("  *** raw data: %s" % variableDict['fname'])
    log_lib.info("  *** center: %f" % variableDict['rot_center'])

    if (variableDict['phase'] is False):
        data = tomopy.minus_log(data)

    data = tomopy.remove_nan(data, val=0.0)
    data = tomopy.remove_neg(data, val=0.00)
    data[np.where(data == np.inf)] = 0.00

    variableDict['rot_center'] = variableDict['rot_center']/np.power(2, float(variableDict['binning']))
    data = tomopy.downsample(data, level=variableDict['binning']) 
    data = tomopy.downsample(data, level=variableDict['binning'], axis=1)

    # padding 
    N = data.shape[2]
    data_pad = np.zeros([data.shape[0],data.shape[1],3*N//2],dtype = "float32")
    data_pad[:,:,N//4:5*N//4] = data
    data_pad[:,:,0:N//4] = np.reshape(data[:,:,0],[data.shape[0],data.shape[1],1])
    data_pad[:,:,5*N//4:] = np.reshape(data[:,:,-1],[data.shape[0],data.shape[1],1])
    data = data_pad
    rot_center = variableDict['rot_center']+N//4

    # Reconstruct object.
    log_lib.info("  *** algorithm: %s" % variableDict['algorithm'])
    if variableDict['algorithm'] == 'astrasirt':
        extra_options ={'MinConstraint':0}
        options = {'proj_type':'cuda', 'method':'SIRT_CUDA', 'num_iter':200, 'extra_options':extra_options}
        rec = tomopy.recon(data, theta, center=rot_center, algorithm=tomopy.astra, options=options)
    else:        
        rec = tomopy.recon(data, theta, center=rot_center, algorithm=variableDict['algorithm'], filter_name='parzen')
 
    rec = rec[:,N//4:5*N//4,N//4:5*N//4]


    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)
    
    return rec
      

def rec_full(variableDict):
    
    data_shape = get_dx_dims(variableDict['fname'], 'data')

    # Select sinogram range to reconstruct.
    sino_start = 0
    sino_end = data_shape[1]

    chunks = 6          # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction

    nSino_per_chunk = (sino_end - sino_start)/chunks
    log_lib.info("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            

    strt = 0
    for iChunk in range(0,chunks):
        log_lib.info('chunk # %i' % (iChunk+1))
        sino_chunk_start = np.int(sino_start + nSino_per_chunk*iChunk)
        sino_chunk_end = np.int(sino_start + nSino_per_chunk*(iChunk+1))
        log_lib.info('  *** [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                
        if sino_chunk_end > sino_end: 
            break

        sino = (int(sino_chunk_start), int(sino_chunk_end))
        # Reconstruct.
        rec = reconstruct(variableDict, sino)
                
        if os.path.dirname(variableDict['fname']) is not '':
            fname = os.path.dirname(variableDict['fname']) + os.sep + os.path.splitext(os.path.basename(variableDict['fname']))[0]+ '_full_rec/' + 'recon'
        else:
            fname = '.' + os.sep + os.path.splitext(os.path.basename(variableDict['fname']))[0]+ '_full_rec/' + 'recon'

        log_lib.info("  *** reconstructions: %s" % fname)
        dxchange.write_tiff_stack(rec, fname=fname, start=strt)
        strt += sino[1] - sino[0]

    log = "python rec.py --axis " + str(variableDict['rot_center']) + " --type full " + variableDict['fname'] + "\n"
    log_lib.info('  *** command to repeat the reconstruction: %s' % log)

    p = pathlib.Path(fname)
    lfname = variableDict['logs_home'] + p.parts[-3] + '.log'
    log_lib.info('  *** command added to %s ' % lfname)
    with open(lfname, "a") as myfile:
        myfile.write(log)
    
def rec_phase(variableDict):
    
    data_shape = get_dx_dims(variableDict['fname'], 'data')
    ssino = int(data_shape[1] * variableDict['nsino'])

    # Select sinogram range to reconstruct       
    sino_start = ssino - 32
    sino_end = ssino + 32
    chunks = 1          # number of sinogram chunks to reconstruct
                        # only one chunk at the time is reconstructed
                        # allowing for limited RAM machines to complete a full reconstruction

    nSino_per_chunk = (sino_end - sino_start)/chunks
    log_lib.info("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            

    strt = 0
    for iChunk in range(0,chunks):
        log_lib.info('chunk # %i' % (iChunk+1))
        sino_chunk_start = np.int(sino_start + nSino_per_chunk*iChunk)
        sino_chunk_end = np.int(sino_start + nSino_per_chunk*(iChunk+1))
        log_lib.info('  *** [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                
        if sino_chunk_end > sino_end: 
            break

        sino = (int(sino_chunk_start), int(sino_chunk_end))
        # Reconstruct.
        alphaa = [1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 5e-2, 1e-1, 5e-1, 1]
        for k in range(len(alphaa)):
            variableDict['alpha'] = alphaa[k]
            rec = reconstruct(variableDict, sino)
                
            if os.path.dirname(variableDict['fname']) is not '':
                fname = os.path.dirname(variableDict['fname']) + os.sep + os.path.splitext(os.path.basename(variableDict['fname']))[0]+ '_subset_rec/' + 'recon_' + str(alphaa[k])
            else:
                fname = '.' + os.sep + os.path.splitext(os.path.basename(variableDict['fname']))[0]+ '_subset_rec/' + 'recon_' + str(alphaa[k])

            log_lib.info("  *** reconstructions: %s" % fname)
            dxchange.write_tiff_stack(rec, fname=fname, start=strt)
        strt += sino[1] - sino[0]

    log = "python rec.py --axis " + str(variableDict['rot_center']) + " --type subset " + variableDict['fname'] + "\n"
    log_lib.info('  *** command to repeat the reconstruction: %s' % log)

    p = pathlib.Path(fname)
    lfname = variableDict['logs_home'] + p.parts[-3] + '.log'
    log_lib.info('  *** comnad added to %s ' % lfname)
    with open(lfname, "a") as myfile:
        myfile.write(log)

def rec_slice(variableDict):
    
    data_shape = get_dx_dims(variableDict['fname'], 'data')
    ssino = int(data_shape[1] * variableDict['nsino'])

    # Select sinogram range to reconstruct       
    start = ssino
    end = start + 1
    sino = (start, end)

    rec = reconstruct(variableDict, sino)

    if os.path.dirname(variableDict['fname']) is not '':
        fname = os.path.dirname(variableDict['fname']) + os.sep + 'slice_rec/' + 'recon_' + os.path.splitext(os.path.basename(variableDict['fname']))[0]
    else:
        fname = './slice_rec/' + 'recon_' + os.path.splitext(os.path.basename(variableDict['fname']))[0]
    dxchange.write_tiff_stack(rec, fname=fname)
    log_lib.info("  *** rec: %s" % fname)
    log_lib.info("  *** slice: %d" % start)
    

def rec_try(variableDict):
    
    data_shape = get_dx_dims(variableDict['fname'], 'data')
    log_lib.info(data_shape)
    ssino = int(data_shape[1] * variableDict['nsino'])
    center_range = (variableDict['rot_center']-variableDict['center_search_width'], variableDict['rot_center']+variableDict['center_search_width'], 0.5)
    log_lib.info('  *** reconstruct slice %d with rotation axis ranging from %.2f to %.2f in %.2f pixel steps' % (ssino, center_range[0], center_range[1], center_range[2]))

    # log_lib.info(center_range[0], center_range[1], center_range[2])

    # Select sinogram range to reconstruct
    start = ssino
    end = start + 1
    sino = (start, end)

    # Read APS 32-BM raw data.
    proj, flat, dark, theta = dxchange.read_aps_32id(variableDict['fname'], sino=sino)

    if variableDict['reverse']:
        step_size = (theta[1] - theta[0]) 
        theta_size = dxreader.read_dx_dims(variableDict['fname'], 'data')[0]
        theta = np.linspace(np.pi , (0+step_size), theta_size)    # zinger_removal
        log_lib.warning("  *** overwrite theta")

    # Flat-field correction of raw data.
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    # data = tomopy.remove_stripe_fw(data,level=7,wname='sym16',sigma=1,pad=True)


    log_lib.info("  *** raw data: %s" % variableDict['fname'])
    log_lib.info("  *** center: %f" % variableDict['rot_center'])

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
    fname = os.path.dirname(variableDict['fname']) + os.sep + 'try_rec/' + path_base_name(variableDict['fname']) + os.sep + 'recon_' ##+ os.path.splitext(os.path.basename(variableDict['fname']))[0]    
    for axis in np.arange(*center_range):
        rfname = fname + str('{0:.2f}'.format(axis) + '.tiff')
        dxchange.write_tiff(rec[index], fname=rfname, overwrite=True)
        index = index + 1

    log_lib.info("  *** reconstructions: %s" % fname)

    if variableDict['plot']:
        slider(rec, np.arange(*center_range))
     

def find_rotation_axis(variableDict):
    

    log_lib.info("  *** calculating automatic center")
    data_size = get_dx_dims(variableDict['fname'], 'data')
    ssino = int(data_size[1] * variableDict['nsino'])

    # Select sinogram range to reconstruct
    start = ssino
    end = start + 1
    sino = (start, end)

    # Read APS 32-BM raw data
    proj, flat, dark, theta = dxchange.read_aps_32id(variableDict['fname'], sino=sino)
        
    # Flat-field correction of raw data
    data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

    # remove stripes
    data = tomopy.remove_stripe_fw(data,level=5,wname='sym16',sigma=1,pad=True)

    # find rotation center
    rot_center = tomopy.find_center_vo(data)   
    log_lib.info("  *** automatic center: %f" % rot_center)
    return rot_center


def main(arg):


    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Directory containing multiple datasets or file name of a single dataset: /data/ or /data/sample.h5")
    parser.add_argument("--axis", nargs='?', type=str, default="0", help="Rotation axis location (pixel): 1024.0 (default 1/2 image horizontal size)")
    parser.add_argument("--bin", nargs='?', type=int, default=0, help="Reconstruction binning factor as power(2, choice) (default 0, no binning)")
    parser.add_argument("--method", nargs='?', type=str, default="gridrec", help="Reconstruction algorithm: astrasirt, gridrec, sirtfbp (default gridrec)")
    parser.add_argument("--type", nargs='?', type=str, default="slice", help="Reconstruction type: full, slice, try, phase (default slice)")
    parser.add_argument("--srs", nargs='?', type=int, default=10, help="+/- center search width (pixel): 10 (default 10). Search is in 0.5 pixel increments")
    parser.add_argument("--nsino", nargs='?', type=restricted_float, default=0.5, help="Location of the sinogram to reconstruct (0 top, 1 bottom): 0.5 (default 0.5)")
    parser.add_argument("--reverse",action="store_true", help="set when the data set was collected in reverse (180-0)")
    parser.add_argument("--auto",action="store_true", help="set to use autocenter, when set --axis value is ignored")
    parser.add_argument("--plot",action="store_true", help="set to plot try result")

    args = parser.parse_args()

    # Set path to the micro-CT data to reconstruct.
    variableDict['fname'] = args.fname
    variableDict['algorithm'] = args.method
    variableDict['rot_center'] = float(args.axis)
    variableDict['binning'] = int(args.bin)
    variableDict['nsino'] = float(args.nsino)
    variableDict['rec_type'] = args.type
    variableDict['center_search_width'] = args.srs
    variableDict['reverse'] = args.reverse
    variableDict['auto'] = args.auto
    variableDict['plot'] = args.plot

    # create logger
    home = str(pathlib.Path.home())
    logs_home = home + '/logs/'

    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)

    lfname = logs_home + 'rec_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log_lib.setup_logger(lfname)

    variableDict['logs_home'] = logs_home
    if os.path.isfile(variableDict['fname']):    

        log_lib.info("Reconstructing a single file")   
        # Set default rotation axis location
        if variableDict['rot_center'] == 0:
            if (variableDict['auto'] == True):
                variableDict['rot_center'] = find_rotation_axis(variableDict)
            else:    
                data_shape = get_dx_dims(variableDict['fname'], 'data')
                variableDict['rot_center'] =  data_shape[2]/2
        if variableDict['rec_type'] == "try":            
            rec_try(variableDict)
        elif variableDict['rec_type'] == "full":
            rec_full(variableDict)
        elif variableDict['rec_type'] == "phase":
            rec_phase(variableDict)
        else:
            rec_slice(variableDict)

    elif os.path.isdir(variableDict['fname']):
        log_lib.info("Reconstructing a folder containing multiple files")   
        # Add a trailing slash if missing
        top = os.path.join(variableDict['fname'], '')
        
        # Load the the rotation axis positions.
        jfname = top + "rotation_axis.json"
        
        dictionary = read_rot_centers(jfname)
            
        for key in dictionary:
            dict2 = dictionary[key]
            for h5fname in dict2:
                variableDict['rot_center'] = dict2[h5fname]
                fname = top + h5fname
                log_lib.info("Reconstructing %s" % h5fname)
                # Set default rotation axis location
                if variableDict['rot_center'] == 0:
                    data_shape = get_dx_dims(variableDict['fname'], 'data')
                    variableDict['rot_center'] =  data_shape[2]/2
                if variableDict['rec_type'] == "try":            
                    rec_try(variableDict)
                elif variableDict['rec_type'] == "full":
                    rec_full(variableDict)
                else:
                    rec_slice(variableDict)
    else:
        log_lib.info("Directory or File Name does not exist: %s" % variableDict['fname'])

if __name__ == "__main__":
    main(sys.argv[1:])

