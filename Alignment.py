# -*- coding: utf-8 -*-

import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import ndimage

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
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    #print nRow, nCol

    image_size = nRow * nCol
    #if ROI:
        #Mat3D = np.zeros((steps, (ROI_pixV[1]-ROI_pixV[0]), (ROI_pixH[1]-ROI_pixH[0])), np.int16)
    #else:
    # Initialize the 3D matrix
    mat_3d_x = np.zeros((steps, nRow, nCol), np.int16) 
    mat_3d_y = mat_3d_x

    # Get the current BPM position
    curr_BPMY_pos = pv.beam_monitor_y.get()
    curr_BPMX_pos = pv.beam_monitor_x.get() 

    # Define the vector containing Motor positions to be scanned:
    vect_pos_y = np.linspace(curr_BPMY_pos - y_range/2, curr_BPMY_pos + y_range/2, steps)
    vect_pos_x = np.linspace(curr_BPMX_pos - x_range/2, curr_BPMX_pos + x_range/2, steps)

    # Define the intensity vectors where intensity values will be stored:
    intensity_y = np.arange(0,np.size(vect_pos_y),1)
    intensity_x = np.arange(0,np.size(vect_pos_x),1)

    # Set the dwell time:    
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
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        # Store the image in Mat3D
        mat_3d_y[iLoop,:,:] = img_tmp            

        if ROI:
#           im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            im = mat_3d_y[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            im = mat_3d_y[iLoop,:,:]

        # Store the intensity
        intensity_y[iLoop] = np.sum(im) # store the intensity

        print 'Intensity: ', intensity_y[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_y(iLoop)))

    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_y, intensity_y, kind='cubic')
    vect_pos_y_int = np.linspace(vect_pos_y[0], vect_pos_y[-1], 50)
    intensity_y_int = f(vect_pos_y_int)

    # Get the motor position with the max intensity:
    index_max_intensity = np.where(intensity_y_int==max(intensity_y_int))

    print '*** Best Y position at ', vect_pos_y_int[index_max_intensity]

    plt.plot(vect_pos_y, intensity_y, 'go', vect_pos_y_int, intensity_y_int, 'r-'), plt.grid()
    plt.plot(vect_pos_y_int[index_max_intensity], max(intensity_y_int), 'b*')
    plt.title('Standard deviation for different Y BPM positions')
    plt.show()

    # Move to the optimum Y position:
    pv.beam_monitor_y.put(vect_pos_y_int[index_max_intensity], wait=True, timeout=500)
    pv.beam_monitor_y_set.put(1) # switch to set mode
    pv.beam_monitor_y.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.beam_monitor_y_set.put(0) # switch to use mode

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
        img_tmp = np.reshape(img_vect,[nRow, nCol])

        # Store the image in Mat3D
        mat_3d_x[iLoop,:,:] = img_tmp            

        if ROI:
#           im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            im = mat_3d_x[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            im = mat_3d_x[iLoop,:,:]

        # Store the intensity
        intensity_x[iLoop] = np.sum(im) # store the intensity

        print 'Intensity: ', intensity_x[iLoop]
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos_y(iLoop)))

    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_x, intensity_x, kind='cubic')
    vect_pos_x_int = np.linspace(vect_pos_x[0], vect_pos_x[-1], 50)
    intensity_x_int = f(vect_pos_x_int)

    # Get the motor position with the max intensity:
    index_max_intensity = np.where(intensity_x_int==max(intensity_x_int))

    print '*** Best X position at ', vect_pos_x_int[index_max_intensity]

    plt.plot(vect_pos_x, intensity_x, 'go', vect_pos_x_int, intensity_x_int, 'r-'), plt.grid()
    plt.plot(vect_pos_x_int[index_max_intensity], max(intensity_x_int), 'b*')
    plt.title('Standard deviation for different X BPM positions')
    plt.show()

    # Move to the optimum X position:
    pv.beam_monitor_x.put(vect_pos_x_int[index_max_intensity], wait=True, timeout=500)
    pv.beam_monitor_x_set.put(1) # switch to set mode
    pv.beam_monitor_x.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.beam_monitor_x_set.put(0) # switch to use mode

    # Make a last snapshot
    pv.ccd_trigger.put(1, wait=True, timeout=500)

    return mat_3d_y, intensity_y_int, vect_pos_y, vect_pos_x_int, mat_3d_x, intensity_x_int, vect_pos_x, vect_pos_x_int


