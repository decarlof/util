#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python example of how to read am images.
"""

from __future__ import print_function
import tomopy
import dxchange
import numpy as np
import numpy as np
import matplotlib as mpl
import matplotlib.pylab as pl
from matplotlib.widgets import Slider

def update(val):
    frame = int(np.around(sframe.val))
    l.set_data(data[frame,:,:])

if __name__ == '__main__':
    # Set path to the micro-CT data to reconstruct.
    top = '/Users/decarlo/Desktop/data/am/'
    template = '102_Ti_T046mm_U18G13_04mps_p70_D100um_100ps_longpath_S10156.tif'

    index_start = 10156
    index_end = 10162

    ind_tomo = range(index_start, index_end)

    fname = top + template
    # Read the tiff raw data.
    data = dxchange.read_tiff_stack(fname, ind=ind_tomo)

    ax = pl.subplot(111)
    pl.subplots_adjust(left=0.25, bottom=0.25)


    frame = 0
    l = pl.imshow(data[frame,:,:], cmap='gray') #shows 256x256 image, i.e. 0th frame

    axcolor = 'lightgoldenrodyellow'
    axframe = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    sframe = Slider(axframe, 'Frame', 0, data.shape[0]-1, valfmt='%0.0f')

    sframe.on_changed(update)

    pl.show()

