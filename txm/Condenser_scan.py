

######################### INPUT ##########################
n_cond_zstep = 40
cond_z_start = -656
cond_z_end = -606
acq_time = 0.005
output_path = '/local/data/2015_06/Anne/align/'
the_pause = 1.5
Info = 'scan_40mm_656to606_40pts_'
##########################################################

# Define the vector containing Motor positions to be scanned:
vect_pos_z = np.linspace(cond_z_start, cond_z_end, n_cond_zstep)

# Get the CCD parameters:
nRow = pv.ccd_image_rows.get()
nCol = pv.ccd_image_columns.get()
image_size = nRow * nCol

# Set the CCD acquisition time:
pv.ccd_dwell_time.put(acq_time, wait=True, timeout=100)
# CCD mode switched to fixed
pv.ccd_acquire_mode.put(0, wait=True, timeout=100)


########### START THE 2D SCAN
print '*** Start the butterfly:'
# Move the Butterfly to the Z starting point
pv.condenser_z.put(vect_pos_z[0], wait=True)
pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger once fisrt to avoid a reading bug
while pv.ccd_detector_state.get() != 0: time.sleep(0.05)


for iLoop in range(0, n_cond_zstep):
    print '\n ####################################'
    print '  -- Loop #%i,  Motor pos: %04.4f' % (iLoop, vect_pos_z[iLoop])
    pv.condenser_z.put(vect_pos_z[iLoop], wait=True, timeout=100)
    sleep(the_pause)

    # Trigger the CCD
    pv.ccd_trigger.put(1, wait=True, timeout=100)
    while pv.ccd_detector_state.get() != 0: time.sleep(0.05)

    # Get the image loaded in memory
    img_vect = pv.ccd_image.get(count=image_size)
    img_tmp = np.reshape(img_vect,[nRow, nCol])

    FileName = output_path+'/cond_focus_'+Info+'%04i.tif' % iLoop
    img = misc.toimage(img_tmp)
    img.save(FileName)

# CCD mode switched to continuous
pv.ccd_acquire_mode.put(2, wait=True, timeout=100)

