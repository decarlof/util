
#################### INPUT ######################
output_path = '/local/data/2014_11/2014_11_Chiu/Powder2/movie/powder2_1s_'
stage_ff = sample_y
ff_pos = -0.2
nff = 10
nDark=5
exposure = 1 # unit = seconds
acq_time = 10000000 # unit = minutes
Pause = 1 # time ellapsed to save data
wait=1
#################################################


# Get the CCD parameters:
nRow = pv.ccd_image_rows.get()
nCol = pv.ccd_image_columns.get()
image_size = nRow * nCol

# CCD mode switched to fixed
pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
pv.ccd_Image_number.put(1, wait=True, timeout=wait)
# Set the CCD acquisition time:
pv.ccd_dwell_time.put(exposure, wait=True, timeout=wait)

# acquire flat & dark field:
#---------------------------
    # Acquire n dark flieds, average them and save:
if 0:
    print '*** Close the shutter...'
    pv.BPM_DCM_FBL.put(0, wait=True, timeout=wait) # turn feedback off
    pv.close_shutter_B.put(1, wait=True, timeout=wait) # close the shutter 

    print '*** Acquiring the dark-fields...'
    img_tmp = np.zeros((nRow, nCol))
    for iDark in range(0,nDark):
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = img_tmp + np.reshape(img_vect,[nRow, nCol])

    img_tmp = np.round(img_tmp/nDark)
    Dark_FileName = output_path+'Dark_st_avg%iDark.tif' % nDark
    img = misc.toimage(img_tmp)
    img.save(Dark_FileName)
    sleep(0.5)

    print '*** Open the shutter...'
    pv.open_shutter_B.put(1, wait=True, timeout=wait) # close the shutter 
    sleep(4)
    pv.BPM_DCM_FBL.put(1, wait=True, timeout=wait) # turn feedback on

if 1:
    # Acquire n flat flieds, average them and save:
    print '*** Move to flat-field position...'
    stage_ff.put(ff_pos, wait=True, timeout=wait)
    print '*** Acquiring the flat-fields...'
    img_tmp = np.zeros((nRow, nCol))
    for iFF in range(0,nff):
        print '   ff# %i' % (iFF+1)
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = img_tmp + np.reshape(img_vect,[nRow, nCol])

    img_tmp = np.round(img_tmp/nff)
    FF_FileName = output_path+'ff_st_avg%iff.tif' % nff
    img = misc.toimage(img_tmp)
    img.save(FF_FileName)
    sleep(0.5)
    stage_ff.put(0, wait=True, timeout=wait)


########################################
# Prepare the movie acquisition:
start = time()
elapsed_time = 0
img_ct = -1

# Start movie acquisition:
print '*** Starting the movie acquisition...'
while elapsed_time < acq_time:
    print 'image # %i' % (img_ct+1)
    # Image counter:
    img_ct = img_ct+1

#    print 'Wait buddy...'
    curr_time = time()
    elapsed_time = (curr_time - start)/60

    # Trigger the CCD
    pv.ccd_trigger.put(1, wait=True, timeout=wait)

    # Get the image loaded in memory
    img_vect = pv.ccd_image.get()
    if img_vect is None:
        # did not get an image: need to stop the detector
        pv.ccd_trigger.put(0, wait=True)
        img_vect = pv.ccd_image.get()
    if img_vect is not None:
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        FileName = output_path+'%04i.tif' % img_ct
        img = misc.toimage(img_tmp)
        img.save(FileName)
        sleep(Pause)

