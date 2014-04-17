
import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import ndimage
from time import *

# INPUT ---------------------------------
n_cond_zstep = 10
cond_z_start = 0
cond_z_end = 0

knife_xstart = -0.25
knife_xend = 0.05
knife_xstep = 15
knife_acq_time = 2
#----------------------------------------


# Record the current sample position:
curr_SpleX_pos = pv.sample_x.get()

# Define the vector containing Motor positions to be scanned:
vect_pos_z = np.linspace(cond_z_start, cond_z_end, n_cond_zstep)

# Define the intensity vectors where intensity values will be stored:
intensities = np.arange(0,np.size(vect_pos_x),n_cond_zstep)


print '*** Start the butterfly: '
# move the Butterfly to the Z starting point
pv.condenser_z.put(vect_pos_z[0], wait=True)
pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger once fisrt to avoid a reading bug

for iLoop in range(0, n_cond_zstep):
    print '::: Knife edge # %i/%i' % (iLoop+1, np.size(vect_pos_z))
    print '    Motor pos: ',vect_pos_z[iLoop]
    pv.condenser_z.put(vect_pos_z[iLoop], wait=True, timeout=100)
    [vect_pos_x_int, intensity_x_int] = knife_edge(knife_xstart, knife_xend, knife_xstep, knife_acq_time)
    intensities[iLoop,:] = intensity_x_int


