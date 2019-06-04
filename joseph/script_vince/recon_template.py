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
#file_name = '/local/data/2018-11/Jakes/EW500um100mm_test1_0006.h5' # best center = 1291
#output_name = '/local/data/2018-11/Jakes/EW500um100mm_test1_0006_phase'
#
##file_name = '/local/data/2018-11/Jakes/EW500um_test1_0005.h5' # best center = 1271
##output_name = '/local/data/2018-11/Jakes/EW500um_test1_0005_phase/'
#
#file_name = '/local/data/2018-11/Jakes/EW500um50mm_test1_0007.h5' # best center = 1273
#output_name = '/local/data/2018-11/Jakes/EW500um50mm_test1_0007_phase/'
#
#file_name = '/local/data/2018-11/Jakes/EW500um50mm100ms_test1_0009.h5' # best center = 1273
#output_name = '/local/data/2018-11/Jakes/EW500um50mm100ms_test1_0009_no_phase_retrieval/'


file_name = '/run/media/tomo/Seagate Backup Plus Drive/2BM_2018-11/Jakes/distalThread_2_0070.h5' # best center = 1279
output_name = '/run/media/tomo/Seagate Backup Plus Drive/2BM_2018-11/Jakes/distalThread_2_0070/'

best_center = 1292
sino_start = 000; sino_end = 2160  #sino_start = 000; sino_end = 2160
flat_field_norm = True # 
flat_field_drift_corr = True # Correct the intensity drift
remove_rings = True 
phase_retrieval = False
medfilt_size = 0 # 0 or 1= no filtering; # 2= 2x2 kernel; 3= 3x3 kernel
binning = 0

sample_detector_distance = 10        # Propagation distance of the wavefront in cm
detector_pixel_size_x = 0.000065    # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4)
monochromator_energy = 24.9         # Energy of incident wave in keV
#alpha = 1e-02                       # Phase retrieval coeff.
#alpha = 1e-03                       # Phase retrieval coeff.
#alpha = 1e-01                       # Phase retrieval coeff
alpha = 1.5e-02                       # Phase retrieval coeff

medfilt3D_size = 0 # applied after reconstruction. 0 or 1= no filtering; # 2= 2x2x2 kernel; 3= 3x3x3 kernel
recon_algo = 'gridrec'
num_iter = 50 # for sirt-fbp or iterative methods
rec_filter = 'parzen' # 'sirtfbp', 'parzen', 'butterworth', 'none', etc
nChunks = 5 # number of rows divided by the number of chunks must be an integer

recon_1slice = False # True: reconstruct only 1 slice
test_sirtfbp_iter = False # True: recon_1slice needs to be True, then recon 1 slice with filters computed for different iterations
recon_full_vol = True # True: reconstruct the full volume
######################################################################################################################



######################################################################################################################
if output_name[-1] == '/':
    output_name = output_name[0:-1]
if ((recon_algo=='gridrec' or recon_algo=='fbp') and rec_filter!='sirtfbp'):
    output_name_2 = output_name + '_' + recon_algo + '_' + rec_filter + '/rec_' + recon_algo + '_' + rec_filter + '_slice'
else:
    output_name_2 = output_name + '_' + recon_algo + '_' + rec_filter + '_' + str(num_iter) + 'iter/rec_' + recon_algo + '_' + rec_filter + '_' + str(num_iter) + 'iter' + '_slice'


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

    if phase_retrieval:
        # phase retrieval
        prj = tomopy.prep.phase.retrieve_phase(prj,pixel_size=detector_pixel_size_x,dist=sample_detector_distance,energy=monochromator_energy,alpha=alpha,pad=True)


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
    if (recon_algo == 'gridrec' and rec_filter == 'sirtfbp'):
        if test_sirtfbp_iter:
            num_iter = [1, 2, 3]
    #            filter_dict = sirtfilter.getfilterfile(nCol, theta, num_iter, filter_dir='./')
            filter_dict = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
            for its in num_iter:
                output_name_2 = output_name + '_test_iter/'
                tomopy_filter = sirtfilter.convert_to_tomopy_filter(filter_dict[its], nCol)
                rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
                output_name_2 = output_name_2 + 'sirt_fbp_%iiter_slice_' % its
                dxchange.write_tiff_stack(rec, fname=output_name_2, start=sino_start, dtype='float32')
        else:
#            filter_file = sirtfilter.getfilterfile(nCol, theta, num_iter, filter_dir='./')
            sirtfbp_filter = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
            tomopy_filter = sirtfilter.convert_to_tomopy_filter(sirtfbp_filter, nCol)
    
            rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
    else:
        rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm=recon_algo, filter_name=rec_filter)
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

#        prj = prj[130:1175,:,:]
#        theta = theta[130:1175]

        # Pre-processing data
        prj = preprocess_data(prj, flat, dark, FF_norm=flat_field_norm, remove_rings = remove_rings, medfilt_size=medfilt_size, FF_drift_corr=flat_field_drift_corr, downspling=binning)

#        print('WATCH OUT!!!!!! Theta put manually line 225')
#        theta = tomopy.angles(691, -78, 96)

        # reconstruct
        ##########################################
        print('\n*** Reconstructing...')
        start_recon_time = time.time()
        nCol = prj.shape[2]
       
        if (recon_algo == 'gridrec' and rec_filter == 'sirtfbp'):
            sirtfbp_filter = sirtfilter.getfilter(nCol, theta, num_iter, filter_dir='./')
            tomopy_filter = sirtfilter.convert_to_tomopy_filter(sirtfbp_filter, nCol)
            
            rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm='gridrec', filter_name='custom2d', filter_par=tomopy_filter)
        else:
            rec = tomopy.recon(prj, theta, center=best_center/pow(2,binning), algorithm=recon_algo, filter_name=rec_filter)
#            rec = tomopy.recon(prj[0:4800, :, :].copy(), theta[0:4800].copy(), center=best_center/pow(2,binning), algorithm='osem', num_block=200, num_iter=2)
    
        print('   Slice reconstruction done in %0.3f min' % ((time.time() - start_recon_time)/60))
        print(output_name_2)

        # Postprocessing reconstruction:
        rec = postprocess_data(rec, medfilt3D_size = medfilt3D_size)

        # Write data as stack of TIFs.
        dxchange.write_tiff_stack(rec, fname=output_name_2, start=strt, dtype='float32')
        strt += prj.shape[1]

    print(" *** TOTAL RECONSTRUCTION TIME: %i min" % ((time.time() - start_time)/60))

