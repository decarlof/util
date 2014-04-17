

import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import ndimage
from time import *

def knife_edge(X_start, X_end, n_steps, acq_time):

#   exple: knife_edge(-0.25, 0.05, 15, 2)

    sleeptime = 1

    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol

    # Record the current sample position:
    curr_SpleX_pos = pv.sample_x.get()

    # Define the vector containing Motor positions to be scanned:
    vect_pos_x = np.linspace(X_start, X_end, n_steps)

    # Define the intensity vectors where intensity values will be stored:
    intensity_x = np.arange(0,np.size(vect_pos_x),1)

    # Set the dwell time:    
    pv.ccd_dwell_time.put(acq_time, wait=True, timeout=100)
    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0, wait=True, timeout=100)

    ######################################
    # start the knife edge scan
    # move the knife edge to the X starting point
    pv.sample_x.put(vect_pos_x[0], wait=True)
    pv.ccd_trigger.put(1, wait=True, timeout=100) # trigger once fisrt to avoid a reading bug

    print '*** X knife edge scan starting position: ',(vect_pos_x[0])

    for iLoop in range(0, n_steps):
        print '*** Step %i/%i' % (iLoop+1, np.size(vect_pos_x))
        print '    Motor pos: ',vect_pos_x[iLoop]
        pv.sample_x.put(vect_pos_x[iLoop], wait=True, timeout=100)

        sleep(sleeptime)

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=100)

        # Get the image loaded in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        # Store the intensity
        intensity_x[iLoop] = np.sum(img_tmp) # store the intensity

        print '  :: Intensity: ', intensity_x[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_x(iLoop)))

    pv.sample_x.put(curr_SpleX_pos, wait=True, timeout=100)

    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_x, intensity_x, kind='cubic')
    vect_pos_x_int = np.linspace(vect_pos_x[0], vect_pos_x[-1], 50)
    intensity_x_int = f(vect_pos_x_int)

    plt.plot(vect_pos_x, intensity_x, 'go', vect_pos_x_int, intensity_x_int, 'r-'), plt.grid()
#    plt.plot(vect_pos_x, intensity_x, 'go'), plt.grid()
    plt.title('Knife edge')
    plt.show()

    return vect_pos_x_int, intensity_x_int


