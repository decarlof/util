# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 16:00:45 2014

@author: vdeandrade
"""

import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from time import *
from scipy import interpolate

# get the current position of the DCM 2nd crystal piezo:
curr_pos = pv.pzt_sec_crystal.get()

sleeptime = 2 # time to wait in order to register the intensity

# Initialization of variables (scaning range, intensity vector)
scan_val = np.linspace(curr_pos-6*0.5, curr_pos+6*0.5, 12)
intensity = scan_val*0

# Loop acquiring the rocking curve:
for i in range(0, np.size(scan_val)):
    print '*** Step %i/%i' % (i+1, np.size(scan_val))
    print '    Motor pos: ',scan_val[i]
#    pv.pzt_sec_crystal.put(scan_val[i], wait=True, timeout=500)
    pv.pzt_sec_crystal.put(scan_val[i], wait=True, timeout=500)
    sleep(sleeptime)
    intensity[i] = pv.ion_chamber_DCM.get()

# Interpolate the rocking curve over 50 points
f = interpolate.interp1d(scan_val, intensity, kind='cubic')
scan_val_interp = np.linspace(scan_val[0], scan_val[-1], 50)
intensity_interp = f(scan_val_interp)

# Get the motor position with the max intensity on the interpolated data:
index_max_intensity = np.where(intensity_interp==max(intensity_interp))

# Move the 2nd crystal at the max intensity of the rocking curve:
pv.pzt_sec_crystal.put(scan_val_interp[index_max_intensity], wait=True, timeout=500)

plt.plot(scan_val, intensity, 'go', scan_val_interp, intensity_interp, 'r-'), plt.grid()
plt.plot(scan_val_interp[index_max_intensity], max(intensity_interp), 'b*')
plt.xlabel('Crystal pos. (arcsec)'), plt.ylabel('Intensity')
plt.title('Rocking curve of the 2nd DCM crystal')
plt.show()