#if __name__ == "__main__":
#    align_bpm(3, 3, 5, 1)



#####################################
#####################################
def align_CCD():
    """
    align_CCD: aligned a CCD on the gravity center of the current image. Is supposed to be launched 
    with a pinhole in.
    
    Parameters
    ----------
    No input required
    """
    
    # Check the magnification lens:
    Objective_pos = np.round(pv.ccd_camera_objective.get())
    if Objective_pos==-40:
        Pix_size = 6.5/1.25/1000 # mm
        print '1X mag'
    elif Objective_pos==0:
        Pix_size = 6.5/5/1000 # mm
        print '5X mag'
    else:
        Pix_size = 6.5/20/1000 # mm
        print '20X mag'
        

    Threshold = 200 # threshold on pixel below which intensity is considered as noise and set to 0
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol # size of the snapshot
    CCD_center_X = np.round(nCol/2) # X coordinates of the image center
    CCD_center_Y = np.round(nRow/2) # Y coordinates of the image center
    print "CCD_center_X", CCD_center_X
    print "CCD_center_Y", CCD_center_Y

   # Set the dwell time:    
    pv.ccd_dwell_time.put(0.05)
 
    # Get the current CCD position
    curr_CCDY_pos = pv.ccd_camera_y.get()
    curr_CCDX_pos = pv.ccd_camera_x.get() 

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0)

    # Trigger the CCD & get the image 
    pv.ccd_trigger.put(1, wait=True, timeout=500)
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])

##    # Image centroid calculation
##    img_tmp[np.where(img_tmp < Threshold)] = 0; # attribute 0 to pixels with intensity < threshold
##    [X,Y] = np.meshgrid(np.arange(1,nCol+1), np.arange(1,nRow+1))	# used for the centroid calculation
##    centX = np.sum(np.multiply(img_tmp,X)/np.sum(img_tmp));
##    centY = np.sum(np.multiply(img_tmp,Y)/np.sum(img_tmp));
    center = ndimage.measurements.center_of_mass(img_tmp)
    print center

    CCD_center_X = center[0]
    CCD_center_Y = center[1]
    
    # Calculate the distance in pixel between the CCD center and the Intenisty gravity center
    Diff_X = centX - CCD_center_X
    Diff_Y = centY - CCD_center_Y

    # Calculate the distance in mm between the CCD center and the Intenisty gravity center
    CCD_Xpos = curr_CCDX_pos + Diff_X * Pix_size
    CCD_Ypos = curr_CCDY_pos + Diff_Y * Pix_size

    # Center the CCD in X & Y on the intensity gravity center
    pv.ccd_camera_x.put(CCD_Xpos, wait=True, timeout=500)
    #pv.ccd_camera_x_set.put(1) # switch to set mode
    pv.ccd_camera_x.put(0, wait=True, timeout=500) # reinitialize position to 0
#    pv.ccd_camera_x_set.put(0) # switch to use mode
    
    pv.ccd_camera_y.put(CCD_Ypos, wait=True, timeout=500)
#    pv.ccd_camera_y_set.put(1) # switch to set mode
    pv.ccd_camera_y.put(0, wait=True, timeout=500) # reinitialize position to 0
 #   pv.ccd_camera_y_set.put(0) # switch to use mode
    
    pv.ccd_trigger.put(1, wait=True, timeout=500) # Trigger the CCD

    return


