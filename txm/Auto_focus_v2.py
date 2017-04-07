#!/usr/bin/env python


import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def auto_focus(focus_range, steps, dwell_time):
    """
    auto_focus : is based on the contrast of images.
    
    Parameters
    ----------
    focus_range : range for the scanning of the motor repsonsible for the fine focus
    steps: number of steps inside the scanned range
    dwell_time: dwell time for the CCD acquisition

    """

    # Work on a ROI
    ROI=1

    # Variables creation:
    ROI_pixH = [400, 2300]
    ROI_pixV = [620, 1900]
    ROI_pixH = [1300, 1500]
    ROI_pixV = [800, 1000]

    nVPix = pv.ccd_image_rows.get()
    nHPix = pv.ccd_image_columns.get()
    print nVPix, nHPix

    image_size = nVPix * nHPix
#   if ROI:
#       mat_3d = np.zeros((steps, (ROI_pixV[1]-ROI_pixV[0]), (ROI_pixH[1]-ROI_pixH[0])), np.int16)
#   else:

    # initialize the 3D matrix
    mat_3d = np.zeros((steps, nVPix, nHPix), np.int16)				
    current_focus_position = pv.ccd_focus.get()									# get the current focus position
    vect_pos = np.linspace(current_focus_position - focus_range/2, current_focus_position + focus_range/2, steps)	# define the vector containing angles
    delta_step = abs(vect_pos[1] - vect_pos[0])							# get the delta angle
    std_im = np.arange(0,np.size(vect_pos),1)

    pv.ccd_dwell_time.put(dwell_time)  

    # move the focus before the scan starting point to annihilate the backlash
    pv.ccd_focus.put(vect_pos[0]-8000, wait=True, timeout=500)
    print '*** Starting position: ',(vect_pos[0]-8000)
 
    # start the focus scan
    for iLoop in range(0, steps):
        print '*** Step #%i / %i' % (iLoop, np.size(vect_pos))
        print '    Motor pos: ',vect_pos[iLoop]
        pv.ccd_focus.put(vect_pos[iLoop], wait=True, timeout=500)			#

        # Trigger the CCD
        pv.ccd_trigger.put(1, wait=True, timeout=500)

        # Get the image still in memory
        img_vect = pv.ccd_image.get()
        img_vect = img_vect[0:image_size]
        img_tmp = np.reshape(img_vect,[nVPix, nHPix])

        # Store the image in Mat3D
        mat_3d[iLoop,:,:] = img_tmp            

        if ROI:
#           im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            im = mat_3d[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            im = mat_3d[iLoop,:,:]
                
        std_tmp = im.std(axis=0)

        # store the std devation in std_im
        std_im[iLoop] = std_tmp.std(axis=0)	
        #plt.imshow(img_tmp), plt.set_cmap('gray'), plt.colorbar()
        #plt.set_title('image #%i, focus:%f' % (iLoop, vect_pos(iLoop)))
            
    # Interpolate the minimum value
    #std_int = interp(linspace(vect_pos[0], vect_pos[-1], 10), vect_pos, std_im)
    f = interpolate.interp1d(vect_pos, std_im, kind='cubic')	
    vect_pos_int = np.linspace(vect_pos[0], vect_pos[-1], 50)
    std_int = f(vect_pos_int)
    
    # get the highest sdt:
    index_max_std = np.where(std_int==max(std_int))

    print '*** Best focus at ', vect_pos_int[index_max_std]
    

    plt.plot(vect_pos, std_im, 'go', vect_pos_int, std_int, 'r-'), plt.grid()
    plt.plot(vect_pos_int[index_max_std], max(std_int), 'b*')
    plt.title('Standard deviation for different focus values')
    plt.show()
    
    return mat_3d, std_int
	
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
    auto_focus(3, 5, 1)
