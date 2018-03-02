## XANES.py
#
# data=np.loadtxt('/local/data/2014_11/2014_11_Chiu/XANES/XANES.txt')
# ---------------------------- INPUT ------------------------
FileName = '/local/data/2015_02/2015_02_Nelson/CuSn_std_XANES.txt'
acq_time = 0.5 # unit=second
en_st = 8.98; en_end = 9.100; en_stp = 0.004 # unit=keV
offset = 0.100 # unit=keV
sleeptime = 0.2
wait=5
#------------------------------------------------------------

en_vect = np.arange(en_st, en_end, en_stp)
intensity_scan = np.zeros((len(en_vect), 3)) # col1=energy, col2 = I0; col3 = I
intensity_scan[:,0] = en_vect

############################ play with CCD settings: ###################
# Set the CCD acquisition time:
#pv.ccd_dwell_time.put(acq_time, wait=True, timeout=wait)
## CCD mode switched to fixed
#pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
## CCD binning
#pv.ccd_binning.put(4, wait=True, timeout=wait) # state = 4 --> 8x8 bin
## get CCD parameters:
#nRow = pv.ccd_image_rows.get()
#nCol = pv.ccd_image_columns.get()
#image_size = nRow * nCol
#pv.ccd_trigger.put(1, wait=True, timeout=wait) # Trigger the CCD
########################################################################

#wait on a pv to be a value until max_timeout (default forever)
def wait_pv(pv, wait_val, max_timeout_sec=-1):
	print 'wait_pv(', pv.pvname, wait_val, max_timeout_sec, ')'
	#delay for pv to change
	time.sleep(.05)
	startTime = time.time()
	while(True):
		pv_val = pv.get()
		if (pv_val != wait_val):
			if max_timeout_sec > -1:
				curTime = time.time()
				diffTime = curTime - startTime
				if diffTime >= max_timeout_sec:
					return False
			time.sleep(.1)
		else:
			return True

############################ play with the ion chambers #############################
dwelltime = pv.ion_chamber_autodwelltime.get() # get the dwell time of the auto mode
pv.ion_chamber_dwelltime.put(acq_time, wait=True, timeout=wait) # assigned the dwell time to the oneshot mode

print 'Switch ion chamber on OneShot mode'
pv.ion_chamber_auto.put(0, wait=True, timeout=wait) # switch automatic to 1 shot mode
print 'Done!'

print 'Trigger ion chamber once'
pv.ion_chamber_trigger.put(1, wait=True, timeout=wait)
####################################################################################


pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
wait_pv(DCM_mvt_status, 1)


pv.gap_en.put(en_vect[0] + offset-0.1, wait=True)# -0.1 for the gap (backclash):
pv.DCM_en.put(en_vect[0], wait=True)

for iEn in range(0,len(en_vect)):
    print '*** Step # %i / %i' % (iEn, len(en_vect))
    print '*** Energy: %04.4f' % en_vect[iEn]
    # move the gap and the DCM to the suitable energy:
    pv.gap_en.put(en_vect[iEn] + offset, wait=True)
    pv.DCM_en.put(en_vect[iEn], wait=True)

    print 'Pause after energy step'
    sleep(sleeptime)

#    # Trigger the CCD
#    pv.ccd_trigger.put(1, wait=True, timeout=wait)
#
#    # Get the image loaded in memory
#    img_vect = pv.ccd_image.get()
#    img_vect = img_vect[0:image_size]
#    img_tmp = np.reshape(img_vect,[nRow, nCol])
#
#    intensity_scan[iEn,1] = np.sum(img_tmp)
#

    pv.ion_chamber_trigger.put(1, wait=True)
    wait_pv(ion_chamber_trigger, 0)

    intensity_scan[iEn,1] = pv.ion_chamber_DCM.get()
    intensity_scan[iEn,2] = pv.ion_chamber_down.get()
    print intensity_scan[iEn,1]
    print intensity_scan[iEn,2]


# Come back to the initial CCD binning values:
#pv.ccd_binning.put(0, wait=True, timeout=wait) # state = 4 --> 8x8 bin


# DCM mode: come back to manual
pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto

np.savetxt(FileName, intensity_scan, fmt='%f', delimiter='   ', header='Energy(keV), I0, I')

pv.ion_chamber_auto.put(1, wait=True, timeout=wait) # come back to automatic mode


###################################
#en_st = 8.37; en_end = 8.550; en_stp = 0.001 # unit=keV
#en_vect = np.arange(en_st, en_end, en_stp)
#intensity_scan = np.zeros((len(en_vect), 3)) # col1=energy, col2 = I0; col3 = I
#intensity_scan=np.loadtxt('/local/data/2014_11/2014_11_Chiu/XANES/XANES.txt')
#intensity_scan[:,0] = en_vect

#filter_struct = 5
#intensity_scan[:,1] = filters.median_filter(intensity_scan[:,1], footprint=np.ones(filter_struct))
#intensity_scan[:,2] = filters.median_filter(intensity_scan[:,2], footprint=np.ones(filter_struct))

# Display
#plt.subplot(2,2,2),plt.plot(intensity_scan[:,0], intensity_scan[:,2], 'r.-'), plt.grid(), #plt.xlabel('Energy (keV)'), plt.ylabel('I')
plt.subplot(2,2,1),plt.plot(intensity_scan[:,0], intensity_scan[:,1], 'r.-'), plt.grid(), plt.xlabel('Energy (keV)'), plt.ylabel('I0')
plt.subplot(2,2,3), plt.plot(intensity_scan[:,0], -np.log(intensity_scan[:,2]), 'r.-')
plt.grid(), plt.xlabel('Energy (keV)'), plt.ylabel('abs')
#plt.subplot(2,2,4), plt.plot(intensity_scan[0:-1,0], np.diff(-np.log(np.divide(intensity_scan[:,2], intensity_scan[:,1]))), 'r.-')
plt.subplot(2,2,4), plt.plot(intensity_scan[0:-1,0], np.diff(-np.log(intensity_scan[:,1])), 'r.-')
plt.grid(), plt.xlabel('Energy (keV)'), plt.ylabel('derivative')
plt.show()





#pv.gap_en.put(en_vect[iEn] + offset, wait=True); pv.DCM_en.put(en_vect[iEn], wait=True)


