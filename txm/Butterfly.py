


######################### INPUT ##########################
Stage_fast_axis = sample_x
Stage_slow_axis = condenser_z
n_cond_zstep = 40
cond_z_start = -3
cond_z_end = 3

# param for knife-edge scan
detector = diode
knife_xend = -1.35
knife_xstart = -1.15 
knife_nSteps = 25
knife_acq_time = 0.7
disp = 0 # display each knife edge; will pause the scan!!!
output_file = ''
##########################################################

wait_timeout = acq_time + 5 # set timeout time
curr_SpleX_pos = pv.sample_x.get() # Record the current sample position
vect_pos_z = np.linspace(cond_z_start, cond_z_end, n_cond_zstep) # Define the vector containing Motor positions to be scanned
intensities = np.zeros((n_cond_zstep, knife_nSteps)) # Define the intensity matrix where intensity values will be stored
#FWHMs = vect_pos_z*0 # Define the FWHM vector
pv.ccd_acquire_mode.put(0, wait=True, timeout=wait_timeout) # CCD mode switched to fixed

########### START THE 2D SCAN
print '*** Start the butterfly:'
pv.condenser_z.put(vect_pos_z[0], wait=True, timeout=wait_timeout) # Move the Butterfly to the Z starting point
pv.ccd_trigger.put(1, wait=True, timeout=wait_timeout) # trigger once fisrt to avoid a reading bug

for iLoop in range(0, n_cond_zstep):
    print '\n ####################################'
    print '::: Knife edge # %i/%i\n' % (iLoop+1, np.size(vect_pos_z))
    print '    Motor pos: ',vect_pos_z[iLoop]
    Stage_slow_axis.put(vect_pos_z[iLoop], wait=True, timeout=wait_timeout)
    #pv.condenser_z.put(vect_pos_z[iLoop], wait=True, timeout=wait_timeout)

    # Call the knife edge function
    [vect_pos_x_int, intensity, FWHM] = knife_edge(Stage_fast_axis, knife_xstart, knife_xend, knife_nSteps, knife_acq_time, detector)
    intensities[iLoop,:] = intensity
    #FWHMs[iLoop] = FWHM

#    if iLoop<n_cond_zstep-1:
#        plt.show((block=False))
#    else:
#    plt.show()

#index_waist = np.where(FWHMs==np.min(FWHMs)) # find the index of the butterfly waist
#print ' --> Focus @ condenser z posisiton = %.3f ' % vect_pos_z[index_waist]

sio.imsave(output_file, intensities, plugin='tiffile', dtype='uint16')

# Display the map of the Butterfly:
plt.figure
plt.imshow(intensities, cmap='jet', extent = [knife_xstart, knife_xend, vect_pos_z[0], vect_pos_z[-1]], aspect="auto")
plt.xlabel('sample x position'), plt.ylabel('Condenser z pozition'), plt.colorbar()
#plt.subplot(1,2,2), plt.plot(vect_pos_z, FWHMs, 'g-'), plt.grid(), plt.show()



def knife_edge(Motor, pos_start, pos_end, n_steps, acq_time, detector, output_path = None, disp = None):
#   exple: knife_edge(sample_x, -2, 2, 10, 1, diode)

    #sleeptime = 0.05
    wait_timeout = acq_time + 5
    #detector = ion_chamber_DCM
    #detector = diode
    
    curr_Motor_pos = Motor.get()    # Record the current sample position:
    vect_pos_x = np.linspace(pos_start, pos_end, n_steps)    # Define the vector containing Motor positions to be scanned:
    intensity = np.arange(0,np.size(vect_pos_x),1)    # Define the intensity vectors where intensity values will be stored:
    data = np.zeros((np.size(vect_pos_x), 2)) 

    pv.ion_chamber_dwelltime.put(acq_time, wait=True, timeout=wait_timeout) # assigned the dwell time to the oneshot mode
    print 'Switch ion chamber on OneShot mode'
    pv.ion_chamber_auto.put(0, wait=True, timeout=wait_timeout) # switch automatic to 1 shot mode
    print 'Done!'
    print 'Trigger ion chamber once'
    pv.ion_chamber_trigger.put(1, wait=True, timeout=wait_timeout)
    #sleep(acq_time)
    print 'Done!'

    ########################### START THE KNIFE EDGE SCAN
    # Move the knife edge to the X starting point
    Motor.put(vect_pos_x[0], wait=True, timeout=wait_timeout)

    print '*** X knife edge scan starting position: ',(vect_pos_x[0])

    # Start the scan
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i, -- Motor pos: %.3f' % (iLoop+1, np.size(vect_pos_x), vect_pos_x[iLoop])
        Motor.put(vect_pos_x[iLoop], wait=True, timeout=wait_timeout)

        #sleep(sleeptime) # pause
        pv.ion_chamber_trigger.put(1, wait=True, timeout=wait_timeout)
        intensity = detector.get()
        #sleep(acq_time)

        # Store the intensity
        data[iLoop,0] = vect_pos_x[iLoop]
        data[iLoop,1] = intensity # store the intensity

        print ' :: Intensity: ', intensity

    Motor.put(curr_Motor_pos, wait=True, timeout=wait_timeout) # move the sample stage back to the first location

#    np.savetxt(output_path, data, fmt='%4.4f', delimiter='   ', header='col1=pos, col2=intensity')
    if output_path != None:
        np.savetxt(output_path, data, fmt='%4.4f', delimiter='   ')
#    np.savetxt(output_path, np.squeeze(intensity_scan[:,:,i]), fmt='%4.4f', delimiter='   ', header='col1=gap_en, col2=gap pos, col3=DCM_en, col4=bragg position, col5=intensity')


    ################################  DATA PROCESSING
    if disp:
        TheTitle = 'Knife edge'
        plt.plot(data[:,0], data[:,1], 'r.-'), plt.grid()
        plt.title(TheTitle), plt.xlabel('motor position'), plt.ylabel('Intensity'), plt.grid()
        plt.show()
    
    return vect_pos_x, intensity#, FWHM_2


