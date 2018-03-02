# -*- coding: utf-8 -*-
# Recon a single slice for testing.
import tomopy
import numpy as np
from scipy import ndimage
import h5py
import matplotlib.pylab as plt

##################################### Inputs ##########################################################
file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_3kbar_.h5' # best_center = 1232
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_3kbar_recon/Ce6Al4_3kbar_recon_'
best_center = 1232; slice_first = 740; slice_last = 1700; miss_angles = [141,226]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_5P7kbar_.h5' # best_center = 1321
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_5P7kbar_recon/CCe6Al4_5P7kbar_recon_'
best_center = 1321; slice_first = 1000; slice_last = 1440; miss_angles = [141,228]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_8P59GPa_.h5' # best_center = 1219
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_8P59GPa_recon/Ce6Al4_8P59GPa_recon_'
best_center = 1219; slice_first = 550; slice_last = 1370; miss_angles = [147,233]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_13P37GPa_.h5' # best_center = 1286
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_13P37GPa_recon/Ce6Al4_13P37GPa_recon_'
best_center = 1286; slice_first = 740; slice_last = 1500; miss_angles = [142,227]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_17p44GPa_.h5' # best_center = 
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_17p44GPa_recon/Ce6Al4_17p44GPa_recon_'
best_center = 1292; slice_first = 620; slice_last = 1320; miss_angles = [140,226]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_19GPa_decrease_.h5' # best_center = 
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_19GPa_decrease_recon/Ce6Al4_19GPa_decrease_recon_'
best_center = 1116; slice_first = 800; slice_last = 1200; miss_angles = [140,225]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_20kbar_.h5' # best_center = 1314
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_20kbar_recon/Ce6Al4_20kbar_recon_'
best_center = 1314; slice_first = 610; slice_last = 1500; miss_angles = [71,113]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_21p39GPa_.h5' # best_center = 1140
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_21p39GPa_recon_crop_filt/Ce6Al4_21p39GPa_recon_'
best_center = 1140; slice_first = 610; slice_last = 1200; miss_angles = [140,226]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_26p17GPa_.h5' # best_center = 1124
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_26p17GPa_recon_crop_filt/Ce6Al4_26p17GPa_recon_'
best_center = 1124; slice_first = 740; slice_last = 1270; miss_angles = [140,227]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_29P5GPa_decrease_.h5' # best_center = 1338
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_29P5GPa_decrease_recon_crop_filt/Ce6Al4_29P5GPa_decrease_recon_'
best_center = 1338; slice_first = 760; slice_last = 1180; miss_angles = [140,227]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_33p07GPa_.h5' # best_center = 
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_33p07GPa_recon_crop_filt/Ce6Al4_33p07GPa_recon_'
best_center = 1232; slice_first = 710; slice_last = 1210; miss_angles = [140,227]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_41p88GPa_.h5' # best_center = 1292
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_41p88GPa_recon_crop_filt/Ce6Al4_41p88GPa_recon_'
best_center = 1292; slice_first = 700; slice_last = 1180; miss_angles = [138,225]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_47p89GPa_.h5' # best_center = 1114
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_47p89GPa_recon_crop_filt/Ce6Al4_47p89GPa_recon_'
best_center = 1114; slice_first = 740; slice_last = 1210; miss_angles = [141,228]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_54p73GPa_.h5' # best_center = 1352
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_54p73GPa_recon_crop_filt/Ce6Al4_54p73GPa_recon_'
best_center = 1352; slice_first = 750; slice_last = 1230; miss_angles = [138, 224]

file_name = '/local/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_59GPa_.h5' # best_center = 1352
output_name = '/local/prom04/vdeandrade/dataraid/2014_11/2014_11_Haozhe/Ce6Al4_59GPa_crop_filt/Ce6Al4_59GPa_recon_'
best_center = 1352; slice_first = 630; slice_last = 1100; miss_angles = [138, 224]

medfilt_size = 2
perform_norm = 1 # 1 or 0 to apply or not a flat-field correction
remove_stripe1 = 0 # 1 or 0 to apply or not the stripe removal algo based on wavelet transform
remove_stripe2 = 1 # 1 or 0 to apply or not the stripe removal algo based on wavelet transform
remove_stripe4 = 0 # 1 or 0 to apply or not the stripe removal algo based on wavelet transform
#stripe_lvl = 8 # level for the stripe removal algo
#sig = 8 # sigma for the stripe removal algo
#Wname = 42 #  # wavelet shape for the stripe removal algo
drift_correct = 1
level = 1 # 2^level binning
RingW = 10 # for ring artifact removal M. Rivers algo
chunk = 6 # number of data chunks for the reconstruction
ExchangeRank = 0 # exchange rank corresponding to the dataset
########################################################################################################


print '\n#### Processing '+file_name

