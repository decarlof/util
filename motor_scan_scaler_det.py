
from epics import PV
import numpy as np
import time
import matplotlib.pyplot as plt

###################
# Define motors:
#rot_diamond = PV('32idcTMP:PIC867:2:p1_drive.VAL')
rot_diamond = PV('32idcTXM:DAC1_3.VAL')
sample_y = PV('32idcTXM:mcs .VAL')

def ascan(Motor, pos_start, pos_end, n_steps, acq_time):
#
#   script: ascan(PV_motor, X_start, X_end, n_steps, acq_time, disp)
#        - PV_motor: 
#        - pos_start: 
#        - pos_end:
#        - n_steps: # of steps during the scan
#        - acq_time: acquisition time in seconds
#
#   exple: ascan(condenser_z, -0.25, 0.05, 15, 2, 0)

    global intensity
    # Pre-defined & set parameters
    ####################################################################
    sleeptime = 0.5
    wait = 100

    # Define det / scaler PVs:
    scaler = PV('32idc01:scaler1.S2')
    scaler_trigger = PV('32idc01:scaler1.CNT')
    scaler_auto = PV('32idc01:scaler1.CONT')
    scaler_dwelltime = PV('32idc01:scaler1.TP')

    ############################ play with the ion chambers #############################
    dwelltime = scaler_dwelltime.get() # get the dwell time of the auto mode
    scaler_dwelltime.put(acq_time, wait=True, timeout=wait) # assigned the dwell time to the oneshot mode
    
    print 'Switch ion chamber on OneShot mode'
    scaler_auto.put(0, wait=True, timeout=wait) # switch automatic to 1 shot mode
    print 'Done!'
    
    print 'Trigger ion chamber once'
    scaler_trigger.put(1, wait=True, timeout=wait)
    ####################################################################################

    # Record the current sample position:
    curr_pos = Motor.get()


    # Define the vector containing Motor positions to be scanned:
    vect_pos_x = np.linspace(pos_start, pos_end, n_steps)

    # Define the intensity vectors where intensity values will be stored:
    intensity = np.arange(0,np.size(vect_pos_x),1)


    ########################### START THE KNIFE EDGE SCAN
    # Move the knife edge to the X starting point
    Motor.put(vect_pos_x[0], wait=True)

    print '*** Scan starting position: ',(vect_pos_x[0])

    # Start the scan
    for iLoop in range(0, n_steps):
        print '*** Step %i/%i' % (iLoop+1, np.size(vect_pos_x))
        print '    Motor pos: ',vect_pos_x[iLoop]
        Motor.put(vect_pos_x[iLoop], wait=True, timeout=wait)

        sleep(sleeptime) # pause

        scaler_trigger.put(1, wait=True)
        wait_pv(scaler_trigger, 0)
    
        intensity[iLoop] = scaler.get()
        print '  :: Intensity: ', intensity[iLoop]
    
    plt.plot(vect_pos_x, intensity, 'go-')
    plt.title('X'), plt.ylabel('Intensity'), plt.grid()
    plt.show()

    return intensity
    
#wait on a pv to be a value until max_timeout (default forever)
def wait_pv(pv, wait_val, max_timeout_sec=-1):
	print 'wait_pv(', pv.pvname, wait_val, max_timeout_sec, ')'
	#delay for pv to change
	time.sleep(.05)
	startTime = time.time()
	while(True):
		pv_val = pv.get()
		if (pv_val != wait_val):
			if max_timeout_sec > -1:
				curTime = time.time()
				diffTime = curTime - startTime
				if diffTime >= max_timeout_sec:
					return False
			time.sleep(.1)
		else:
			return True
    
#ascan(rot_diamond, 49.09, 49.40, 21, 1)
ascan(rot_diamond, 3, 9.5, 61, 1)

