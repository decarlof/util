

moveE
    


################################ XANES change:
if 0:
    ################# Input ###############
    output_path = '/local/data/2014_11/2014_11_Chiu/Powder2/XANES/powder2_10s_postred_'
    stage_ff = sample_y
    ff_pos = -0.2
    nff = 1
    nDark=1
    exposure = 10 # unit = seconds
    acq_time = 10000000 # unit = minutes
    Pause = 1 # time ellapsed to save data
    wait=1
    ######################################f
    

    # Get the CCD parameters:
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
    pv.ccd_Image_number.put(1, wait=True, timeout=wait)
    # Set the CCD acquisition time:
    pv.ccd_dwell_time.put(exposure, wait=True, timeout=wait)

    # Acquire the dark:
    dark = dark_acq(exposure, nDark)
    
    # 1st XANES:
    print '##### 1st radiograph @ 8316 eV'
    moveE_8316()

    # Acquire the flat-fields:
    ff = ff_acq(stage_ff, ff_pos, exposure, nff)

    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=exposure+0.1)
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
    
    # Acquire the flat-fields:
    ff = ff_acq(stage_ff, ff_pos, exposure, nff)

    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=exposure+0.1)
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

    # Acquire the flat-fields:
    ff = ff_acq(stage_ff, ff_pos, exposure, nff)
    
    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=exposure+0.1)
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

    # Acquire the flat-fields:
    ff = ff_acq(stage_ff, ff_pos, exposure, nff)
    
    # Acquire the radiograph:
    print '*** Acquiring the sample radiograph...'
    pv.ccd_trigger.put(1, wait=True, timeout=exposure+0.1)
    # Get the image loaded in memory
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])
    
    rad_corr = np.divide(np.subtract(img_tmp, dark), np.subtract(ff, dark))
    
    FileName = output_path+'8376eV.tif'
    img = misc.toimage(rad_corr)
    img.save(FileName)
    sleep(Pause)
  

