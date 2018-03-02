#!/usr/bin/env python

#import Tomo_script_simplified as tss
#from pkg_resources import require; require('cothread'); from numpy import *; import cothread; from cothread.catools import *

####################### INPUT BEFORE LAUNCHING THE tomo_acq FUNCTION: ###################
ThePath = 'C:\\epics\\data\\Manip\\201311\\debug\\'
ThePath_linux = '/epics/data/Manip/201311/debug/'

#FileName = 'Test_Vince'

PV_ThePath = 'XF:05ID-ES:X2B{Cam:1}TIF:FilePath'
PV_FileName = 'XF:05ID-ES:X2B{Cam:1}TIF:FileName'
caput(PV_ThePath, ThePath, datatype=DBR_CHAR_STR, wait=True)	# set the path where the data will be saved
os.chdir(ThePath_linux)

#caput(PV_FileName, FileName, datatype=DBR_CHAR_STR, wait=True)	# set the radix of the files name that will be saved
#########################################################################################


def tomo_acq(ang_range, n_stps, radio_time, nRad, ff_frqcy, ff_time, nff, ff_pos, df_pos):

#   script: tomo_acq(ang_range, n_stps, radio_time, nRad, ff_frqcy, ff_time, nff, ff_pos, df_pos)
#     ang_range: scalar value in degree corresponding to the angular range that has to be scanned
#     n_stps: number of angular steps over the angular range
#     radio_time: dwell time per radio
#     nRad: number of radio acquired per angular position
#     ff_frqcy: number of angles before the acquisition of a new flat field
#     ff_time: flat field dwell time
#     nff: number of flat field frames (for statistic improvement)
#     ff_pos: X stage absolute position for flat field acquisitions
#     df_pos: X stage absolute position for dark field acquisitions (absorber position)
#
# 		script for testing:
# 		tomo_acq(8, 4, 0.3, 3, 4, 0.2, 2, 508, 539)

	# Build the header:
	# .....
	# .....
	# .....
	
	# PV declaration:
	PV_samx = 'XF:05ID1-ES:X2B{Stg:XY-Ax:X}Mtr.VAL'
	PV_rot = 'XF:05ID1-ES:X2B{Stg:Rot-Ax:Omega}Mtr.VAL'
	PV_dwelltime = 'XF:05ID-ES:X2B{Cam:1}AcquireTime'
	PV_prefix = 'XF:05ID-ES:X2B{Cam:1}TIF:FileName'			# 
	PV_radio_index = 'XF:05ID-ES:X2B{Cam:1}TIF:FileNumber'	# next file index
	PV_trigger = 'XF:05ID-ES:X2B{Cam:1}Acquire'
	PV_save = 'XF:05ID-ES:X2B{Cam:1}TIF:WriteFile'
 	PV_nRow_CCD = 'XF:05ID-ES:X2B{Cam:1}SizeY';
	PV_nCol_CCD = 'XF:05ID-ES:X2B{Cam:1}SizeX';
	PV_image = 'XF:05ID-ES:X2B{Cam:1}ARR:ArrayData'
	
	# Create variables:
	curr_samx_pos = caget(PV_samx)					# get the current sample position
	curr_rot_pos = caget(PV_rot)					# get the current angle of the rotary stage
	vect_angle_rel = np.linspace(0, ang_range, n_stps)	# define the vector containing angles
	vect_angle_abs = vect_angle_rel + curr_rot_pos	# define the vector containing angles
	nVPix = caget(PV_nRow_CCD)
	nHPix = caget(PV_nCol_CCD)
	
	# dark field acquisition and saving
	dark_rad_name  = 'dark_rad'
	dark_ff_name  = 'dark_ff'
	
	print ' '; print '*** Move the beamstop in the beam for Dark Field acq.'
	print 'DF pos:', df_pos
	caput(PV_samx,  df_pos, wait=True, timeout=1000)					# move motor samx in position for dark field acquisition
	caput(PV_prefix, dark_rad_name, datatype=DBR_CHAR_STR, wait=True)	# create the file name for the next snapshot saving
	caput(PV_radio_index, 0, timeout=1000)								# change the acquisition index to 0
	caput(PV_dwelltime, radio_time, wait=True, timeout=1000)			# set the dwell time of the snapshot for the first dark
	print '   dark field for the radiographies...'
	caput(PV_trigger, 1, wait=True, timeout=1000)						# trigger the snapshot for the first dark
	caput(PV_save, 1, wait=True, timeout=1000)							# save the snapshot for the first dark
	caput(PV_radio_index, 0, wait=True, timeout=1000)					# change the acquisition index to 0
	caput(PV_prefix, dark_ff_name, datatype=DBR_CHAR_STR, wait=True, timeout=1000)	# create the file name for the next snapshot saving
	caput(PV_dwelltime, ff_time, wait=True, timeout=1000)				# set the dwell time of the snapshot for the second dark
	print '   dark field for the flat field...'
	caput(PV_trigger, 1, wait=True, timeout=1000)						# trigger the snapshot for the second dark
	caput(PV_save, 1, wait=True, timeout=1000)							# save the snapshot for the second dark
	
	# Variables initialization for the loop
	ff_count = 0
	radio_count = 0
	
	# start the angular scan
	for iLoop in range(0, np.size(vect_angle_rel)):
		print ' ';
		print 'loop in process: %i/%i' % (iLoop,np.size(vect_angle_rel))
		print '  Angle: %d (abs pos); %d (rel pos)' % (vect_angle_abs[iLoop], vect_angle_rel[iLoop])
		print vect_angle_abs[iLoop]
		caput(PV_rot, vect_angle_abs[iLoop], wait=True, timeout=1000)	# rotary stage movement by the angular incrementation

		# deal with the flat field acquisitions:
		if np.remainder(iLoop, ff_frqcy)==0 or iLoop ==0:			# check if the flat-field acquisition is required
			print ' '
			print '********* Move samx for Flat Field acq.'
			print 'FF pos:', ff_pos
			caput(PV_samx,  ff_pos, wait=True, timeout=1000)	# move to the flat field location
			caput(PV_dwelltime, ff_time, timeout=1000)			# set the dwell time for the flat-field
			ff_count+=1
			Img = np.zeros((nVPix, nHPix), dtype=np.uint16)
			
			print '#### Start Flat Field. acq. # %i' % ff_count
			for iff in range(0, nff):
				print '    Acq. ff %i_%i' % (ff_count, iff)
				caput(PV_trigger, 1, wait=True, timeout=1000)	# trigger the CCD
				Img_vect = caget(PV_image)							# get the image in memory
				Img_tmp = np.reshape(Img_vect,[nVPix, nHPix])
				Img = Img + Img_tmp
			
			Img = Img/nff
			print Img.dtype
			print np.max(Img)
