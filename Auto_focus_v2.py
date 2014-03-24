#!/usr/bin/env python


#import matplotlib.pylab as plt
#from PIL import Image

import Auto_focus_v2 as af

# best value at 39000

def auto_focus(Range, steps, dwell_time):
	from scipy import interpolate
#   auto_focus(Range, steps, dwell_time)
#
#	This autofocus is based on the contrast of images.
#     Range: range for the scanning of the motor repsonsible for the fine focus
#	  steps: number of steps inside the scanned range
#	  dwell_time: dwell time for the CCD acquisition

#	auto_focus(3000, 10, 0.2)

	# PV declaration:
	PV_focus = 'XF:05ID1-ES:X2B{Cam-Ax:Focus}Mtr.VAL'
	PV_dwelltime = 'XF:05ID-ES:X2B{Cam:1}AcquireTime'
	PV_trigger = 'XF:05ID-ES:X2B{Cam:1}Acquire'
 	PV_nRow_CCD = 'XF:05ID-ES:X2B{Cam:1}SizeY';
	PV_nCol_CCD = 'XF:05ID-ES:X2B{Cam:1}SizeX';
	PV_image = 'XF:05ID-ES:X2B{Cam:1}ARR:ArrayData'
	

	# Work on a ROI
	ROI=1
	
	# Variables creation:
	ROI_pixH = [400, 2300]
	ROI_pixV = [620, 1900]
	ROI_pixH = [1300, 1500]
	ROI_pixV = [800, 1000]
	
 	nVPix = caget(PV_nRow_CCD)
	nHPix = caget(PV_nCol_CCD)
#	nHPix = 2560	# CCD parameter
#	nVPix = 2160	# CCD parameter

#	if ROI:
#		Mat3D = np.zeros((steps, (ROI_pixV[1]-ROI_pixV[0]), (ROI_pixH[1]-ROI_pixH[0])), np.int16)
#	else:
	Mat3D = np.zeros((steps, nVPix, nHPix), np.int16)	# initialize the 3D matrix

			
	prefix = 'focus'
	curr_focus_pos = caget(PV_focus)									# get the current focus position
	vect_pos = np.linspace(curr_focus_pos - Range/2, curr_focus_pos + Range/2, steps)	# define the vector containing angles
	delta_step = abs(vect_pos[1] - vect_pos[0])							# get the delta angle
	Std_Im = np.arange(0,np.size(vect_pos),1)
	
	caput(PV_dwelltime, dwell_time)
	
	# move the focus before the scan starting point to annihilate the backlash
	caput(PV_focus, vect_pos[0]-8000, wait=True, timeout=500)
	print '*** Starting position: ',(vect_pos[0]-8000)
 
	# start the focus scan
	for iLoop in range(0, steps):
		print '*** Step #%i / %i' % (iLoop, np.size(vect_pos))
		print '    Motor pos: ',vect_pos[iLoop]
		caput(PV_focus, vect_pos[iLoop], wait=True, timeout=500)			#
		caput(PV_trigger, 1, wait=True, timeout=500)					# trigger the CCD
		
		# get the image still in memory
		Img_vect = caget(PV_image)
		Img_tmp = np.reshape(Img_vect,[nVPix, nHPix])
		
		Mat3D[iLoop,:,:] = Img_tmp			# store the image in Mat3D
	
		if ROI:
#			Im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
			Im = Mat3D[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
		else:
			Im = Mat3D[iLoop,:,:]
			
		Std_tmp = Im.std(axis=0)
		Std_Im[iLoop] = Std_tmp.std(axis=0)	# store the std devation in Std_Im

#		plt.imshow(Img_tmp), plt.set_cmap('gray'), plt.colorbar()
#		plt.set_title('Image #%i, focus:%f' % (iLoop, vect_pos(iLoop)))
		
	# Interpolate the minimum value
#	Std_int = interp(linspace(vect_pos[0], vect_pos[-1], 10), vect_pos, Std_Im)
	f = interpolate.interp1d(vect_pos, Std_Im, kind='cubic')	
	vect_pos_int = np.linspace(vect_pos[0], vect_pos[-1], 50)
	Std_int = f(vect_pos_int)
	
	# get the highest sdt:
	Index_max_std = np.where(Std_int==max(Std_int))

	print '*** Best focus at ', vect_pos_int[Index_max_std]
	
 
	plt.plot(vect_pos, Std_Im, 'go', vect_pos_int, Std_int, 'r-'), plt.grid()
	plt.plot(vect_pos_int[Index_max_std], max(Std_int), 'b*')
	plt.title('Standard deviation for different focus values')
	plt.show()
	
	return [Mat3D, Std_int]
	
#import matplotlib.pylab as plt	
#plt.ion()
#img = plt.imread('radio_16.tiff')
#plt.imshow(img), plt.set_cmap('jet'), plt.colorbar()
#plt.set_cmap('hot')
#plt.colorbar()
#plt.hist(lum_img.flatten(), 256, range=(0.0,1.0), fc='k', ec='k')
#plt.clim(0.0,0.7)
#rsize = img.resize((img.size[0]/10,img.size[1]/10)) # Use PIL to resize
#rsizeArr = np.asarray(rsize)  # Get array back
#imgplot = plt.imshow(rsizeArr)


# COMMAND LINE EXAMPLES:
# os.getcwd()
# os.listdir('.') 
# os.chdir("dir path or name")
# os.makedirs('dir name')
# os.removedirs(path)
# execfile("Startup.py")
# execfile("file name",global_vars,local_vars)
                                   

