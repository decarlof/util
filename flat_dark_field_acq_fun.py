
def ff_acq(stage_ff, ff_pos, exposure, nff):
#
#   script: ff_acq(stage_ff, ff_pos, exposure, nff)
#   exple: FF = ff_acq(sample_y, -0.2, 10, 1)

    # Get the CCD parameters:
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
    pv.ccd_Image_number.put(1, wait=True, timeout=wait)
    # Set the CCD acquisition time:
    pv.ccd_dwell_time.put(exposure, wait=True, timeout=wait)

    # Acquire and average n flat flieds:
    print '*** Move to flat-field position...'
    stage_ff.put(ff_pos, wait=True, timeout=wait)
    sleep(3)
    print '*** Acquiring the flat-fields...'
    ff_tmp = np.zeros((nRow, nCol))
    for iFF in range(0,nff):
        print '   ff# %i' % (iFF+1)
        pv.ccd_trigger.put(1, wait=True, timeout=wait)
        while pv.ccd_detector_state.get() != 0: time.sleep(0.05)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get(count=image_size)
        ff_tmp = ff_tmp + np.reshape(img_vect,[nRow, nCol])
        sleep(1)

    ff = np.round(ff_tmp/nff)
    stage_ff.put(0, wait=True, timeout=wait) # move sample back in
    sleep(3)
    return ff


def dark_acq(exposure, nDark):
#
#   script: dark_acq(exposure, nDark)
#   exple: dark = dark_acq(2, 5)

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
    sleep(0.5)
    pv.close_shutter_B.put(1, wait=True, timeout=wait) # close the shutter 
    sleep(1.5)

    print '*** Acquiring the dark-fields...'
    dark_tmp = np.zeros((nRow, nCol))
    for iDark in range(0,nDark):
        pv.ccd_trigger.put(1, wait=True, timeout=exposure)
        while pv.ccd_detector_state.get() != 0: time.sleep(0.05)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get(count=image_size)
        dark_tmp = dark_tmp + np.reshape(img_vect,[nRow, nCol])
        sleep(0.5)

    dark = np.round(img_tmp/nDark)

    print '*** Open the shutter...'
    pv.open_shutter_B.put(1, wait=True, timeout=wait) # close the shutter 
    sleep(4); pv.BPM_DCM_FBL.put(1, wait=True, timeout=wait); sleep(0.5) # turn feedback on

    return dark





