# -*- coding: utf-8 -*-
# Utility to find center of rotation.
import tomopy
import dxchange
import numpy as np
import h5py
import matplotlib.pyplot as plt

# Inputs:
#----------------------------------------------------------------------------------
input_path='/local/data/2018-11/Jakes/'
#file_string = 'EW500um_test1_0005' # best center = 1271
#file_string = 'EW500um100mm_test1_0006' # best center = 1291
#file_string = 'EW500um50mm_test1_0007' # best center = 1273
#file_string = 'EW500um50mm100ms_test1_0009' # best center = 1273
#file_string = 'EW1000um0RH_1_0013' # best center = 1279
#file_string = 'LW1000um0RH_1_0014' # best center = 1282
#file_string = 'EW50um0RH_1_0019' # best center = 1291
#file_string = 'LW50um0RH_1_0020' # best center = 1294
#file_string = 'EW500um0RH_1_0015' # best center = 1283
#file_string = 'LW500um0RH_1_0016' # best center = 1293
#file_string = 'EW150um0RH_1_0017' # best center = 1282
#file_string = 'LW150um0RH_1_0018' # best center = 1284
#file_string = 'EW50um0RH_1_0019' # best center = 1293
#file_string = 'LW50um0RH_1_0020' # best center = 1293
#file_string = 'EW1000um0RH_2_0021' # best center = 1281
#file_string = 'LW1000um0RH_2_0022' # best center = 
#file_string = 'EW500um0RH_2_0023' # best center = 
#file_string = 'LW500um0RH_2_0024' # best center = 
#file_string = 'LW500um0RH_2_0025' # best center = 
#file_string = 'EW150um0RH_2_0026' # best center = 
#file_string = 'LW150um0RH_2_0027' # best center = 
#file_string = 'EW50um0RH_2_0028' # best center = 
#file_string = 'LW50um0RH_2_0029' # best center = 
#file_string = 'EW1000um0RH_3_0030' # best center = 
#file_string = 'LW1000um0RH_3_0031' # best center = 
#file_string = 'EW500um0RH_3_0032' # best center = 
#file_string = 'LW500um0RH_3_0033' # best center = 
#file_string = 'EW150um0RH_3_0034' # best center = 
#file_string = 'LW150um0RH_3_0035' # best center = 
#file_string = 'EW50um0RH_3_0036' # best center = 
#file_string = 'LW50um0RH_3_0037' # best center = 
#file_string = 'EW1000um33RH_1_0038' # best center = 
#file_string = 'LW1000um33RH_1_0039' # best center = 
#file_string = 'EW500um33RH_1_0040' # best center = 
#file_string = 'LW500um33RH_1_0041' # best center = 
#file_string = 'EW150um33RH_1_0042' # best center = 
#file_string = 'LW150um33RH_1_0043' # best center = 
#file_string = 'EW50um33RH_1_0044' # best center = 1298
#file_string = 'LW50um33RH_1_0045' # best center = 
#file_string = 'EW1000um33RH_2_0046' # best center = 
#file_string = 'LW1000um33RH_2_0047' # best center = 
#file_string = 'EW500um33RH_2_0048' # best center = 
#file_string = 'LW500um33RH_2_0049' # best center = 
#file_string = 'EW150um33RH_2_0050' # best center = 
#file_string = 'LW150um33RH_2_0051' # best center = 
#file_string = 'EW50um33RH_2_0052' # best center = 
#file_string = 'LW50um33RH_2_0053' # best center = 

#file_string = 'LW50um33RH_3_0062' # best center = 


#file_string = 'proximalThread_1_0066' # best center = 1288  byssus
#file_string = 'proximalThread_2_0067' # best center = 1295
#file_string = 'proximalThread_3_0068' # best center = 1292
#file_string = 'distalThread_1_0069' # best center = 1291
#file_string = 'distalThread_2_0070' # best center = 1292
#file_string = 'distalThread_3_0071' # best center = 


file_string = 'EW50um75RH_1_0078' # best center = 1294


#file_string = 'LW50um33RH_2_0053' # best center = 
#file_string = 'LW50um33RH_2_0053' # best center = 
#file_string = 'LW50um33RH_2_0053' # best center = 
#file_string = 'LW50um33RH_2_0053' # best center = 
#file_string = 'LW50um33RH_2_0053' # best center = 
#file_string = 'LW50um33RH_2_0053' # best center = 


output_path = '/local/data/2018-11/Jakes/center/'

slice_no = 1024

Center_st =  1100 
Center_end = 1400
medfilt_size = 1
level = 1 # 2^level binning

sample_detector_distance = 10        # Propagation distance of the wavefront in cm
detector_pixel_size_x = 0.000065    # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
monochromator_energy = 24.9         # Energy of incident wave in keV
alpha = 1e-02                       # Phase retrieval coeff.


ExchangeRank = 0
auto_center = False
debug = 1
#----------------------------------------------------------------------------------
file_name= input_path+file_string+'.h5'
N_recon = Center_end - Center_st

#prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(slice_no, slice_no+1))
prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(slice_no, slice_no+1))

# Read theta from the dataset:
#File = h5py.File(file_name, "r"); dset_theta = File["/exchange/theta"]; theta = dset_theta[...]; theta = theta*np.pi/180
#prj = prj[130:1175,:,:]
#theta = theta[130:1175]

#theta = tomopy.angles(691, -78, 96)
if debug:
    print('## Debug: after reading data:')
    print('\n** Shape of the data:'+str(np.shape(prj)))
    print('** Shape of theta:'+str(np.shape(theta)))
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))

prj = tomopy.normalize(prj, flat, dark)
print('\n** Flat field correction done!')

if debug:
    print('## Debug: after normalization:')
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))

prj = tomopy.minus_log(prj)
print('\n** minus log applied!')

if debug:
    print('## Debug: after minus log:')
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))

prj = tomopy.misc.corr.remove_neg(prj, val=0.001)
prj = tomopy.misc.corr.remove_nan(prj, val=0.001)
prj[np.where(prj == np.inf)] = 0.001

if debug:
    print('## Debug: after cleaning bad values:')
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))

prj = tomopy.remove_stripe_ti(prj,4)
print('\n** Stripe removal done!')
if debug:
    print('## Debug: after remove_stripe:')
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))

# phase retrieval
#data = tomopy.prep.phase.retrieve_phase(prj,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)


prj = tomopy.median_filter(prj,size=medfilt_size)
print('\n** Median filter done!')
if debug:
    print('## Debug: after nedian filter:')
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))


if level>0:
    prj = tomopy.downsample(prj, level=level)
    print('\n** Down sampling done!\n')
if debug:
    print('## Debug: after down sampling:')
    print('\n** Min and max val in prj before recon: %0.5f, %0.3f'  % (np.min(prj), np.max(prj)))

if auto_center == False:

    tomopy.write_center(prj,theta,dpath=output_path,cen_range=[Center_st/pow(2,level),Center_end/pow(2,level),((Center_end - Center_st)/float(N_recon))/pow(2,level)])

else:
    rot_axis = tomopy.find_center_vo(prj)
    rot_axis = rot_axis * pow(2,level)
    print('*** Rotation center: %0.2f' % rot_axis)
    rec = tomopy.recon(prj, theta, center=rot_axis/pow(2,level), algorithm='gridrec', filter_name='parzen')
    rec=np.squeeze(rec)
    plt.figure()
    plt.imshow(rec, cmap='gray', aspect="auto", interpolation='none')
    plt.colorbar(), plt.title('Rotation center: %0.2f' % rot_axis), plt.show()