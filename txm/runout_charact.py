
# Work once libraries are imported from startup.m

#---------------------------- Input -----------------------------
#################################################################
# flat-field on the fly correction must be activated!!
Motor = sample_rotary
acq_time = 0.3
nAngles = 180; theRange = 360; nScan = 3 # scan parameters
filter_struct = [3,3] # for the median filter on the radiograph
output_path = '/local/data/2014_11/TXM_commissioning/runout/180proj_3scans_0.3s_10X_8keV_goodrot/'

# Pre-defined & set parameters
sleeptime = 0.0 # time to wait in order to register the stand_dev
wait = 100
#################################################################
#----------------------------------------------------------------

radix = 'runout_%iproj_%2.1fs' % (nAngles, acq_time)

# move the rotary stage to home position:
#pv.sample_rotary_home.put(1, wait=True, timeout=wait)

# Get the current position of the rotary stage:
curr_pos = Motor.get()
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
pv.ccd_Image_number.put(1, wait=True, timeout=wait)

# Initialization of variables (scanning range, intensity vector)
scan_val = np.linspace(curr_pos, curr_pos+theRange, nAngles)
stand_dev = scan_val*0
gravity = np.zeros((nAngles, 2, nScan)) # col1=X, col2=y, dim3=scan #



###############
# 1st loop repeat the measurements to assess the repeatability of the stage:
for iScan in range(0, nScan):

    # 2nd loop on the angles
    for iAngle in range(0, nAngles):

        print '*** Scan #%i/%i, step %i/%i' % (iScan+1, nScan, iAngle+1, nAngles)
        print '    Rotary stage angle:  %04.6f', scan_val[iAngle]
        Motor.put(scan_val[iAngle], wait=True, timeout=wait)
        sleep(sleeptime)

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=wait)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        FileName = output_path+radix+'_scan%i_%04i.tif' % (iScan, iAngle)
        img = misc.toimage(img_tmp)
        img.save(FileName)

        # filtering
#        img_tmp = filters.median_filter(img_tmp, footprint=np.ones(filter_struct))


        #Im_max = np.max(np.max(img_tmp))
        #Threshold = Im_max*0.25 # threshold on pixel below which intensity is considered as noise and set to 0 (<15% of the max value)

        # Image centroid calculation
        #img_tmp[np.where(img_tmp < Threshold)] = 0; # attribute 0 to pixels with intensity < threshold
        #img_tmp[np.where(img_tmp > Threshold)] = 1; # attribute 1 to pixels with intensity > threshold --> return binary image
#        center = ndimage.measurements.center_of_mass(img_tmp)
#        gravity[iAngle, 0, iScan] = center[1] # centroid X
#       gravity[iAngle, 1, iScan] = center[0] # centroid Y


       
if 0:
    ###### Sine function
    def sine_fun(X, amp, phi, y_offset):
        return amp * np.sin(np.radians(X+ phi)) + y_offset

    avg_traj = np.mean(gravity,axis=2)
    avg_centroX = avg_traj[:,0] # centroid latteral position during rotation
    avg_centroY = avg_traj[:,1] # centroid vertical position during rotation

    # perform the fit for X:
    amp = np.max(avg_centroX)*2
    phi = 1 # pulse: number of periods within 360
    y_offset = np.mean(avg_centroX)
    popt = curve_fit(sine_fun, scan_val, avg_centroX, p0=[amp, phi, y_offset]) # gaussian fit on the derivative of raw data
    fit_param = popt[0]
    amp_fit = fit_param[0]
    phi_fit = fit_param[1]
    y_offset_fit = fit_param[2]

    Sine_fit = sine_fun(scan_val, amp_fit, phi_fit, y_offset_fit)

    # Runout estimate:
    Error_rep_X = avg_centroX - Sine_fit
    Error_nonrep_X = np.std(np.squeeze(gravity[:,0,:]) - avg_centroX)

    Error_rep_Y = avg_centroY - np.median(np.squeeze(gravity[:,1,:]))
    Error_nonrep_Y = np.std(np.squeeze(gravity[:,1,:]) - avg_centroY)

    # Display:
    plt.subplot(2,2,1), plt.plot(scan_val, avg_centroX, 'b.')
    plt.plot(scan_val, Sine_fit, 'r-'), plt.grid()
    plt.xlabel('angular position'), plt.ylabel('X centroid'), plt.grid()
    plt.subplot(2,2,2), plt.plot(scan_val, Error_rep_X, 'b-')
    plt.xlabel('angular position'), plt.ylabel('repeatable error in X'), plt.grid()

    plt.subplot(2,2,3), plt.plot(scan_val, avg_centroY, 'b-'), plt.grid()
    plt.xlabel('angular position'), plt.ylabel('repeatable error in Y'), plt.grid()
    plt.show()



# Matlab code to rename files
#cd /local/dataraid/2014_11/TXM_commissioning/runout/180proj_0.3s/run2cp/
#clear, clc
#
#FileName = 'runout_180proj_0.3s_scan0_0000.tif';
#
#FileNames = dir;
#nRad = length(FileNames)-2;
#nScans = 4;
#
#for iRad = 1:nRad
#    the_file = FileNames(iRad+2).name;
#    scan_index = str2num(the_file(end-7:end-4));
#    renamed_file = [the_file(1:end-8),'xxx',num2str(scan_index),'.tif'];
#    movefile(the_file, renamed_file) 
#end
#
#for iRad = 1:nRad
#    iRad
#    the_file = FileNames(iRad+2).name;
#    scan_index = str2num(the_file(end-4));
#    rad_index = str2num(the_file(25:end-9));
#    renamed_file = [the_file(1:20),'scan',num2str(scan_index),'_',sprintf('%04i',rad_index),'.tif'];
#    movefile(the_file, renamed_file)
#end




