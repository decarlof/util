# -*- coding: utf-8 -*-
import numpy as np
#import tomopy.tools.multiprocess_shared as mp

# --------------------------------------------------------------------

def rotate(args):
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
        
    Examples
    --------
    - Rotate by 0.5 deg:
        
        >>> import tomopy
        >>> 
        >>> # Load sinogram
        >>> myfile = 'demo/data.h5'
        >>> data, white, dark, theta = tomopy.xtomo_reader(myfile)
        >>> 
        >>> # Construct tomo object
        >>> d = tomopy.xtomo_dataset(log='error')
        >>> d.dataset(data, white, dark, theta)
        >>> 
        >>> # Perform normalization
        >>> d.rotate(0.5)
        >>> 
        >>> # Save sinogram after normalization
        >>> output_file='tmp/after_rotation_'
        >>> tomopy.xtomo_writer(d.data, output_file)
        >>> print "Images are succesfully saved at " + output_file + '...'
    """
    # Arguments passed by multi-processing wrapper
    ind, dshape, inputs = args
    
    # Function inputs
    data = mp.tonumpyarray(mp.shared_arr, dshape) # shared-array
    data_dark = mp.tonumpyarray(mp.shared_arr, dshape) # shared-array
    data_white = mp.tonumpyarray(mp.shared_arr, dshape) # shared-array
    angle = inputs
    
    for m in range(self.data.shape[0]):
        self.data[m, :, :] = ndimage.rotate(self.data[m, :, :], angle, reshape=False)
    for m in range(self.data_dark.shape[0]):
        self.data_dark[m, :, :] = ndimage.rotate(self.data_dark[m, :, :], angle, reshape=False)
    for m in range(self.data_white.shape[0]):
        self.data_white[m, :, :] = ndimage.rotate(self.data_white[m, :, :], angle, reshape=False)
