#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example to plot the HZG nano tomography projections shifts.
"""

from __future__ import print_function
import numpy as np
import uuid
import matplotlib.pyplot as plt

if __name__ == '__main__':

    #folder = '/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections_crop_aligned/align_iter_40/'
    folder = '/local/decarlo/data/hzg/nanotomography/scan_renamed_450projections_crop_rotate_aligned/align_iter_39/'
    unique_filename = uuid.uuid4()
    print(unique_filename)
    sx = np.load(folder + 'shift_x.npy')
    sy = np.load(folder + 'shift_y.npy')
    print (sx.shape, sy.shape)
    err = np.zeros([sx.shape[0], sy.shape[0]])
    err[:,0] = sx
    err[:,1] = sy
    print(sx)
    print('#####################################')
    print(sy)
    x = np.arange(sx.shape[0])
    
    fig = plt.figure()
    fig.suptitle('Projection Shift', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.85)

    ax = fig.add_subplot(211)
    #ax.set_xlabel('number of projections')
    ax.set_ylabel('x', color='red')
    ax.plot(x, sx, 'o', color='red')
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.legend()

    ax1 = fig.add_subplot(212, sharex=ax, frameon=False)
    ax1.yaxis.tick_left()
    ax1.set_xlabel('number of projections')
    ax1.yaxis.set_label_position("left")
    ax1.set_ylabel('y', color='green')

    ax1.plot(x, sy, 'o', color='green')

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

