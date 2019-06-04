

def knife_edge(Motor, X_start, X_end, n_steps, acq_time, disp):

#   exple: knife_edge(sample_x, -0.25, 0.05, 15, 2, 0)

    # Pre-defined & set parameters
    ####################################################################
    Threshold = 200
    sleeptime = 0.05
    wait = 100
    nPt_gaus = 50

    # Record the current sample position:
    curr_Motor_pos = Motor.get()

    # Record the current ccd bin values:
    curr_bin_status = pv.ccd_binning.get()

    # Define the vector containing Motor positions to be scanned:
    vect_pos_x = np.linspace(X_start, X_end, n_steps)

    # Define the intensity vectors where intensity values will be stored:
    intensity = np.arange(0,np.size(vect_pos_x),1)

    # Set the CCD acquisition time:
    pv.ccd_dwell_time.put(acq_time, wait=True, timeout=wait)
    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0, wait=True, timeout=wait)
    # CCD binning
    pv.ccd_binning.put(4, wait=True, timeout=wait) # state = 5 --> 8x8 bin

    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol

    ########################### START THE KNIFE EDGE SCAN
    # Move the knife edge to the X starting point
    Motor.put(vect_pos_x[0], wait=True)
    pv.ccd_trigger.put(1, wait=True, timeout=wait) # trigger once fisrt to avoid a reading bug

    print '*** X knife edge scan starting position: ',(vect_pos_x[0])

    # Start the scan
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i, -- Motor pos: %.3f' % (iLoop+1, np.size(vect_pos_x), vect_pos_x[iLoop])
        Motor.put(vect_pos_x[iLoop], wait=True, timeout=wait)

        sleep(sleeptime) # pause

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])
        img_tmp[np.where(img_tmp < Threshold)] = 0

        # Store the intensity
        intensity[iLoop] = np.sum(img_tmp) # store the intensity

        print '  :: Intensity: ', intensity[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_x(iLoop)))

    pv.ccd_acquire_mode.put(1, wait=True, timeout=wait) # CCD mode switched to continue
    Motor.put(curr_Motor_pos, wait=True, timeout=wait) # move the sample stage back to the first location

    # Come back to the initial CCD binning values:
    pv.ccd_binning.put(curr_bin_status, wait=True, timeout=wait) # state = 5 --> 8x8 bin
    if curr_bin_status==0: # because of the Areadetector bug
        pv.ccd_image_columns.put(2560, wait=True, timeout=wait)

    ################################  DATA PROCESSING
    if 0:
        # Calculate the derivative of the intensity profile:
        deriv_int = np.diff(intensity)
    
        # Noise filtering of intensity profile & its derivative:
        filter_struct = 3
        intensity_filt = filters.median_filter(intensity, footprint=np.ones(filter_struct))
        deriv_int_filt = filters.median_filter(deriv_int, footprint=np.ones(filter_struct))
    
        # Gaussian fit + FWHM estimate:
        deriv_int = np.diff(intensity)
    
        # Gaussian function definition:
        def gaus(x, a, x0, sigma):
            return a*np.exp(-(x-x0)**2/(2*sigma**2))
    
        # Gaussian fitting of the derivative:
        x = vect_pos_x[1:] # resampled because derivative loose one value
        x_HR = np.linspace(x[0], x[-1], nPt_gaus) # higher sampling for the gaussian fit display
        mean_x = np.mean(x)
        sigma = np.std(x)
    
        # Fit a gaussian on the knife edge derivative
        y = deriv_int
        amp = np.max(y)
        try:
            popt = curve_fit(gaus,x,y,p0=[amp,mean_x,sigma])
            param = popt[0]
            sigma1 = param[2]
            deriv_int_fit = gaus(x_HR, param[0], param[1], param[2])
        except (runtimeError, TypeError, NameError):
            deriv_int_fit = deriv_int
            sigma1 = 0
        FWHM_1 = sigma1 * 2.3548
        #--------------------------------------------
    
        # Fit a gaussian on the filtered knife edge derivative
        y = deriv_int_filt
        amp = np.max(y)
        try:
            popt = curve_fit(gaus,x,y,p0=[amp,mean_x,sigma])
            param = popt[0]
            sigma2 = param[2]
            deriv_int_filt_fit = gaus(x_HR, param[0], param[1], param[2])
        except (runtimeError, TypeError, NameError):
            deriv_int_fit = deriv_int
            sigma2 = 0
        FWHM_2 = sigma2 * 2.3548
        #--------------------------------------------
    
        if disp:
            plt.subplot(2,2,1) # knife edge
            plt.plot(vect_pos_x, intensity, 'go-')
            plt.title('Knife edge'), plt.ylabel('Intensity'), plt.grid()
    
            plt.subplot(2,2,3) # knife edge derivative + gaussian fit
            plt.plot(vect_pos_x[1:], deriv_int, 'go--', x_HR, deriv_int_fit, 'r-')
            TheTitle = 'Knife edge derivative; FWHM: %0.2f' % FWHM_1
            plt.title(TheTitle), plt.xlabel('motor position'), plt.ylabel('Intensity'), plt.grid()
    
            plt.subplot(2,2,2) # filtered knife edge
            plt.plot(vect_pos_x, intensity_filt, 'go-')
            plt.title('Filtered knife edge'), plt.ylabel('Intensity'), plt.grid()
    
            plt.subplot(2,2,4) # filtered knife edge derivative + gaussian fit
            plt.plot(vect_pos_x[1:], deriv_int_filt, 'go--', x_HR, deriv_int_filt_fit, 'r-')
            TheTitle = 'Filtered Knife edge derivative; FWHM: %0.2f' % FWHM_2
            plt.title(TheTitle), plt.xlabel('motor position'), plt.ylabel('Intensity'), plt.grid()
    
            plt.show()
    
    return vect_pos_x, intensity, FWHM_2









