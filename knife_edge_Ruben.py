# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 19:04:17 2015

@author: usr32idc
"""
output_path = '/local/data/2015_10/commissioning/beamline_charact/hscan_noCRL_nocond_0p5s.txt'
#knife_edge(sample_y, 0, 0.5, 20, 0.1, diode, output_path, 1)
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
