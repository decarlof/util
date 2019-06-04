import tomopy
import dxchange
import astra
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc, ndimage
import h5py
import sirtfilter


##################################### Inputs #########################################################################
file_name = '/local/dataraid/2018-06/DeAndrade/2018-06-19/brain_petrapoxy/Brain_Petrapoxy_day2_4800prj_720deg_166.h5' 

binning = 1
medfilt_size = 1
nProj = 4841
####################################################################################################################

if 0:
    #prj, flat, dark, theta = dxchange.read_aps_32id(file_name, proj=(nProj, nProj+1))
    prj, flat, dark, theta = dxchange.read_aps_32id(file_name, proj=(0, nProj+1, 1210)) # open proj from 0 to 720 deg with 180deg step --> 5 proj
    prj = tomopy.normalize(prj, flat, dark)
    
    prj = tomopy.misc.corr.remove_neg(prj, val=0.000)
    prj = tomopy.misc.corr.remove_nan(prj, val=0.000)
    prj[np.where(prj == np.inf)] = 0.000
    prj[np.where(prj > 1.0)] = 1
    prj = tomopy.downsample(prj, level=binning)
    prj = tomopy.downsample(prj, level=binning, axis=1)
    prj = ndimage.median_filter(prj,footprint=np.ones((1, medfilt_size, medfilt_size)))
    
    #prj = np.squeeze(prj); avg = np.mean(prj); std = np.std(prj)
    #plt.imshow(prj, cmap='gray', aspect="auto", interpolation='none', vmin=avg-3*std, vmax=avg+3*std), plt.colorbar(), plt.show()
    ##plt.imshow(prj, cmap='gray', aspect="auto", interpolation='none', vmin=0, vmax=0.1), plt.colorbar(), plt.show()
    
    dxchange.write_tiff(prj, fname='/local/dataraid/2018-06/DeAndrade/2018-06-19/brain_petrapoxy/tmp/data', dtype='float32', overwrite=False)

sino_st = 750
sino_end = 1250

if 0:
    prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(sino_st,sino_end,1), proj=(0, 1210, 1)) # open proj from 0 to 720 deg with 180deg step --> 5 proj
    prj = tomopy.normalize(prj, flat, dark)

    print('\n*** Shape of the data:'+str(np.shape(prj)))
    prj = tomopy.misc.corr.remove_neg(prj, val=0.000)
    prj = tomopy.misc.corr.remove_nan(prj, val=0.000)
    prj[np.where(prj == np.inf)] = 0.000
    prj[np.where(prj > 1.0)] = 1
    prj = tomopy.downsample(prj.copy(), level=binning)
    prj = tomopy.downsample(prj.copy(), level=binning, axis=1)
    print('\n*** Shape of the data:'+str(np.shape(prj)))
    dxchange.write_tiff_stack(prj, fname='/local/dataraid/2018-06/DeAndrade/2018-06-19/brain_petrapoxy/rot1/prj', dtype='float32', axis=0, digit=4, start=0, overwrite=False)

if 0:
    prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(sino_st,sino_end,1), proj=(1210, 1210+1210, 1)) # open proj from 0 to 720 deg with 180deg step --> 5 proj
    prj = tomopy.normalize(prj, flat, dark)

    prj = tomopy.misc.corr.remove_neg(prj, val=0.000)
    prj = tomopy.misc.corr.remove_nan(prj, val=0.000)
    prj[np.where(prj == np.inf)] = 0.000
    prj[np.where(prj > 1.0)] = 1
    prj = tomopy.downsample(prj.copy(), level=binning)
    prj = tomopy.downsample(prj.copy(), level=binning, axis=1)
    dxchange.write_tiff_stack(prj, fname='/local/dataraid/2018-06/DeAndrade/2018-06-19/brain_petrapoxy/rot2/prj', dtype='float32', axis=0, digit=4, start=0, overwrite=False)

if 0:
    prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(sino_st,sino_end,1), proj=(2420, 2420+1210, 1)) # open proj from 0 to 720 deg with 180deg step --> 5 proj
    prj = tomopy.normalize(prj, flat, dark)

    prj = tomopy.misc.corr.remove_neg(prj, val=0.000)
    prj = tomopy.misc.corr.remove_nan(prj, val=0.000)
    prj[np.where(prj == np.inf)] = 0.000
    prj[np.where(prj > 1.0)] = 1
    prj = tomopy.downsample(prj.copy(), level=binning)
    prj = tomopy.downsample(prj.copy(), level=binning, axis=1)
    dxchange.write_tiff_stack(prj, fname='/local/dataraid/2018-06/DeAndrade/2018-06-19/brain_petrapoxy/rot3/prj', dtype='float32', axis=0, digit=4, start=0, overwrite=False)

if 1:
    prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(sino_st,sino_end,1), proj=(3630, 3630+1210, 1)) # open proj from 0 to 720 deg with 180deg step --> 5 proj
    prj = tomopy.normalize(prj, flat, dark)

    prj = tomopy.misc.corr.remove_neg(prj, val=0.000)
    prj = tomopy.misc.corr.remove_nan(prj, val=0.000)
    prj[np.where(prj == np.inf)] = 0.000
    prj[np.where(prj > 1.0)] = 1
    prj = tomopy.downsample(prj.copy(), level=binning)
    prj = tomopy.downsample(prj.copy(), level=binning, axis=1)
    dxchange.write_tiff_stack(prj, fname='/local/dataraid/2018-06/DeAndrade/2018-06-19/brain_petrapoxy/rot4/prj', dtype='float32', axis=0, digit=4, start=0, overwrite=False)

