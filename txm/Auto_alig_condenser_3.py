#output_path = '/local/vdeandrade/txm_util/testdir/zp_focus/'

#zp_focus(output_path, -5, -5.1, 4, 0.2, 1)
#import process_variables as pv
def align_cond_pitch(pos_start, pos_end, n_steps, acq_time, disp):
#
#   script: zp_focus(output_path, pos_start, pos_end, n_steps, acq_time, disp)
#        - output_path: string
#        - pos_start: zp_focus
#        - pos_end:
#        - n_steps: # of steps during the scan
#        - acq_time: acquisition time in seconds
#        - disp: 0= no dislay, 1= display
#
#   exple: align_cond_pitch(3.0, 3.5, 5, 0.4, 1)

    # Pre-defined & set parameters
    #################################################################
    sleeptime = 0.2 # time to wait in order to register the delta_R
    nPt_interp = 40
    wait = 100
    Thresh_low = 110;
    #################################################################
    
    # Get the current position of the condenser pitch:
    curr_pos = pv.condenser_pitch.get()
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
    delta_R = scan_val*0

    # Loop acquiring images sequence at different pitch positions:
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i' % (iLoop+1, n_steps)
        print '    Zone plate position along opt. ax.: ', scan_val[iLoop]
        pv.condenser_pitch.put(scan_val[iLoop], wait=True, timeout=wait)
        sleep(sleeptime)

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img = np.reshape(img_vect,[nRow, nCol])

        # Centroid calculation of the direct beam:
        Thresh_high = np.max(img) * 0.1;
        img_disc = np.copy(img)
        img_disc[np.where(img<Thresh_high)] = 0
        center = ndimage.measurements.center_of_mass(img)
        centX = center[1]
        centY = center[0]

        img = filters.median_filter(intensity, footprint=np.ones(filter_struct))

        # Store the snapshot in the 3D matrix:
#        Mat3D[i,:,:] = img
        # Store the delta_R
        delta_R[iLoop] = np.sum(img) # store the delta_R
        # Save data in tif:
        motor_pos_info = np.round(scan_val[iLoop]*1000)
        FileName = output_path+'/ZP_focus_%5.0i.tif' % motor_pos_info
        img = misc.toimage(img)
        img.save(FileName)

    # CCD mode switched to continuous
    pv.ccd_acquire_mode.put(1, wait=True, timeout=wait)

    # Interpolate the std deviation curve over nPt_interp points:
    f = interpolate.interp1d(scan_val, delta_R, kind='cubic')
    scan_val_interp = np.linspace(scan_val[0], scan_val[-1], nPt_interp)
    delta_R_interp = f(scan_val_interp)

    # Get the motor position with the max delta_R on the interpolated data:
    index_max_delta_R = np.where(delta_R_interp==max(delta_R_interp))

    # Move the ZP at the max delta_R:
#    pv.condenser_pitch.put(scan_val_interp[index_max_delta_R], wait=True, timeout=wait)

    plt.plot(scan_val, delta_R, 'go', scan_val_interp, delta_R_interp, 'r-'), plt.grid()
    plt.plot(scan_val_interp[index_max_delta_R], max(delta_R_interp), 'b*')
    plt.xlabel('Zone plate pos. (mm)'), plt.ylabel('Image std')
    plt.show()
    #plt.show((block=False))

    return
