# -*- coding: utf-8 -*-
#"""
#Created on Tue Apr  1 16:00:45 2014
#
#@author: vdeandrade
#"""


def rocking_curve():

    ########################### input ###############################
    sleeptime = 2.5 # time to wait in order to register the intensity
    nSteps = 10
    range_scanned = 10
    nPt_interp = 50
    wait = 100
    #################################################################

    # get the current position of the DCM 2nd crystal piezo:
    curr_pos = pv.pzt_sec_crystal.get()

    # Initialization of variables (scaning range, intensity vector)
    scan_val = np.linspace(curr_pos - range_scanned/2, curr_pos + range_scanned/2, nSteps)
    intensity = scan_val*0

    pv.ion_chamber_auto.put(0, wait=True, timeout=wait) # switch automatic to 1 shot mode
    dwelltime = pv.ion_chamber_autodwelltime.get() # get the dwell time of the auto mode
    pv.ion_chamber_dwelltime.put(dwelltime, wait=True, timeout=wait) # assigned the dwell time to the oneshot mode
    pv.ion_chamber_trigger.put(1) # trigger once fisrt to avoid a reading bug

    # Loop acquiring the rocking curve:
    for i in range(0, np.size(scan_val)):
        print '*** Step %i/%i' % (i+1, np.size(scan_val))
        print '    Motor pos: ',scan_val[i]
        pv.pzt_sec_crystal.put(scan_val[i], wait=True, timeout=wait)
        sleep(sleeptime)
        pv.ion_chamber_trigger.put(1)
        intensity[i] = pv.ion_chamber_DCM.get()
        print intensity[i]

    pv.ion_chamber_auto.put(1, wait=True, timeout=wait) # come back to automatic mode

    # Interpolate the rocking curve over 50 points
    f = interpolate.interp1d(scan_val, intensity, kind='cubic')
    scan_val_interp = np.linspace(scan_val[0], scan_val[-1], nPt_interp)
    intensity_interp = f(scan_val_interp)

    # Get the motor position with the max intensity on the interpolated data:
    index_max_intensity = np.where(intensity_interp==max(intensity_interp))

    # Move the 2nd crystal at the max intensity of the rocking curve:
    pv.pzt_sec_crystal.put(scan_val_interp[index_max_intensity], wait=True, timeout=wait)

    if 0:
        plt.plot(scan_val, intensity, 'go', scan_val_interp, intensity_interp, 'r-'), plt.grid()
        plt.plot(scan_val_interp[index_max_intensity], max(intensity_interp), 'b*')
        plt.xlabel('Crystal pos. (arcsec)'), plt.ylabel('Intensity')
        plt.title('Rocking curve of the 2nd DCM crystal')
        plt.show()

    return
