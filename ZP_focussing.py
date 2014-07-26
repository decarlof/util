

#output_path = '/local/vdeandrade/txm_util/testdir/zp_focus/'

#zp_focus(output_path, -5, -5.1, 4, 0.2, 1)
#import process_variables as pv
def zp_focus(output_path, pos_start, pos_end, n_steps, acq_time, disp):
#
#   script: zp_focus(output_path, pos_start, pos_end, n_steps, acq_time, disp)
#        - output_path: string
#        - pos_start: zp_focus
#        - pos_end:
#        - n_steps: # of steps during the scan
#        - acq_time: acquisition time in seconds
#        - disp: 0= no dislay, 1= display
#
#   exple: zp_focus(3.0, 3.5, 10, 2, 1)

    # Pre-defined & set parameters
    #################################################################
    sleeptime = 0.2 # time to wait in order to register the stand_dev
    nPt_interp = 40
    wait = 100
    #################################################################
    
    # Get the current position of the ZP:
    curr_pos = pv.zone_plate_z.get()
    # Get the current acquisition time:
    curr_dwell_time = pv.ccd_dwell_time.get()

    # Get the CCD parameters:
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol
    
    # Set the CCD acquisition time:
    pv.ccd_dwell_time.put(acq_time, wait=True, timeout=wait)
    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
    
    # Initialization of variables (scaning range, intensity vector)
    scan_val = np.linspace(pos_start, pos_end, n_steps)
    stand_dev = scan_val*0
#    Mat3D = np.zeros((n_steps, nRow, nCol))

    # Loop acquiring images sequence at different ZP positions:
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i' % (iLoop+1, n_steps)
        print '    Zone plate position along opt. ax.: ', scan_val[iLoop]
        pv.zone_plate_z.put(scan_val[iLoop], wait=True, timeout=wait)
        sleep(sleeptime)

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        # Store the snapshot in the 3D matrix:
#        Mat3D[i,:,:] = img_tmp
        # Store the stand_dev
        stand_dev[iLoop] = np.sum(img_tmp) # store the stand_dev
        # Save data in tif:
        motor_pos_info = np.round(scan_val[iLoop]*1000)
        FileName = output_path+'/ZP_focus_%5.0i.tif' % motor_pos_info
        img = misc.toimage(img_tmp)
        img.save(FileName)

    # CCD mode switched to continuous
    pv.ccd_acquire_mode.put(1, wait=True, timeout=wait)

    # Interpolate the std deviation curve over nPt_interp points:
    f = interpolate.interp1d(scan_val, stand_dev, kind='cubic')
    scan_val_interp = np.linspace(scan_val[0], scan_val[-1], nPt_interp)
    stand_dev_interp = f(scan_val_interp)

    # Get the motor position with the max stand_dev on the interpolated data:
    index_max_stand_dev = np.where(stand_dev_interp==max(stand_dev_interp))

    # Move the ZP at the max stand_dev:
#    pv.zone_plate_z.put(scan_val_interp[index_max_stand_dev], wait=True, timeout=wait)

    plt.plot(scan_val, stand_dev, 'go', scan_val_interp, stand_dev_interp, 'r-'), plt.grid()
    plt.plot(scan_val_interp[index_max_stand_dev], max(stand_dev_interp), 'b*')
    plt.xlabel('Zone plate pos. (mm)'), plt.ylabel('Image std')
    plt.show()
    #plt.show((block=False))

    return

