import tomopy
import dxchange
import astra
import time
import numpy as np
from scipy import misc, ndimage
import h5py
import sirtfilter
#import medfiltmp

##################################### Inputs #########################################################################
file_name = '/local/data/2018-11/Jakes/EW1000um0RH_1_0013.h5' # best center = 1273
output_name = '/local/data/2018-11/Jakes/EW1000um0RH_1_0013/'

best_center = 1279
sino_start = 0; sino_end = 100 #sino_start = 0; sino_end = 2048
flat_field_norm = True # 
flat_field_drift_corr = True # Correct the intensity drift
remove_rings = True 
medfilt_size = 1 # 0 or 1= no filtering; # 2= 2x2 kernel; 3= 3x3 kernel
binning = 0
medfilt3D_size = 0 # applied after reconstruction. 0 or 1= no filtering; # 2= 2x2x2 kernel; 3= 3x3x3 kernel\
# https://astra-toolbox.readthedocs.io/en/latest/docs/index.html
recon_algo = 'CGLS_CUDA' # 'SIRT_CUDA', 'CGLS_CUDA', 'EM_CUDA' 
num_iter = 25 # for sirt-fbp or iterative methods1
nChunks = 100 # number of rows divided by the number of chunks must be an integer

recon_1slice = False # True: reconstruct only 1 slice
test_sirtfbp_iter = False # True: recon_1slice needs to be True, then recon 1 slice with filters computed for different iterations
recon_full_vol = True# True: reconstruct the full volume
######################################################################################################################



######################################################################################################################
if output_name[-1] == '/':
    output_name = output_name[0:-1]

if recon_1slice == True:
    output_name_2 = output_name + '_' + recon_algo + '/rec_' + recon_algo + '_' + ('%0004iiter' % num_iter) + '_slice'
else:
    output_name_2 = output_name + '_' + recon_algo + '_' + str(num_iter) + 'iter/rec_' + recon_algo + '_' + str(num_iter) + 'iter' + '_slice'


def preprocess_data(prj, flat, dark, FF_norm=flat_field_norm, remove_rings = remove_rings, medfilt_size=medfilt_size, FF_drift_corr=flat_field_drift_corr, downspling=binning):

    if FF_norm:
        # normalize the prj
        print('\n*** Applying flat field correction:') 
        start_norm_time = time.time()
        prj = tomopy.normalize(prj, flat, dark)
        print('   done in %0.3f min' % ((time.time() - start_norm_time)/60))

    if FF_drift_corr:
        print('\n*** Applying flat field drift correction:')
        start_norm_bg_time = time.time()
        prj = tomopy.normalize_bg(prj, air=100)
        print('   done in %0.3f min' % ((time.time() - start_norm_bg_time)/60))

    # Applying -log
    print('\n*** Applying -log:') 
    start_log_time = time.time()
    prj = tomopy.minus_log(prj)
    print('   done in %0.3f min' % ((time.time() - start_log_time)/60))

    prj = tomopy.misc.corr.remove_neg(prj, val=0.000)
    prj = tomopy.misc.corr.remove_nan(prj, val=0.000)
    prj[np.where(prj == np.inf)] = 0.000
#    prj[np.where(prj == 0)] = 0.000
    print('\n*** Min and max val in prj before recon: %0.3f, %0.3f'  % (np.min(prj), np.max(prj)))

    if remove_rings:
        # remove ring artefacts
        tmp = prj[-1,:,:] # use to fixe the bug of remove_stripe_ti
        print('\n*** Applying ring removal algo:') 
        start_ring_time = time.time()
        prj = tomopy.remove_stripe_ti(prj,2)
    #    prj = tomopy.remove_stripe_sf(prj,10); prj = tomopy.misc.corr.remove_neg(prj, val=0.000) # remove the neg values coming from remove_stripe_sf
        print('   done in %0.3f min' % ((time.time() - start_ring_time)/60))
        prj[-1,:,:] = tmp # fixe the bug of remove_stripe_ti

    # Filtering data with 2D median filter before downsampling and recon 
    if medfilt_size>1:
        start_filter_time = time.time()
        print('\n*** Applying median filter')
        #prj = tomopy.median_filter(prj,size=1)
        prj = ndimage.median_filter(prj,footprint=np.ones((1, medfilt_size, medfilt_size)))
        print('   done in %0.3f min' % ((time.time() - start_filter_time)/60))

    # Downsampling data:
    if downspling>0:
        print('\n** Applying downsampling')
        start_down_time = time.time()
        prj = tomopy.downsample(prj, level=binning)
        prj = tomopy.downsample(prj, level=binning, axis=1)
        print('   done in %0.3f min' % ((time.time() - start_down_time)/60))
        
    print('\n*** Shape of the data:'+str(np.shape(prj)))
    print('      Dimension of theta:'+str(np.shape(theta)))

    return prj
    
def postprocess_data(rec, medfilt3D_size = medfilt3D_size):
    if medfilt3D_size>1:
        start_filter_time = time.time()
        print('\n** Applying post 3D Median filter, slow!!!')
        rec = ndimage.median_filter(rec,footprint=np.ones((medfilt3D_size, medfilt3D_size, medfilt3D_size)))
        #            rec = medfiltmp.median_filter(rec,footprint=np.ones((filter_size, filter_size, filter_size)))												
        print('   done in %0.3f min' % ((time.time() - start_filter_time)/60))
    return rec


        ##########################################################################
        #                        1 Slice recontruction                           #
        ##########################################################################

