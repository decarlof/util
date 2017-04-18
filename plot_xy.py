#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plot example
"""

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def setplot(fname, nplot, xplot, yplot, label=False):

    data = np.load(fname)
    ax = fig.add_subplot(nplot, xplot, yplot)
    if label:
        ax.set_ylabel(label, rotation=0)
    ax.yaxis.set_label_coords(1.1, 0.4)
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])

    ax.set_xlim(1, 10**3)
    ax.set_ylim(1, 5 * 10**6)
    ax.xaxis.set_major_locator(ticker.AutoLocator())

    # for linear ticks
    ax.yaxis.set_major_locator(ticker.LinearLocator(10))

    # for log ticks
    #ax_n05.set_yscale('log')
    #ax_n05.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=4))
    return data, ax

if __name__ == '__main__':


    fig = plt.figure()
    fig.suptitle('  Noise Level', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.94)

    n05, ax_n05 = setplot('./plots/hist_n05.npy', 6, 2, 1, label='5%')
    ax_n05.set_title('Simulated')
    ax_n05.fill(n05)


    c05, ax_c05 = setplot('./plots/hist_cnn05.npy', 6, 2, 2)
    ax_c05.set_title('CNN enhanced')
    ax_c05.fill(c05)

    n10, ax_n10 = setplot('./plots/hist_n10.npy', 6, 2, 3, label='10%')
    ax_n10.fill(n10)

    c10, ax_c10 = setplot('./plots/hist_cnn10.npy', 6, 2, 4)
    ax_c10.fill(c10)

    n15, ax_n15 = setplot('./plots/hist_n15.npy', 6, 2, 5, label='15%')
    ax_n15.fill(n15)

    c15, ax_c15 = setplot('./plots/hist_cnn15.npy', 6, 2, 6)
    ax_c15.fill(c15)

    n20, ax_n20 = setplot('./plots/hist_n20.npy', 6, 2, 7, label='20%')
    ax_n20.fill(n20)

    c20, ax_c20 = setplot('./plots/hist_cnn20.npy', 6, 2, 8)
    ax_c20.fill(c20)

    n25, ax_n25 = setplot('./plots/hist_n20.npy', 6, 2, 9, label='25%')
    ax_n25.fill(n25)

    c25, ax_c25 = setplot('./plots/hist_cnn25.npy', 6, 2, 10)
    ax_c25.fill(c25)

    n30, ax_n30 = setplot('./plots/hist_n30.npy', 6, 2, 11, label='30%')
    ax_n30.fill(n30)

    c30, ax_c30 = setplot('./plots/hist_cnn30.npy', 6, 2, 12)
    ax_c30.fill(c30)

    plt.show()

