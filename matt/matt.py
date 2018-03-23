#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TomoPy script to reconstruct Matt's data in chuck of sinogrmas. 
This function is for reconstructing large data on limited memory computers.
If you have limited memory increase chunk. 
Change dfolder to match your data top directory

"""


import tomopy
import dxchange
import time
import numpy as np
from scipy import misc, ndimage
from scipy.interpolate import interp1d
from skimage import restoration
import matplotlib.pyplot as plt
import h5py


dfolder = '/local/dataraid/matt/'


sample_detector_distance  = 60      # Propagation distance of the wavefront in cm
energy = 120                        # Energy of incident wave in keV
detector_pixel_size_x = 2.8e-4      # Detector pixel size in cm (5x: 1.17e-4, 2X: 2.93e-4) 
alpha = 5e-3                        # Phase retrieval coeff.

def reconstruct(sname, rot_center, ovlpfind, s_start, s_end):
    fname = dfolder + sname + '.h5'
    print (fname)
    start = s_start  
    end =   s_end
    chunks = 24 
    num_sino = (end - start) // chunks
    for m in range(chunks):
        sino_start = start + num_sino * m
        sino_end = start + num_sino * (m + 1)
        start_read_time = time.time()
        proj, flat, dark, thetat = dxchange.read_aps_2bm(fname, sino=(sino_start, sino_end))
        print('   done read in %0.1f min' % ((time.time() - start_read_time)/60))
        dark = proj[9001:9002]
        flat = proj[0:1]
        proj = proj[1:9000]
        theta = tomopy.angles(proj.shape[0], 0., 360.)
        proj = tomopy.sino_360_to_180(proj, overlap=ovlpfind, rotation='right')
        proj = tomopy.remove_outlier(proj, dif=0.4)
        proj = tomopy.normalize_bg(proj, air=10)
        proj = tomopy.minus_log(proj)
        center = rot_center
        start_ring_time = time.time()
        proj = tomopy.remove_stripe_fw(proj, wname='sym5', sigma=4, pad=False)
        proj = tomopy.remove_stripe_sf(proj, size=3)
        print('   done pre-process in %0.1f min' % ((time.time() - start_ring_time)/60))
        start_phase_time = time.time()
        proj = tomopy.retrieve_phase(proj, pixel_size=detector_pixel_size_x, dist=sample_detector_distance, energy=energy, alpha=alpha, pad=True, ncore=None, nchunk=None)
        print('   done phase retrieval in %0.1f min' % ((time.time() - start_phase_time)/60))
        start_recon_time = time.time()
        rec = tomopy.recon(proj, theta, center=center, algorithm='gridrec', filter_name='ramalk')
        tomopy.circ_mask(rec, axis=0, ratio=0.95)
        print ("Reconstructed", rec.shape)
        dxchange.write_tiff_stack(rec, fname = dfolder + '/' + sname + '/' + sname, overwrite=True, start=sino_start)
        print('   Chunk reconstruction done in %0.1f min' % ((time.time() - start_recon_time)/60))
    print ("Done!")


# ###################################################################################################
sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_001'
ovlpfind = 680
rot_center = 1580
reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_002'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_003'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_004'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_005'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_006'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_007'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_008'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_98_120keV_4mmCu_600mm_9000_009'
# ovlpfind = 680
# rot_center = 1580
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_001'
# ovlpfind = 683
# rot_center = 1578
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_002'
# ovlpfind = 683
# rot_center = 1578
# reconstruct(sname, rot_center, ovlpfind, 1, 1200)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_003'
# ovlpfind = 683
# rot_center  = 1578
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_004'
# ovlpfind = 683
# rot_center  = 1578
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_005'
# ovlpfind = 683
# rot_center  = 1578
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_006'
# ovlpfind = 683
# rot_center  = 1578
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_74_120keV_4mmCu_600mm_9000_007'
# ovlpfind = 683
# rot_center  = 1578
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_001'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_002'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_003'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_004'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_005'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_006'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_007'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_008'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_009'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_010'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_011'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_012'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_013'
# ovlpfind = 545
# rot_center  = 1647
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_014'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_015'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################
# sname = 'HA_Crato_71_120keV_4mmCu_600mm_9000_016'
# ovlpfind = 545
# rot_center  = 1647
# reconstruct(sname, rot_center, ovlpfind, 200, 1000)
# ###################################################################################################