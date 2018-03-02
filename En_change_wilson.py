

################################ Energy change:
def moveE_8316():
    pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
    offset = 0.132
    pv.gap_en.put(8.316 + offset, wait=True) # miove the gap
    pv.DCM_en.put(8.316, wait=True) # move the DCM
    pv.zone_plate_z.put(-0.291, wait=True)
    pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto


def moveE_8348():
    pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
    offset = 0.132
    pv.gap_en.put(8.348 + offset, wait=True) # miove the gap
    pv.DCM_en.put(8.348, wait=True) # move the DCM
    pv.zone_plate_z.put(0, wait=True)
    pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto

def moveE_8358():
    pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
    offset = 0.132
    pv.gap_en.put(8.358 + offset, wait=True) # miove the gap
    pv.DCM_en.put(8.358, wait=True) # move the DCM
    pv.zone_plate_z.put(0.091, wait=True)
    pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto
    
def moveE_8376():
    pv.DCM_mvt_status.put(1, wait=True) # status: 0=manual, 1=auto
    offset = 0.132
    pv.gap_en.put(8.376 + offset, wait=True) # miove the gap
    pv.DCM_en.put(8.376, wait=True) # move the DCM
    pv.zone_plate_z.put(0.255, wait=True)
    pv.DCM_mvt_status.put(0, wait=True) # status: 0=manual, 1=auto
    
    


################################ XANES change:
if 1:
    ################# Input ###############
    output_path = '/local/data/2014_11/2014_11_Chiu/Powder1/XANES/powder2_10s_preheat_'
    stage_ff = sample_y
    ff_pos = -0.2
    nff = 1
    nDark=1
    exposure = 10 # unit = seconds
    acq_time = 10000000 # unit = minutes
    Pause = 1 # time ellapsed to save data
    wait=1
    ######################################
    

    # Get the CCD parameters:
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
    pv.ccd_Image_number.put(1, wait=True, timeout=wait)
    # Set the CCD acquisition time:
    pv.ccd_dwell_time.put(exposure, wait=True, timeout=wait)

    print '*** Close the shutter...'
    pv.BPM_DCM_FBL.put(0, wait=True, timeout=wait) # turn feedback off
    pv.close_shutter_B.put(1, wait=True, timeout=wait) # close the shutter 

    print '*** Acquiring the dark-fields...'
    dark_tmp = np.zeros((nRow, nCol))
    for iDark in range(0,nDark):
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        dark_tmp = dark_tmp + np.reshape(img_vect,[nRow, nCol])

    dark = np.round(img_tmp/nDark)
    sleep(0.5)

    print '*** Open the shutter...'
    pv.open_shutter_B.put(1, wait=True, timeout=wait) # close the shutter 
    sleep(4)
    pv.BPM_DCM_FBL.put(1, wait=True, timeout=wait) # turn feedback on

    
    # 1st XANES:
    print '##### 1st radiograph @ 8316 eV'
    moveE_8316()
    # Acquire and average n flat flieds:
    print '*** Move to flat-field position...'
    stage_ff.put(ff_pos, wait=True, timeout=wait)
    print '*** Acquiring the flat-fields...'
    ff_tmp = np.zeros((nRow, nCol))
    for iFF in range(0,nff):
        print '   ff# %i' % (iFF+1)
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        ff_tmp = ff_tmp + np.reshape(img_vect,[nRow, nCol])

    ff = np.round(ff_tmp/nff)
    stage_ff.put(0, wait=True, timeout=wait) # move sample back in
    
    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=wait)
    # Get the image loaded in memory
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])
    
    rad_corr = np.divide(np.subtract(img_tmp, dark), np.subtract(ff, dark))
    
    FileName = output_path+'8316eV.tif'
    img = misc.toimage(rad_corr)
    img.save(FileName)
    sleep(Pause)


    # 2nd XANES:
    print '##### 2nd radiograph @ 8348 eV'
    moveE_8348()
    # Acquire and average n flat flieds:
    print '*** Move to flat-field position...'
    stage_ff.put(ff_pos, wait=True, timeout=wait)
    print '*** Acquiring the flat-fields...'
    ff_tmp = np.zeros((nRow, nCol))
    for iFF in range(0,nff):
        print '   ff# %i' % (iFF+1)
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        ff_tmp = ff_tmp + np.reshape(img_vect,[nRow, nCol])

    ff = np.round(ff_tmp/nff)
    stage_ff.put(0, wait=True, timeout=wait) # move sample back in
    
    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=wait)
    # Get the image loaded in memory
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])
    
    rad_corr = np.divide(np.subtract(img_tmp, dark), np.subtract(ff, dark))
    
    FileName = output_path+'8348eV.tif'
    img = misc.toimage(rad_corr)
    img.save(FileName)
    sleep(Pause)


    # 3rd XANES:
    print '##### 3rd radiograph @ 8358 eV'
    moveE_8358()
    # Acquire and average n flat flieds:
    print '*** Move to flat-field position...'
    stage_ff.put(ff_pos, wait=True, timeout=wait)
    print '*** Acquiring the flat-fields...'
    ff_tmp = np.zeros((nRow, nCol))
    for iFF in range(0,nff):
        print '   ff# %i' % (iFF+1)
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        ff_tmp = ff_tmp + np.reshape(img_vect,[nRow, nCol])

    ff = np.round(ff_tmp/nff)
    stage_ff.put(0, wait=True, timeout=wait) # move sample back in
    
    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=wait)
    # Get the image loaded in memory
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])
    
    rad_corr = np.divide(np.subtract(img_tmp, dark), np.subtract(ff, dark))
    
    FileName = output_path+'8358eV.tif'
    img = misc.toimage(rad_corr)
    img.save(FileName)
    sleep(Pause)

   
    # 4th XANES:
    print '##### 4th radiograph @ 8376 eV'
    moveE_8376()
    # Acquire and average n flat flieds:
    print '*** Move to flat-field position...'
    stage_ff.put(ff_pos, wait=True, timeout=wait)
    print '*** Acquiring the flat-fields...'
    ff_tmp = np.zeros((nRow, nCol))
    for iFF in range(0,nff):
        print '   ff# %i' % (iFF+1)
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        ff_tmp = ff_tmp + np.reshape(img_vect,[nRow, nCol])

    ff = np.round(ff_tmp/nff)
    stage_ff.put(0, wait=True, timeout=wait) # move sample back in
    
    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=wait)
    # Get the image loaded in memory
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])
    
    rad_corr = np.divide(np.subtract(img_tmp, dark), np.subtract(ff, dark))
    
    FileName = output_path+'8376eV.tif'
    img = misc.toimage(rad_corr)
    img.save(FileName)
    sleep(Pause)
    