def knife_edge_zp(X_start, X_end, n_steps, dwelltime, disp):

#   exple: knife_edge_zp(sample_x_bpm, -0.25, 0.05, 15, 2, 0)

    # Pre-defined & set parameters
    ####################################################################
    sleeptime = 0.1
    wait = 50
    nPt_gaus = 50

    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol

    # Record the current jena_y position:
    curr_jena_y_pos = pv.jena_y.get()

    # Define the vector containing jena_y positions to be scanned:
    vect_pos_x = np.linspace(X_start, X_end, n_steps)

    # Define the intensity vectors where intensity values will be stored:
    intensity = np.arange(0,np.size(vect_pos_x),1)

    pv.ion_chamber_auto.put(0, wait=True, timeout=wait) # switch automatic to 1 shot mode
    pv.ion_chamber_dwelltime.put(dwelltime, wait=True, timeout=wait) # assigned the dwell time to the oneshot mode


    ########################### START THE KNIFE EDGE SCAN
    # Move the knife edge to the X starting point
    pv.jena_y.put(vect_pos_x[0], wait=True)
    pv.ion_chamber_trigger.put(1) # trigger once fisrt to avoid a reading bug

    print '*** X knife edge scan starting position: ',(vect_pos_x[0])

    # Start the scan
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i' % (iLoop+1, np.size(vect_pos_x))
        print '    jena_y pos: ',vect_pos_x[iLoop]
        pv.jena_y.put(vect_pos_x[iLoop], wait=True, timeout=wait)

        sleep(sleeptime) # pause

        # Trigger the CCD
        pv.ion_chamber_trigger.put(1, wait=True, timeout=wait)

        # Store the intensity
        intensity[iLoop] = pv.ion_chamber_bpm.get() # store the intensity

        print '  :: Intensity: ', intensity[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_x(iLoop)))

    pv.ion_chamber_auto.put(1, wait=True, timeout=wait) # come back to automatic mode
    pv.jena_y.put(curr_jena_y_pos, wait=True, timeout=wait) # move the sample stage back to the first location


    ################################  DATA PROCESSING
    # Calculate the derivative of the intensity profile:
    deriv_int = np.diff(intensity)

    # Noise filtering of intensity profile & its derivative:
    filter_struct = 3
    intensity_filt = filters.median_filter(intensity, footprint=np.ones(filter_struct))
    deriv_int_filt = filters.median_filter(deriv_int, footprint=np.ones(filter_struct))

    # Gaussian fit + FWHM estimate:
    deriv_int = np.diff(intensity)

    # Gaussian function definition:
    def gaus(x, a, x0, sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))

    # Gaussian fitting of the derivative:
    x = vect_pos_x[1:] # resampled because derivative loose one value
    x_HR = np.linspace(x[0], x[-1], nPt_gaus) # higher sampling for the gaussian fit display
    mean_x = np.mean(x)
    sigma = np.std(x)

    if 1:
        y = deriv_int
        amp = np.max(y)
        popt = curve_fit(gaus,x,y,p0=[amp,mean_x,sigma])
        param = popt[0]
        sigma1 = param[2]
        deriv_int_fit = gaus(x_HR, param[0], param[1], param[2])
        FWHM_1 = sigma1 * 2.3548

        y = deriv_int_filt
        amp = np.max(y)
        popt = curve_fit(gaus,x,y,p0=[amp,mean_x,sigma])
        param = popt[0]
        sigma2 = param[2]
        deriv_int_filt_fit = gaus(x_HR, param[0], param[1], param[2])
        FWHM_2 = sigma2 * 2.3548

    if disp:
        plt.subplot(2,2,1) # knife edge
        plt.plot(vect_pos_x, intensity, 'go-')
        plt.title('Knife edge'), plt.ylabel('Intensity'), plt.grid()
        
        plt.subplot(2,2,3) # knife edge derivative + gaussian fit
        plt.plot(vect_pos_x[1:], deriv_int, 'go--', x_HR, deriv_int_fit, 'r-')
        TheTitle = 'Knife edge derivative; FWHM: %0.2f' % FWHM_1
        plt.title(TheTitle), plt.xlabel('jena_y position'), plt.ylabel('Intensity'), plt.grid()

        plt.subplot(2,2,2) # filtered knife edge
        plt.plot(vect_pos_x, intensity_filt, 'go-')
        plt.title('Filtered knife edge'), plt.ylabel('Intensity'), plt.grid()

        plt.subplot(2,2,4) # filtered knife edge derivative + gaussian fit
        plt.plot(vect_pos_x[1:], deriv_int_filt, 'go--', x_HR, deriv_int_filt_fit, 'r-')
        TheTitle = 'Filtered Knife edge derivative; FWHM: %0.2f' % FWHM_2
        plt.title(TheTitle), plt.xlabel('jena_y position'), plt.ylabel('Intensity'), plt.grid()

        plt.show()

#    return x_HR, intensity_int, FWHM_2
    return intensity_filt
