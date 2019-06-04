Motor = sample_rotary
nAngles = 721; nScan = 100 # scan parameters
exposure = 3 # sec/local/data/2015_07/IUPUI/test2dyonds



############################################
# Set the CCD acquisition time:
pv.ccd_dwell_time.put(exposure, wait=True, timeout=100)
# CCD mode switched to fixed
pv.ccd_acquire_mode.put(0, wait=True, timeout=100)


curr_pos = Motor.get()
theRange = 180
scan_val = np.linspace(curr_pos, curr_pos+theRange, nAngles)

time_st = time.time()

for iScan in range(0, nScan):
    for iAngle in range(0, nAngles):

        print '*** Scan #%i/%i, step %i/%i' % (iScan+1, nScan, iAngle+1, nAngles)
        print '    Rotary stage angle:  %0.4f' % scan_val[iAngle]
        Motor.put(scan_val[iAngle], wait=True, timeout=100)
 
       # Trigger the CCD
#        pv.ccd_trigger.put(1, wait=True, timeout=100)
#        while pv.ccd_detector_state.get() != 0: time.sleep(0.05)
        sleep(exposure)
        curr_time = time.time()
        print ' ..... time spent: %02.2f min' % ((curr_time - time_st)/60)
        print ' '

