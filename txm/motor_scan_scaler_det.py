
## DOESN'T WORK YET, IN DEVELOPMENT!!
from epics import PV

rot_diamond = PV('32idcTMP:PIC867:2:P1_drive.VAL')
ascan(rot_diamond, 49.09, 49.20, 21, 1, 1)

def ascan(Motor, pos_start, pos_end, n_steps, acq_time, disp):
#
#   script: ascan(PV_motor, X_start, X_end, n_steps, acq_time, disp)
#        - PV_motor: 
#        - pos_start: 
#        - pos_end:
#        - n_steps: # of steps during the scan
#        - acq_time: acquisition time in seconds
#        - disp: 0= no dislay, 1= display
#
#   exple: ascan(condenser_z, -0.25, 0.05, 15, 2, 0)

    # Pre-defined & set parameters
    ####################################################################
    sleeptime = 0.2
    wait = 100

    # Define det / scaler PVs:
    scaler = PV('32idc01:scaler1.S7') #  downstream
    scaler_trigger = PV('32idc01:scaler1.CNT')
    scaler_auto = PV('32idc01:scaler1.CONT')
    scaler_dwelltime = PV('32idc01:scaler1.TP')

    ############################ play with the ion chambers #############################
    dwelltime = pv.scaler_dwelltime.get() # get the dwell time of the auto mode
    pv.scaler_dwelltime.put(acq_time, wait=True, timeout=wait) # assigned the dwell time to the oneshot mode
    
    print 'Switch ion chamber on OneShot mode'
    pv.scaler_auto.put(0, wait=True, timeout=wait) # switch automatic to 1 shot mode
    print 'Done!'
    
    print 'Trigger ion chamber once'
    pv.scaler_trigger.put(1, wait=True, timeout=wait)
    ####################################################################################

    # Record the current sample position:
    curr_pos = Motor.get()


    # Define the vector containing Motor positions to be scanned:
    vect_pos_x = np.linspace(pos_start, pos_end, n_steps)

    # Define the intensity vectors where intensity values will be stored:
    intensity = np.arange(0,np.size(vect_pos_x),1)


    ########################### START THE KNIFE EDGE SCAN
    # Move the knife edge to the X starting point
    pv.sample_x.put(vect_pos_x[0], wait=True)
    pv.ccd_trigger.put(1, wait=True, timeout=wait) # trigger once fisrt to avoid a reading bug

    print '*** Scan starting position: ',(vect_pos_x[0])

    # Start the scan
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i' % (iLoop+1, np.size(vect_pos_x))
        print '    Motor pos: ',vect_pos_x[iLoop]
        Motor.put(vect_pos_x[iLoop], wait=True, timeout=wait)

        sleep(sleeptime) # pause

        pv.scaler_trigger.put(1, wait=True)
        wait_pv(scaler_trigger, 0)
    
        intensity[iLoop,1] = pv.scaler.get()
        print intensity[iLoop,1]

        # Store the intensity
        intensity[iLoop] = np.sum(img_tmp) # store the intensity

        print '  :: Intensity: ', intensity[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_x(iLoop)))

    plt.plot(vect_pos_x, intensity, 'go-')
    plt.title('X'), plt.ylabel('Intensity'), plt.grid()
    plt.show()

    return vect_pos_x_int, intensity_int, FWHM_2