#			Img = np.asarray(Img,dtype=np.uint16)
			Img2 = Img.astype('uint16')
			im=Image.fromarray(Img2)								# save the sum ff image
			FileName = 'ff_%i.tiff' % ff_count					# save the sum ff image
			im.save(FileName)									# save the sum ff image

			print ' '; print '*** Move the sample in position for radio acq.'
			print 'Sample pos:', curr_samx_pos
			caput(PV_samx,  curr_samx_pos, wait=True, timeout=1000)	# come back to the sample location
		
		# Acquisition of the sample radiographies
		radio_count+=1
		Img = np.zeros((nVPix, nHPix), dtype='uint16')
		print '#### Start radio. acq. # %i' % radio_count
		caput(PV_dwelltime, radio_time, wait=True, timeout=1000)	# set the dwell time for the radio
		for iRad in range(0, nRad):
			print '    Acq. radio %i_%i' % (radio_count, iRad)
			caput(PV_trigger, 1, wait=True, timeout=1000)		# trigger the CCD
			Img_vect = caget(PV_image)						# get the image in memory
			Img_tmp = np.reshape(Img_vect,[nVPix, nHPix])
#			Img_tmp = np.ndarray(buffer=Img_vect,shape=(nVPix, nHPix),dtype=np.uint16)
			Img = Img + Img_tmp
		
		Img = Img/nRad
		print Img.dtype

#		Img = np.asarray(Img, dtype=np.uint16)
		Img = Img.astype('uint16')
		im=Image.fromarray(Img)								# save the sum ff image
		FileName = 'radio_%i.tiff' % radio_count				# save the sum ff image
		im.save(FileName)									# save the sum ff image
		
	# Bring samx on the beam stop position
	print '*** Move the beamstop in the beam'
	caput(PV_samx,  df_pos, wait=True, timeout=1000)
	print 'Acquisition done'




