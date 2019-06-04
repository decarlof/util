import time
import skimage.io as io

#################### INPUT ######################
output_path = '/local/data/2015_02/2015_02_IUPUI/'
stage_ff = sample_y
ff_pos = -0.2
nff = 10
nDark=5
exposure = 0.02 # unit = seconds
acq_time = 10000000 # unit = minutes
Pause = 1 # time ellapsed to save data
wait=0.1
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
    dark = dark_acq(exposure, nDark)

    Dark_FileName = output_path+'Dark_st_avg%iDark.tif' % nDark
    img = misc.toimage(dark)
    img.save(Dark_FileName)
    sleep(0.5)

if 0:
    ff = ff_acq(stage_ff, ff_pos, exposure, nff)

    FF_FileName = output_path+'ff_st_avg%iff.tif' % nff
    img = misc.toimage(img_tmp)
    img.save(FF_FileName)
    sleep(0.5)

if 0:
    ff = ff_acq(stage_ff, ff_pos, exposure, nff)

    FF_FileName = output_path+'ff_end_avg%iff.tif' % nff
    img = misc.toimage(img_tmp)
    img.save(FF_FileName)
    sleep(0.5)


########################################
# Prepare the movie acquisition:
#start = time()
elapsed_time = 0
img_ct = -1

# Start movie acquisition:
print '*** Starting the movie acquisition...'
#while elapsed_time < acq_time:
while 1:
    print 'image # %i' % (img_ct+1)
    # Image counter:
    img_ct = img_ct+1

#    curr_time = time()
#   elapsed_time = (curr_time - start)/60

    # Trigger the CCD
    pv.ccd_trigger.put(1, wait=True, timeout=wait)
    while pv.ccd_detector_state.get() != 0: time.sleep(0.05)

    # Get the image loaded in memory
    img_vect = pv.ccd_image.get(count=image_size)
    if img_vect is None:
        # did not get an image: need to stop the detector
        pv.ccd_trigger.put(0, wait=True)
        img_vect = pv.ccd_image.get(count=image_size)
    if img_vect is not None:
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        FileName = output_path+'%04i.tif' % img_ct
        img = img_tmp.astype('uint16')
#        io.imsave(FileName, img, plugin='tifffile')
        io.imsave(FileName, img)
        sleep(Pause)



