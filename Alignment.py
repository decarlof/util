# Alignment.py

# library importation:
import matplotlib.pyplot as plt
import Image
import numpy as np
from epics import caget, caput


# Alignement of the BPM:
def Align_BPM(camera = None, X_Range, Y_Range, steps, dwell_time):
    from scipy import interpolate

    # PV declaration:
    if camera == None:
        PV_Prefix = 'TXMNeo1:'
    beam_monitor_X = '32idcTXM:nf:c0:m1.VAL'
    PV_beam_monitor_Y = '32idcTXM:nf:c0:m2.VAL'
    PV_dwelltime = PV_Prefix + 'cam1:AcquireTime'
    PV_trigger = PV_Prefix + 'cam1:Acquire'
    PV_nRow_CCD = PV_Prefix + 'cam1:SizeY'
    PV_nCol_CCD = PV_Prefix + 'cam1:SizeX'
    PV_image = PV_Prefix + 'image1:ArrayData'
    

    # Work on a ROI
    ROI=0

    # Variables creation:
    ROI_pixH = [400, 2300]
    ROI_pixV = [620, 1900]
    ROI_pixH = [1300, 1500]
    ROI_pixV = [800, 1000]   
    nVPix = caget(PV_nRow_CCD)
    nHPix = caget(PV_nCol_CCD)
#   nHPix = 2560    # CCD parameter
#   nVPix = 2160    # CCD parameter

#   if ROI:
#   Mat3D = np.zeros((steps, (ROI_pixV[1]-ROI_pixV[0]), (ROI_pixH[1]-ROI_pixH[0])), np.int16)
#   else:
    Mat3D_X = np.zeros((steps, nVPix, nHPix), np.int16) # initialize the 3D matrix
    Mat3D_Y = Mat3D_X

    curr_BPMY_pos = caget(PV_beam_monitor_Y)                    # get the current focus position
    vect_pos_Y = np.linspace(curr_BPMY_pos - Y_Range/2, curr_BPMY_pos + Y_Range/2, steps)   # define the vector containing angles
    delta_step_Y = abs(vect_pos_Y[1] - vect_pos_Y[0])                       # get the delta angle
    Std_Im_Y = np.arange(0,np.size(vect_pos_Y),1)

    curr_BPMX_pos = caget(PV_beam_monitor_X)                    # get the current focus position
    vect_pos_X = np.linspace(curr_BPMX_pos - X_Range/2, curr_BPMX_pos + X_Range/2, steps)   # define the vector containing angles
    delta_step_X = abs(vect_pos_X[1] - vect_pos_X[0])                       # get the delta angle
    Std_Im_X = np.arange(0,np.size(vect_pos_X),1)

    caput(PV_dwelltime, dwell_time)


    ######################################
    # start the Y BPM scan
    caput(PV_beam_monitor_Y, vect_pos_Y[0] # move the BPM to the Y starting point
#    print '*** Y BPM scan tarting position: ',(vect_pos_Y[0])
    
    for iLoop in range(0, steps)
#        print '*** Step #%i / %i' % (iLoop, np.size(vect_pos_Y))
#        print '    Motor pos: ',vect_pos_Y[iLoop]
        caput(PV_beam_monitor_Y, vect_pos_Y[iLoop], wait=True, timeout=500) #
        caput(PV_trigger, 1, wait=True, timeout=500)                # trigger the CCD

        # get the image still in memory
        Img_vect = caget(PV_image)
        Img_tmp = np.reshape(Img_vect,[nVPix, nHPix])
    
        Mat3D_Y[iLoop,:,:] = Img_tmp            # store the image in Mat3D

        if ROI:
#           Im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            Im = Mat3D_Y[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            Im = Mat3D_Y[iLoop,:,:]
      
        Intensity_Y[iLoop] = np.sum(Im) # store the intensity

#       plt.imshow(Img_tmp), plt.set_cmap('gray'), plt.colorbar()
#       plt.set_title('Image #%i, focus:%f' % (iLoop, vect_pos_Y(iLoop)))
        
    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_Y, Intensity_Y, kind='cubic') 
    vect_pos_Y_int = np.linspace(vect_pos_Y[0], vect_pos_Y[-1], 50)
    Intensity_Y_int = f(vect_pos_Y_int)

#    get the motor position with the max intensity:
    Index_max_Intensity = np.where(Intensity_Y==max(Intensity_Y))

    print '*** Best Y position at ', vect_pos_Y_int[Index_max_std]
    
    plt.plot(vect_pos_Y, Intensity_Y, 'go', vect_pos_Y_int, Intensity_Y_int, 'r-'), plt.grid()
    plt.plot(vect_pos_Y_int[Index_max_Intensity], max(Intensity_Y_int), 'b*')
    plt.title('Standard deviation for different Y BPM positions')
    plt.show()

    # Move to the optimum Y position:
    caput(PV_beam_monitor_Y, vect_pos_Y_int[Index_max_Intensity])

    ######################################
    # start the X BPM scan
    caput(PV_beam_monitor_X, vect_pos_X[0] # move the BPM to the X starting point
    print '*** Y BPMN scan tarting position: ',(vect_pos_X[0])
    
    for iLoop in range(0, steps):
        print '*** Step #%i / %i' % (iLoop, np.size(vect_pos_X))
        print '    Motor pos: ',vect_pos_X[iLoop]
        caput(PV_beam_monitor_X, vect_pos_X[iLoop], wait=True, timeout=500) #
        caput(PV_trigger, 1, wait=True, timeout=500)                # trigger the CCD

        # get the image still in memory
        Img_vect = caget(PV_image)
        Img_tmp = np.reshape(Img_vect,[nVPix, nHPix])
        
        Mat3D_X[iLoop,:,:] = Img_tmp            # store the image in Mat3D

        if ROI:
    #       Im = Mat3D[iLoop, ROI_pixV[1]-ROI_pixV[0], ROI_pixH[1]-ROI_pixH[0]]
            Im = Mat3D_X[iLoop, ROI_pixV[0]:ROI_pixV[1], ROI_pixH[0]:ROI_pixH[1]]
        else:
            Im = Mat3D_X[iLoop,:,:]
            Intensity_X[iLoop] = np.sum(Im) # store the intensity

    #       plt.imshow(Img_tmp), plt.set_cmap('gray'), plt.colorbar()
    #       plt.set_title('Image #%i, focus:%f' % (iLoop, vect_pos_Y(iLoop)))
        
    # Interpolate the minimum value
    f = interpolate.interp1d(vect_pos_X, Intensity_X, kind='cubic') 
    vect_pos_X_int = np.linspace(vect_pos_X[0], vect_pos_X[-1], 50)
    Intensity_X_int = f(vect_pos_X_int)

    # Get the motor position with the max intensity:
    Index_max_Intensity = np.where(Intensity_X==max(Intensity_X))

    print '*** Best X position at ', vect_pos_X_int[Index_max_std]

    plt.plot(vect_pos_X, Intensity_X, 'go', vect_pos_X_int, Intensity_X_int, 'r-'), plt.grid()
    plt.plot(vect_pos_X_int[Index_max_Intensity], max(Intensity_X_int), 'b*')
    plt.title('Standard deviation for different X BPM positions')
    plt.show()

    # Move to the optimum X position:
    caput(PV_beam_monitor_X, vect_pos_X_int[Index_max_Intensity])

    return [Mat3D_Y, Intensity_Y_int, Mat3D_X, Intensity_X_int]

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
                   


