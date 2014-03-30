# -*- coding: utf-8 -*-

import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def align_bpm(x_range, y_range, steps, dwell_time):
    """
    align_bpm
    
    Parameters
    ----------
    X_range : float
    Y_range : float
    steps: number of steps inside the scanned range
    dwell_time: dwell time for the CCD acquisition
    """
    
    # Work on a ROI
    ROI=0

    # Variables creation:
    ROI_pixH = [400, 2300]
    ROI_pixV = [620, 1900]
    ROI_pixH = [1300, 1500]
    ROI_pixV = [800, 1000]
    nVPix = pv.ccd_image_rows.get()
    nHPix = pv.ccd_image_columns.get()
    print nVPix, nHPix

    image_size = nVPix * nHPix
    #if ROI:
        #Mat3D = np.zeros((steps, (ROI_pixV[1]-ROI_pixV[0]), (ROI_pixH[1]-ROI_pixH[0])), np.int16)
    #else:
    # Initialize the 3D matrix
    mat_3d_x = np.zeros((steps, nVPix, nHPix), np.int16) 
    mat_3d_y = mat_3d_x

    # Get the current focus position
    curr_BPMY_pos = pv.beam_monitor_y.get()

    # Define the vector containing angles
    vect_pos_y = np.linspace(curr_BPMY_pos - y_range/2, curr_BPMY_pos + y_range/2, steps)

    # get the delta angle
#    delta_step_Y = abs(vect_pos_y[1] - vect_pos_y[0])                       
    intensity_y = np.arange(0,np.size(vect_pos_y),1)

    # Det the current focus position
    curr_BPMX_pos = pv.beam_monitor_x.get() 

    # Define the vector containing angles
    vect_pos_x = np.linspace(curr_BPMX_pos - x_range/2, curr_BPMX_pos + x_range/2, steps)

    # Get the delta angle
    #delta_step_X = abs(vect_pos_x[1] - vect_pos_x[0])                       
    intensity_x = np.arange(0,np.size(vect_pos_x),1)

    pv.ccd_dwell_time.put(dwell_time)  

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0) 

    ######################################
    # start the Y BPM scan

    # move the BPM to the Y starting point
    pv.beam_monitor_y.put(vect_pos_y[0], wait=True)
    print '*** Y BPM scan tarting position: ',(vect_pos_y[0])

    for iLoop in range(0, steps):
        print '*** Step %i/%i' % (iLoop+1, np.size(vect_pos_y))
        print '    Motor pos: ',vect_pos_y[iLoop]
        pv.beam_monitor_y.put(vect_pos_y[iLoop], wait=True, timeout=500)

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=500)

        # Get the image still in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nVPix, nHPix])

        # Store the image in Mat3D
        mat_3d_y[iLoop,:,:] = img_tmp            

        if ROI:
#           im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            im = mat_3d_y[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            im = mat_3d_y[iLoop,:,:]

        intensity_y[iLoop] = np.sum(im) # store the intensity

        # Store the intensity
        tmp = np.sum(im)
        print tmp
        
        # Not sure what this is for:
        #tmp[np.where(tmp < 250)] = 0
        
        print 'Intensity: ', intensity_y[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_y(iLoop)))

    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_y, intensity_y, kind='cubic')
    vect_pos_y_int = np.linspace(vect_pos_y[0], vect_pos_y[-1], 50)
    intensity_y_int = f(vect_pos_y_int)

    # Get the motor position with the max intensity:
    index_max_intensity = np.where(intensity_y==max(intensity_y))

    print '*** Best Y position at ', vect_pos_y_int[index_max_intensity]

    plt.plot(vect_pos_y, intensity_y, 'go', vect_pos_y_int, intensity_y_int, 'r-'), plt.grid()
    plt.plot(vect_pos_y_int[index_max_intensity], max(intensity_y_int), 'b*')
    plt.title('Standard deviation for different Y BPM positions')
    plt.show()

    # Move to the optimum Y position:
    pv.beam_monitor_y.put(vect_pos_y_int[index_max_intensity], wait=True, timeout=500)

    # Make a last snapshot
    pv.ccd_trigger.put(1, wait=True, timeout=500) 


    ######################################
    # Start the X BPM scan

    # Move the BPM to the X starting point
    pv.beam_monitor_x.put(vect_pos_x[0], wait=True)
    print '*** X BPM scan tarting position: ',(vect_pos_x[0])

    for iLoop in range(0, steps):
        print '*** Step %i/%i' % (iLoop+1, np.size(vect_pos_x))
        print '    Motor pos: ',vect_pos_x[iLoop]
        pv.beam_monitor_x.put(vect_pos_x[iLoop], wait=True, timeout=500)

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=500)

        # gGet the image still in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nVPix, nHPix])

        # Store the image in Mat3D
        mat_3d_x[iLoop,:,:] = img_tmp            

        if ROI:
#           im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            im = mat_3d_x[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            im = mat_3d_x[iLoop,:,:]

        intensity_x[iLoop] = np.sum(im) # store the intensity

        # Store the intensity
        tmp = np.sum(im)
        print tmp
        
        # not sure what this is for:
        #tmp[np.where(tmp < 250)] = 0
        
        print 'Intensity: ', intensity_x[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_y(iLoop)))

    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_x, intensity_x, kind='cubic')
    vect_pos_x_int = np.linspace(vect_pos_x[0], vect_pos_x[-1], 50)
    intensity_x_int = f(vect_pos_x_int)

    # Get the motor position with the max intensity:
    index_max_intensity = np.where(intensity_x==max(intensity_x))

    print '*** Best X position at ', vect_pos_x_int[index_max_intensity]

    plt.plot(vect_pos_x, intensity_x, 'go', vect_pos_x_int, intensity_x_int, 'r-'), plt.grid()
    plt.plot(vect_pos_x_int[index_max_intensity], max(intensity_x_int), 'b*')
    plt.title('Standard deviation for different X BPM positions')
    plt.show()

    # Move to the optimum X position:
    pv.beam_monitor_x.put(vect_pos_x_int[index_max_intensity], wait=True, timeout=500)

    # Make a last snapshot
    pv.ccd_trigger.put(1, wait=True, timeout=500)

    return mat_3d_y, intensity_y_int, vect_pos_y, vect_pos_x_int, mat_3d_x, intensity_x_int, vect_pos_x, vect_pos_x_int

#import matplotlib.pylab as plt
#plt.ion()
#img = plt.imread('radio_16.tiff')
#plt.imshow(img), plt.set_cmap('jet'), plt.colorbar()
#plt.set_cmap('hot')
#plt.colorbar()
#plt.hist(lum_img.flatten(), 256, range=(0.0,1.0), fc='k', ec='k')
#plt.clim(0.0,0.7)
#rsize = img.resize((img.size[0]/10,img.size[1]/10)) # Use PIL to resize
#rsizeArr = np.asarray(rsize)  # Get array back
#imgplot = plt.imshow(rsizeArr)


# COMMAND LINE EXAMPLES:
# os.getcwd()
# os.listdir('.')
# os.chdir("dir path or name")
# os.makedirs('dir name')
# os.removedirs(path)
# execfile("Startup.py")
# execfile("file name",global_vars,local_vars)


if __name__ == "__main__":
    align_bpm(3, 3, 5, 1)
