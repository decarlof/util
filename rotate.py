# -*- coding: utf-8 -*-
import numpy as np
from scipy.ndimage.interpolation import rotate

# --------------------------------------------------------------------

def rotate(data, data_white, data_dark, angle):
    """
    rotate raw projection data 

    Parameters
    ----------
    data : ndarray
        3-D tomographic data with dimensions:
        [projections, slices, pixels]

    data_white : ndarray
        3-D white field projection data.
        
    data_dark : ndarray
        3-D dark field projection data.

    angle : scalar
        angle of rotation applied to data, data_white and data_dark data. 

    Returns
    -------
    data : ndarray
        rotated data.

    data_white : ndarray
        rotated data_white.

    data_dark : ndarray
        rotated data_dark.
    """
    
    for m in range(self.data.shape[0]):
        data[m, :, :] = ndimage.rotate(data[m, :, :], angle, reshape=False)
    for m in range(self.data_dark.shape[0]):
        data_dark[m, :, :] = ndimage.rotate(data_dark[m, :, :], angle, reshape=False)
    for m in range(self.data_white.shape[0]):
        data_white[m, :, :] = ndimage.rotate(data_white[m, :, :], angle, reshape=False)
        
    return data, data_white, data_dark