def align_cond_xy():
    """
    align_cpndxy: aligned the condenser on the center of the CCD. Is supposed to be launched 
    with a pinhole in.
    
    Parameters
    ----------
    No input required
    """


    # Check the magnification lens:
    Objective_pos = np.round(pv.ccd_camera_objective.get())
    if Objective_pos==-40:
        Pix_size = 6.5/1.25/1000 # mm
    elif Objective_pos==0:
        Pix_size = 6.5/5/1000 # mm
    else:
        Pix_size = 6.5/20/1000 # mm

    Threshold = 200 # threshold on pixel below whose intensity is considered as noise and set to 0
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol # size of the snapshot
    CCD_center_X = np.round(nCol/2) # X coordinates of the image center
    CCD_center_Y = np.round(nRow/2) # Y coordinates of the image center

   # Set the dwell time:    
    pv.ccd_dwell_time.put(0.05) # 50 ms

    # Get the current condenser position
    curr_condY_pos = pv.condenser_y.get()
    curr_condX_pos = pv.condenser_x.get() 

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0)

    # Trigger the CCD & get the image 
    pv.ccd_trigger.put(1, wait=True, timeout=500)
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])

    # Image centroid calculation
    img_tmp[np.where(img_tmp < Threshold)] = 0; # attribute 0 to pixels with intensity < threshold
    [X,Y] = np.meshgrid(np.arange(1,nCol+1), np.arange(1,nRow+1))	# used for the centroid calculation
    centX = np.sum(np.multiply(img_tmp,X)/np.sum(img_tmp));
    centY = np.sum(np.multiply(img_tmp,Y)/np.sum(img_tmp));

    # Calculate the distance in pixel between the CCD center and the Intenisty gravity center
    Diff_X = centX - CCD_center_X
    Diff_Y = centY - CCD_center_Y

    # Calculate the distance in mm between the CCD center and the Intenisty gravity center
    cond_Xpos = curr_condX_pos + Diff_X * Pix_size
    cond_Ypos = curr_condY_pos + Diff_Y * Pix_size

    # Center the condenser in X & Y on the intensity gravity center
    pv.condenser_x.put(cond_Xpos, wait=True, timeout=500)
    pv.condenser_x_set.put(1) # switch to set mode
    pv.condenser_x.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.condenser_x_set.put(0) # switch to use mode
    
    pv.condenser_y.put(cond_Ypos, wait=True, timeout=500)
    pv.condenser_y_set.put(1) # switch to set mode
    pv.condenser_y.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.condenser_y_set.put(0) # switch to use mode
    
    pv.ccd_trigger.put(1, wait=True, timeout=500) # Trigger the CCD

    return


def align_pinhole():
    """
    align_cpndxy: aligned the condenser on the center of the CCD. Is supposed to be launched 
    with a pinhole in.
    
    Parameters
    ----------
    No input required
    """

    # Check the magnification lens:
    Objective_pos = np.round(pv.ccd_camera_objective.get())
    if Objective_pos==-40:
        Pix_size = 6.5/1.25/1000 # mm
    elif Objective_pos==0:
        Pix_size = 6.5/5/1000 # mm
    else:
        Pix_size = 6.5/20/1000 # mm

    Threshold = 200 # threshold on pixel below whose intensity is considered as noise and set to 0
    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol # size of the snapshot
    CCD_center_X = np.round(nCol/2) # X coordinates of the image center
    CCD_center_Y = np.round(nRow/2) # Y coordinates of the image center

   # Set the dwell time:    
    pv.ccd_dwell_time.put(0.05) # 50 ms

    # Get the current condenser position
    curr_pinholeY_pos = pv.pin_hole_y.get()
    curr_pinholeX_pos = pv.pin_hole_x.get() 

    # CCD mode switched to fixed
    pv.ccd_acquire_mode.put(0)

    # Trigger the CCD & get the image 
    pv.ccd_trigger.put(1, wait=True, timeout=500)
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])

    # Image centroid calculation
    img_tmp[np.where(img_tmp < Threshold)] = 0; # attribute 0 to pixels with intensity < threshold
    [X,Y] = np.meshgrid(np.arange(1,nCol+1), np.arange(1,nRow+1))	# used for the centroid calculation
    centX = np.sum(np.multiply(img_tmp,X)/np.sum(img_tmp));
    centY = np.sum(np.multiply(img_tmp,Y)/np.sum(img_tmp));

    # Calculate the distance in pixel between the CCD center and the Intenisty gravity center
    Diff_X = centX - CCD_center_X
    Diff_Y = centY - CCD_center_Y

    # Calculate the distance in mm between the CCD center and the Intenisty gravity center
    cond_Xpos = curr_pinholeX_pos + Diff_X * Pix_size
    cond_Ypos = curr_pinholeY_pos + Diff_Y * Pix_size

    # Center the pinhole in X & Y on the intensity gravity center
    pv.pin_hole_x.put(cond_Xpos, wait=True, timeout=500)
    pv.pin_hole_x_set.put(1) # switch to set mode
    pv.pin_hole_x.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.pin_hole_x_set.put(0) # switch to use mode
    
    pv.pin_hole_y.put(cond_Ypos, wait=True, timeout=500)
    pv.pin_hole_y_set.put(1) # switch to set mode
    pv.pin_hole_y.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.pin_hole_y_set.put(0) # switch to use mode
    
    pv.ccd_trigger.put(1, wait=True, timeout=500) # Trigger the CCD

    return

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
