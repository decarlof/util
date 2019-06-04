# 

def gonio_tuning_z(ang_range, n_stps, radio_time):
	
	#    script:
	#
	#

	# PV declaration:
	PV_samx = 'XF:05ID1-ES:X2B{Stg:XY-Ax:X}Mtr'
	PV_gonio = 'XF:05ID1-ES:X2B{Stg:Tilt-Ax:P}Mtr'
	#PV_gonio_x = 'XF:05ID1-ES:X2B{Stg:Tilt-Ax:R}Mtr'
	PV_dwelltime = 'XF:05ID-ES:X2B{Cam:1}AcquireTime'
	PV_trigger = 'XF:05ID-ES:X2B{Cam:1}Acquire'
	PV_nRow_CCD = 'XF:05ID-ES:X2B{Cam:1}ArraySizeY';
	PV_nCol_CCD = 'XF:05ID-ES:X2B{Cam:1}ArraySizeX';
	
	# Create variables:
	curr_gonio_pos = caget('PV_gonio')
	curr_rot_pos = caget('PV_rot')
	vect_angle = np.linspace(0, ang_range, n_stps)			# define the vector containing angles
	delta_angle = vect_angle(2)							# get the delta angle
	nRow = caget('PV_nRow')
	nCol = caget('PV_nCol')
	nAcq = np.size(vect_angle),1
	mat3D = np.zeros(nRow, nCol, nAcq)
	centroid = np.zeros(np.size(vect_angle),2)
	[X,Y] = np.meshgrid(np.arange(1,nCol+1), np.arange(1,nRow+1))	# used for the centroid calculation
	
	# Variables initialization for the loop
	caput('PV_dwelltime', radio_time)					# set the dwell time
	abs_angle_pos = curr_gonio_pos - ang_range/2 - delta_angle
	
	# start the angular scan
	for iLoop in range(1, size(vect_angle)):
		abs_angle_pos = abs_angle_pos + delta_angle	 	# angular incrementation
		caput('PV_gonio', abs_angle_pos, wait=True)		# goniometer movement by the angular incrementation
		caput('PV_trigger', wait=True)				# trigger the snapshot
		vect_image = caget('PV_image', wait=True)	# get the snapshot in 1d vector shape
		mat2D = np.reshape(vect_image, [nRow, nCol])			# construct the 2D image
		mat3D[:,:,iLoop] = mat2D

		# Centroid calculation
		centX = np.sum(np.multiply(mat2D,X)/np.sum(Mat2D));
		centY = np.sum(np.multiply(Mat2D,Y)/np.sum(Mat2D));

		# Storage of centroid values
		centroid[iLoop-1,:] = [centX, centY]
		
	# display the matrix and its centroid:
	del cothread 										# delete cothread because of incompatibilty with show
	plt.plot(centroid[:,0], centroid[:,1], 'r.-'), plt.grid()
	plt.show()
	import cothread; from cothread.catools import *			# re-import cothread
	
	return [Mat3D, centroid]
