
import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import ndimage
from time import *

# INPUT ---------------------------------
n_zone_plate_step = 10
ZP_z_start = -0.1
ZP_z_end = 0.1
acq_time = 15
#----------------------------------------

# CCD parameters
nRow = pv.ccd_image_rows.get()
nCol = pv.ccd_image_columns.get()
image_size = nRow * nCol # size of the snapshot

# Record the current sample position:
curr_ZP_z_pos = pv.zone_plate_z.get()

# Define the vector containing Motor positions to be scanned:
vect_pos_z = np.linspace(zone_plate_z_start, zone_plate_z_end, n_zone_plate_step)

print '*** Start the ZP focusing: '
# move the Zone Plate to the Z starting point
pv.zone_plate_z.put(vect_pos_z[0], wait=True)

pv.ccd_dwell_time.put(acq_time) # Set the dwell time 
pv.ccd_trigger.put(0, wait=True, timeout=500) # stop CCD acquisitions
pv.ccd_acquire_mode.put(0, wait=True, timeout=500) # CCD mode switched to fixed

pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger once fisrt to avoid a reading bug

for iLoop in range(0, n_zone_plate_step):
    print '::: Knife edge # %i/%i' % (iLoop+1, np.size(vect_pos_z))
    print '    Motor pos: ',vect_pos_z[iLoop]
    sleep(sleeptime)
    pv.zone_plate_z.put(vect_pos_z[iLoop], wait=True, timeout=100)
    
    pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])
    