if recon_1slice:
    start_time = time.time()
    print('\n#### Processing '+ file_name)
    f = h5py.File(file_name, "r");
    sino_start = int(np.round(f["/exchange/data"].shape[1]/2))
    print('\n########## Slice chosen manually\n')
#    sino_start = 776
    sino_end   = int(sino_start + pow(2,binning))
    
    print("** Test reconstruction of slice [%d]" % sino_start)

    # Read HDF5 file.
    print('\n*** Reading data:') 
    start_reading_time = time.time()								
    try:
        prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(sino_start, sino_end))
        print(prj.shape, flat.shape, dark.shape)
    except:
        prj, flat, dark = dxchange.read_aps_32id(file_name, sino=(sino_start, sino_end))
        print(prj.shape, flat.shape, dark.shape)
        f = h5py.File(file_name, "r"); dset_theta = f["/exchange/theta"]; theta = dset_theta[...]; theta = theta*np.pi/180
    print("   Reading time: %0.3f min" % ((time.time() - start_reading_time)/60))
    
    # Pre-processing data
    prj = preprocess_data(prj, flat, dark, FF_norm=flat_field_norm, remove_rings = remove_rings, medfilt_size=medfilt_size, FF_drift_corr=flat_field_drift_corr, downspling=binning)


    # reconstruct
    ##########################################
    print('\n*** Reconstructing...')
    start_recon_time = time.time()
    nCol = prj.shape[2]

    extra_options ={'MinConstraint':0}
#    extra_options ={}   
    options = {'proj_type':'cuda', 'method':recon_algo, 'num_iter':num_iter, 'extra_options':extra_options}
    rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm=tomopy.astra, options=options)       
 
    print('   Slice reconstruction done in %0.3f min' % ((time.time() - start_recon_time)/60))
    print(output_name_2)

    # Postprocessing reconstruction:
    rec = postprocess_data(rec, medfilt3D_size = medfilt3D_size)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname=output_name_2, start=sino_start, dtype='float32')

    print(" *** TOTAL RECONSTRUCTION TIME: %i s" % ((time.time() - start_time)))
    
    
            ##########################################################################
            #                      Full volume reconstruction                        #
            ##########################################################################

if recon_full_vol:
    start_time = time.time()
    print('\n#### Processing '+ file_name)

    if recon_algo == 'sirtfbp':
        nCol = prj.shape[2]
        filter_file = sirtfilter.getfilterfile(nCol, theta, num_iter, filter_dir='./')
        astra.plugin.register(sirtfilter.astra_plugin)
        options = {'method':'SIRT-FBP', 'proj_type':'cuda'}
        options['extra_options'] = {'filter_file':filter_file}
    

    
    nSino_per_chunk = (sino_end - sino_start)/nChunks
    print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, nChunks, nSino_per_chunk))
    print("Sinogram / chunk: %i" % nSino_per_chunk)
    strt = 0
    for iChunk in range(0,nChunks):
        print('\n   -- chunk # %i\n' % (iChunk+1))
        sino_chunk_start = np.int(sino_start + nSino_per_chunk*iChunk)
        sino_chunk_end = np.int(sino_start + nSino_per_chunk*(iChunk+1))
        print('\n   --------> [%i, %i]\n' % (sino_chunk_start, sino_chunk_end))
        
        if sino_chunk_end > sino_end: 
            break
        
        # Reading data
        print('\n*** Reading data:') 
        start_reading_time = time.time()								
        try:
            prj, flat, dark, theta = dxchange.read_aps_32id(file_name, sino=(sino_chunk_start, sino_chunk_end))
            print(prj.shape, flat.shape, dark.shape)
        except:
            prj, flat, dark = dxchange.read_aps_32id(file_name, sino=(sino_chunk_start, sino_chunk_end))
            print(prj.shape, flat.shape, dark.shape)
            f = h5py.File(file_name, "r"); dset_theta = f["/exchange/theta"]; theta = dset_theta[...]; theta = theta*np.pi/180
        print("   Reading time: %0.3f min" % ((time.time() - start_reading_time)/60))

        # Pre-processing data
        prj = preprocess_data(prj, flat, dark, FF_norm=flat_field_norm, remove_rings = remove_rings, medfilt_size=medfilt_size, FF_drift_corr=flat_field_drift_corr, downspling=binning)

#        print('WATCH OUT!!!!!! Theta put manually line 225')
#        theta = tomopy.angles(691, -78, 96)

        # reconstruct
        ##########################################
        print('\n*** Reconstructing...')
        start_recon_time = time.time()
        nCol = prj.shape[2]

        extra_options ={'MinConstraint':0}
#        extra_options ={}   
        options = {'proj_type':'cuda', 'method':recon_algo, 'num_iter':num_iter, 'extra_options':extra_options}
        rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm=tomopy.astra, options=options)       
     
        print('   Slice reconstruction done in %0.3f min' % ((time.time() - start_recon_time)/60))
        print(output_name_2)

        # Postprocessing reconstruction:
        rec = postprocess_data(rec, medfilt3D_size = medfilt3D_size)

        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname=output_name_2, start=strt, dtype='float32')
        strt += prj.shape[1]

    print(" *** TOTAL RECONSTRUCTION TIME: %i min" % ((time.time() - start_time)/60))

