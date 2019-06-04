## XANES.py
#
import time
import skimage.io as io

# ---------------------------- INPUT ------------------------
output_path = '/local/data/2015_02/2015_02_Nelson/CuSn_stds_XANES.txt'
acq_time = 1 # unit=second
en_st = 8.85; en_end = 9.3; en_stp = 0.025 # unit=keV
offset = 0.100 # unit=keV
exposure = 0.01

sleeptime = 0.2 # s
im_saving_pause = 0.1 # s
wait=5
#------------------------------------------------------------


####################################################################################

pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto


en_vect = np.arange(en_st, en_end, en_stp) # define the energy vector
intensity_scan = np.zeros((len(en_vect), 2)) # col1=energy, col2 = I
intensity_scan[:,0] = en_vect


# Get the CCD parameters:
nRow = pv.ccd_image_rows.get()
nCol = pv.ccd_image_columns.get()
image_size = nRow * nCol

# CCD mode switched to fixed
pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
pv.ccd_Image_number.put(1, wait=True, timeout=wait)
# Set the CCD acquisition time:
pv.ccd_dwell_time.put(exposure, wait=True, timeout=wait)

# move the gap (backclash):
pv.gap_en.put(en_st + offset-0.1, wait=True)

ct = -1
for iEn in range(0,len(en_vect)):
    ct=ct+1
    print '*** Step # %i / %i' % (iEn, len(en_vect))
    print '*** Energy: %0.3f' % en_vect[iEn]
#    moveE(en_vect[iEn])
    # move the gap and the DCM to the suitable energy:
    pv.gap_en.put(en_vect[iEn] + offset, wait=True)
    pv.DCM_en.put(en_vect[iEn], wait=True)

    print 'Pause after energy step'
    sleep(sleeptime)

    intensity_tmp = 0
    
    # loop to acq and sum several images:
    for i in range(0,5):
        # Trigger the CCD
        print ' -- triger CCD'
        pv.ccd_trigger.put(1, wait=True, timeout=wait)
        while pv.ccd_detector_state.get() != 0: time.sleep(0.05)
        print ' -- acq. over'

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get(count=image_size)
#        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])

#        intensity_tmp = intensity_tmp + np.sum(img_tmp[262:307,388:448])
        intensity_tmp = intensity_tmp + np.sum(img_tmp)

    print '  '
    print '  -- sum of the intesnity: %i' % intensity_tmp
    intensity_scan[iEn,1] = intensity_tmp
    print intensity_scan[iEn,1]
    sleep(sleeptime)


# DCM mode: come back to manual
pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto

# Display:
plt.subplot(2,2,1),plt.plot(intensity_scan[:,0], intensity_scan[:,1], 'r.-'), plt.grid(), plt.xlabel('Energy (keV)'), plt.ylabel('I0')
plt.subplot(2,2,3), plt.plot(intensity_scan[:,0], -np.log(intensity_scan[:,1]), 'r.-')
plt.grid(), plt.xlabel('Energy (keV)'), plt.ylabel('abs')
plt.subplot(2,2,4), plt.plot(intensity_scan[0:-1,0], np.diff(-np.log(intensity_scan[:,1])), 'r.-')
plt.grid(), plt.xlabel('Energy (keV)'), plt.ylabel('derivative')
plt.show()


np.savetxt(output_path, intensity_scan, fmt='%f', delimiter='   ', header='Energy(keV), I0, I')

#    FileName = output_path+'%05ieV_%04i.tif' % (en_vect[iEn]*1000, ct)
#    img = img_tmp.astype('uint16')
#    io.imsave(FileName, img)
#    sleep(im_saving_pause)


