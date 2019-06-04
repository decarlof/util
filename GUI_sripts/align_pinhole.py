import process_variables as pv
import numpy as np
from scipy import ndimage

def align_pinhole():
    """
    align_pinhole: aligned the condenser on the center of the CCD. Is supposed to be launched 
    with a pinhole in.
    
    Parameters
    ----------
    No input required
    """

    # Check the magnification lens:
    Objective_pos = np.round(pv.ccd_camera_objective.get())
    if Objective_pos==-40:
        Pix_size_H = 1/800.*5/1.25 # motor unit
        Pix_size_V = 1/800.*5/1.25 # motor unit
        print '1.25x mag'
    elif Objective_pos==0:
        Pix_size_H = 1/800. # motor unit
        Pix_size_V = 1/800. # motor unit
        print '5x mag'
    else:
        Pix_size_H = 1/800.*5/10 # motor unit
        Pix_size_V = 1/800.*5/10 # motor unit
        print '10x mag'

    nRow = pv.ccd_image_rows.get()
    nCol = pv.ccd_image_columns.get()
    image_size = nRow * nCol # size of the snapshot
    CCD_center_X = np.round(nCol/2) # X coordinates of the image center
    CCD_center_Y = np.round(nRow/2) # Y coordinates of the image center

    # Get the current condenser position
    curr_phlY_pos = pv.pin_hole_y.get()
    curr_phlX_pos = pv.pin_hole_x.get() 

    # Trigger the CCD & get the image
    pv.ccd_dwell_time.put(0.01) # Set the dwell time at 50 ms
    pv.ccd_trigger.put(0, wait=True, timeout=500) # stop CCD acquisitions
    pv.ccd_acquire_mode.put(0, wait=True, timeout=500) # CCD mode switched to fixed
    pv.ccd_trigger.put(1, wait=True, timeout=500) # makes 1 acquisition
    img_vect = pv.ccd_image.get()
    img_vect = img_vect[0:image_size]
    img_tmp = np.reshape(img_vect,[nRow, nCol])

    Im_max = np.max(np.max(img_tmp))
    Threshold = Im_max*0.25 # threshold on pixel below which intensity is considered as noise and set to 0 (<15% of the max value)

    # Image centroid calculation
    img_tmp[np.where(img_tmp < Threshold)] = 0; # attribute 0 to pixels with intensity < threshold
    img_tmp[np.where(img_tmp > Threshold)] = 1; # attribute 1 to pixels with intensity > threshold --> return binary image
    center = ndimage.measurements.center_of_mass(img_tmp)
    centX = center[1]
    centY = center[0]
#    print "Center: (", centX, ", ", centY, ")"

    # Calculate the distance in pixel between the CCD center and the Intenisty gravity center
    Diff_X = CCD_center_X - np.round(centX)
    Diff_Y = CCD_center_Y - np.round(centY)
#    print "Pix diff: (", Diff_X, ", ", Diff_Y, ")"

    # Calculate the distance in mm between the CCD center and the Intensity gravity center
    phl_Xpos = curr_phlX_pos + Diff_X * Pix_size_H
    phl_Ypos = curr_phlY_pos - Diff_Y * Pix_size_V
#    print "New pos: (", phl_Xpos, ", ", phl_Ypos, ")"

    # Center the pinhole in X & Y on the intensity gravity center
    pv.pin_hole_x.put(phl_Xpos, wait=True, timeout=500)
    pv.pin_hole_x_set.put(1) # switch to set mode
    pv.pin_hole_x.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.pin_hole_x_set.put(0) # switch to use mode
    
    pv.pin_hole_y.put(phl_Ypos, wait=True, timeout=500)
    pv.pin_hole_y_set.put(1) # switch to set mode
    pv.pin_hole_y.put(0, wait=True, timeout=500) # reinitialize position to 0
    pv.pin_hole_y_set.put(0) # switch to use mode
    
    pv.ccd_acquire_mode.put(1, wait=True, timeout=500) # CCD mode switched to continuous
    pv.ccd_trigger.put(1) # Trigger the CCD

    return

