from readMDA import *

import re
import os
import numpy as np
import matplotlib.pyplot as plt


def _get_extension(fname):
    """
    Get file extension.
    """
    return '.' + fname.split(".")[-1]


def _remove_trailing_digits(text):
    digit_string = re.search('\d+$', text)
    if digit_string is not None:
        number_of_digits = len(digit_string.group())
        text = ''.join(text[:-number_of_digits])
        return (text, number_of_digits)
    else:
        return (text, 0)

def _get_body(fname):
    """
    Get file name after extension removed.
    """
    body = os.path.splitext(fname)[0]
    return body

def _remove_ext(fname):
    tail, ext = os.path.splitext(fname)
    return tail

def _list_file_stack(fname, ind):
    """
    Return a stack of file names in a folder as a list.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    ind : list of int
        Indices of the files to read.
    """

    body = _get_body(fname)
    body, digits = _remove_trailing_digits(body)

    ext = _get_extension(fname)
    list_fname = []
    for m in ind:
        counter_string = str(m).zfill(digits)
        list_fname.append(body + counter_string + ext)
    return list_fname

def read_raw(fname):
    d = readMDA(fname, verbose=0)
    x = d[1].p[0].data 
    y = d[2].p[0].data
 
    fluo = np.array(d[2].d[6].data)
    diff = np.array(d[2].d[7].data)
    theta = d[2].d[52].data

    return fluo, diff, x, y, theta


if __name__ == '__main__':
    template = '/Users/decarlo/Desktop/irene_python/Data_sector26/mda/26idbSOFT_0001.mda'
    ind = [75,77,83,85,87,91,93]

    list_fname = _list_file_stack(template, ind)
   
    plot_index = 0
    plt.figure(figsize=(15,25))

    for fname in list_fname:
        print(fname)
        head, tail = os.path.split(fname)
        label =  _remove_ext(tail)

        fluo, diff, x, y, theta = read_raw(fname)

        plot_index += 1
        plt.subplot(len(ind), 2, plot_index)

        plt.imshow(fluo[::-1,:], extent=[min(min(y)),max(max(y)),min(x),max(x)])
        plt.colorbar()
        plt.axis('tight')
        plt.title(label + ": fluo" + "- theta =%02.1f"%theta[0][0])
        
        plot_index += 1
        plt.subplot(len(ind), 2, plot_index)

        plt.imshow(np.log10(diff[::-1,:]), extent=[min(min(y)),max(max(y)),min(x),max(x)])
        plt.colorbar()
        plt.axis('tight')
        plt.title(label + ": diff" + "- theta =%02.1f"%theta[0][0])   


    plt.show()