#### for 1 slice reconstruction:
#-------------------------------
if 1:
#    slice_first = 1000
#    slice_last = 1400
    # Read HDF5 file.
    data, white, dark, theta = tomopy.xtomo_reader(file_name,
                                                   exchange_rank = ExchangeRank,
                                                   slices_start=slice_first,
                                                   slices_end=slice_last)

    # Manage the missing angles:
    data_size = np.shape(data)
    theta = np.linspace(0,180,data_size[0])
    data = np.concatenate((data[0:miss_angles[0],:,:], data[miss_angles[1]+1:-1,:,:]), axis=0)
    theta = np.concatenate((theta[0:miss_angles[0]], theta[miss_angles[1]+1:-1]))


    # Xtomo object creation and pipeline of methods.
#    d = tomopy.xtomo_dataset(log='debug')
    d = tomopy.xtomo_dataset(log='debug')
    d.dataset(data, white, dark, theta)
    if perform_norm: d.normalize() # flat & dark field correction
    if drift_correct: d.correct_drift()
    d.median_filter(size=medfilt_size, axis=0) # Apply a median filter in the projection plane
#    if remove_stripe: d.stripe_removal(level=stripe_lvl, sigma=sig, wname=Wname)
#    d.stripe_removal_horiz(level=stripe_lvl, sigma=sig, wname=Wname)
#    z = 3
#    eng = 31
#    pxl = 0.325e-4
#    rat = 5e-03
#    rat = 1e-03
#    d.phase_retrieval(dist=z, energy=eng, pixel_size=pxl, alpha=rat,padding=True)
#    if remove_stripe4:
#        mask_bad_val = crap_mask(white, 200, 40)
#        d.stripe_removal4(mask_bad_val)
    if remove_stripe2: d.stripe_removal2()
#    if remove_stripe: d.stripe_removal(level=stripe_lvl, sigma=sig, wname=Wname)
    d.downsample2d(level=level) # apply binning on the data
    if 1:
        if not best_center: d.optimize_center()
        else: d.center=best_center/pow(2,level) # Manage the rotation center
        d.gridrec(ringWidth=RingW) # Run the reconstruction
        d.apply_mask(ratio=1)

        # Write data as stack of TIFs.
        tomopy.xtomo_writer(d.data_recon, output_name, 
                            axis=0,
                            x_start=slice_first)

#### for the whole volume reconstruction
if 0:
    f = h5py.File(file_name, "r"); nProj, nslices, nCol = f["/exchange/data"].shape
    nslices_per_chunk = nslices/chunk

    for iChunk in range(0,chunk):
        print '\n  -- chunk # %i' % (iChunk+1)
        slice_first = nslices_per_chunk*iChunk 
        slice_last = nslices_per_chunk*(iChunk+1)
        
        # Read HDF5 file.
        data, white, dark, theta = tomopy.xtomo_reader(file_name,
                                                       exchange_rank = ExchangeRank,
                                                       slices_start=slice_first,
                                                       slices_end=slice_last)
        
        # Manage the missing angles:
        data_size = np.shape(data)
        theta = np.linspace(0,180,data_size[0])
        data = np.concatenate((data[0:miss_angles[0],:,:], data[miss_angles[1]+1:-1,:,:]), axis=0)
        theta = np.concatenate((theta[0:miss_angles[0]], theta[miss_angles[1]+1:-1]))

        print '\n  -- 1st & last slice: %i, %i' % (slice_first, slice_last)
        
        # Xtomo object creation and pipeline of methods.
        d = tomopy.xtomo_dataset(log='debug')
        d.dataset(data, white, dark, theta)
        if perform_norm: d.normalize() # flat & dark field correction
        if drift_correct: d.correct_drift()
        d.median_filter(size=medfilt_size, axis=0)
        if remove_stripe1:
            d.stripe_removal_horiz(level=stripe_lvl, sigma=sig, wname=Wname)
#        d.stripe_removal3(40, 1)
#        if remove_stripe: d.stripe_removal(level=stripe_lvl, sigma=sig, wname=Wname)
        if remove_stripe4:
            mask_bad_val = crap_mask(white, 200, 40)
            d.stripe_removal4(mask_bad_val)
        if remove_stripe2: d.stripe_removal2()

#        d.downsample2d(level=level)
        d.downsample3d(level=level)

        if 0:
            ## Save modified data into the hdf5 file:
            data = d.data
            File = h5py.File(file_name, "r+")
            dset = File.create_dataset("/exchange1/data", np.shape(data))
            dset = File['/exchange1/data']
            dset[...] = data
            File.close()
        if 0:
            tomopy.xtomo_writer(d.data, output_name, 
                                axis=1,
                                x_start=slice_first)
        if 1:
            if not best_center: d.optimize_center()
            else: d.center=best_center/pow(2,level) # Manage the rotation center
            d.gridrec(ringWidth=RingW) # Run the reconstruction
            d.apply_mask(ratio=1)
            # Write data as stack of TIFs.
#            tomopy.xtomo_writer(d.data_recon, output_name, 
#                                axis=0,dtype='uint16',
#                                x_start=slice_first)
            tomopy.xtomo_writer(d.data_recon, output_name, 
                                axis=0,
                                x_start=slice_first)



