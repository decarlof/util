
import process_variables as pv
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from scipy import ndimage
from scipy.ndimage import filters
from scipy.optimize import curve_fit
from time import *

def my_func():
    ## Input ----------
    # Param knife edge simu
    nSteps = 30; theRange = 24; std_noise = 0.01; arbitrary_height = 111
    
    nPt_gaus = 100 # gaussian fitting param
    
    filter_struct = 3
    
    #-----------------
    
    vect_pos_x = np.linspace(-theRange/2,theRange/2,nSteps)
    
    # simutlate the sigmoid
    intensity = 1/(1+np.exp(-vect_pos_x)) + np.random.normal(0,std_noise,nSteps) + arbitrary_height
    deriv_int = np.diff(intensity)
    
    vect_pos_x = vect_pos_x + theRange/2+10
    
    # filtering
    intensity_filt = filters.median_filter(intensity, footprint=np.ones(filter_struct))
    deriv_int_filt = filters.median_filter(deriv_int, footprint=np.ones(filter_struct))
    
    # Gaussian function:
    def gaus(x, a, x0, sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))
    
    # Gaussian fitting
    x = vect_pos_x[1:]
    x_HR = np.linspace(x[0], x[-1], nPt_gaus)
    mean_x = np.mean(x)
    sigma = np.std(x)
    
    y = deriv_int
    amp = np.max(y)
    popt = curve_fit(gaus,x,y,p0=[amp,mean_x,sigma])
    param = popt[0]
    sigma1 = param[2]
    deriv_int_fit = gaus(x_HR, param[0], param[1], param[2])
    
    y = deriv_int_filt
    amp = np.max(y)
    popt = curve_fit(gaus,x,y,p0=[amp,mean_x,sigma])
    param = popt[0]
    sigma2 = param[2]
    deriv_int_filt_fit = gaus(x_HR, param[0], param[1], param[2])
    
    
    
    ####################################################### Display
    plt.subplot(2,2,1) # knife edge
    plt.plot(vect_pos_x, intensity, 'go-')
    plt.title('Knife edge'), plt.ylabel('Intensity'), plt.grid()
    
    plt.subplot(2,2,3) # knife edge derivative + gaussian fit
    plt.plot(vect_pos_x[1:], deriv_int, 'go--', x_HR, deriv_int_fit, 'r-')
    TheTitle = 'Knife edge derivative; FWHM: %0.2f' % 2.3548*sigma1
    plt.title(TheTitle), plt.xlabel('motor position'), plt.ylabel('Intensity'), plt.grid()
    
    plt.subplot(2,2,2) # filtered knife edge
    plt.plot(vect_pos_x, intensity_filt, 'go-')
    plt.title('Filtered knife edge'), plt.ylabel('Intensity'), plt.grid()
    
    plt.subplot(2,2,4) # filtered knife edge derivative + gaussian fit
    plt.plot(vect_pos_x[1:], deriv_int_filt, 'go--', x_HR, deriv_int_filt_fit, 'r-')
    TheTitle = 'Filtered Knife edge derivative; FWHM: %0.2f' % 2.3548*sigma2
    plt.title(TheTitle), plt.xlabel('motor position'), plt.ylabel('Intensity'), plt.grid()
    
    plt.show()
 

#f = interpolate.interp1d(vect_pos_x, intensity, kind='cubic')
#vect_pos_x_int = np.linspace(vect_pos_x[0], vect_pos_x[-1], 50)
#intensity_int = f(vect_pos_x_int)
