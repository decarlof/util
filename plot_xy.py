#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example to plot the HZG nano tomography projections shifts.
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    n05 = np.load('./plots/hist_n05.npy')
    c05 = np.load('./plots/hist_cnn05.npy')

    n10 = np.load('./plots/hist_n10.npy')
    c10 = np.load('./plots/hist_cnn10.npy')

    n15 = np.load('./plots/hist_n15.npy')
    c15 = np.load('./plots/hist_cnn15.npy')

    n20 = np.load('./plots/hist_n20.npy')
    c20 = np.load('./plots/hist_cnn20.npy')

    n25 = np.load('./plots/hist_n25.npy')
    c25 = np.load('./plots/hist_cnn25.npy')

    n30 = np.load('./plots/hist_n30.npy')
    c30 = np.load('./plots/hist_cnn30.npy')

    print (n05.shape, c05.shape)

    x = np.arange(n05.shape[0])
    
    fig = plt.figure()
    fig.suptitle('  Noise Level', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.94)

    ax_n05 = fig.add_subplot(6, 2, 1)
    ax_n05.set_title('title')
    ax_n05.set_ylabel('5%', rotation=0)
    ax_n05.yaxis.set_label_coords(1.1, 0.4)
    ax_n05.xaxis.set_ticklabels([])
    ax_n05.yaxis.set_ticklabels([])
    ax_n05.fill(x, n05)

    ax_c05 = fig.add_subplot(6, 2, 2)
    ax_c05.set_title('CNN')
    ax_c05.xaxis.set_ticklabels([])
    ax_c05.yaxis.set_ticklabels([])
    ax_c05.fill(x, c05)

    ax_n10 = fig.add_subplot(6, 2, 3)
    ax_n10.set_ylabel('10%', rotation=0)
    ax_n10.yaxis.set_label_coords(1.1, 0.4)
    ax_n10.xaxis.set_ticklabels([])
    ax_n10.yaxis.set_ticklabels([])
    ax_n10.fill(x, n10)

    ax_c10 = fig.add_subplot(6, 2, 4)
    ax_c10.xaxis.set_ticklabels([])
    ax_c10.yaxis.set_ticklabels([])
    ax_c10.fill(x, c10)

    ax_n15 = fig.add_subplot(6, 2, 5)
    ax_n15.set_ylabel('15%', rotation=0)
    ax_n15.yaxis.set_label_coords(1.1, 0.4)
    ax_n15.xaxis.set_ticklabels([])
    ax_n15.yaxis.set_ticklabels([])
    ax_n15.fill(x, n15)

    ax_c15 = fig.add_subplot(6, 2, 6)
    ax_c15.xaxis.set_ticklabels([])
    ax_c15.yaxis.set_ticklabels([])
    ax_c15.fill(x, c15)

    ax_n20 = fig.add_subplot(6, 2, 7)
    ax_n20.set_ylabel('20%', rotation=0)
    ax_n20.yaxis.set_label_coords(1.1, 0.4)
    ax_n20.xaxis.set_ticklabels([])
    ax_n20.yaxis.set_ticklabels([])
    ax_n20.fill(x, n20)

    ax_c20 = fig.add_subplot(6, 2, 8)
    ax_c20.xaxis.set_ticklabels([])
    ax_c20.yaxis.set_ticklabels([])
    ax_c20.fill(x, c20)

    ax_n25 = fig.add_subplot(6, 2, 9)
    ax_n25.set_ylabel('25%', rotation=0)
    ax_n25.yaxis.set_label_coords(1.1, 0.4)
    ax_n25.xaxis.set_ticklabels([])
    ax_n25.yaxis.set_ticklabels([])
    ax_n25.fill(x, n25)

    ax_c25 = fig.add_subplot(6, 2, 10)
    ax_c25.xaxis.set_ticklabels([])
    ax_c25.yaxis.set_ticklabels([])
    ax_c25.fill(x, c25)

    ax_n30 = fig.add_subplot(6, 2, 11)
    ax_n30.set_ylabel('30%', rotation=0)
    ax_n30.yaxis.set_label_coords(1.1, 0.4)
    ax_n30.xaxis.set_ticklabels([])
    ax_n30.yaxis.set_ticklabels([])
    ax_n30.fill(x, n30)

    ax_c30 = fig.add_subplot(6, 2, 12)
    ax_c30.xaxis.set_ticklabels([])
    ax_c30.yaxis.set_ticklabels([])
    ax_c30.fill(x, c30)

    plt.show()

