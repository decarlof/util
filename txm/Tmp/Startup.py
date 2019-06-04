#!/usr/bin/env python

# %s%s_%d.tiff

#import Tomo_script_simplified as tss
#from pkg_resources import require; require('cothread'); from numpy import *; import cothread; from cothread.catools import *

import os
if 1:
	os.environ['EPICS_CA_MAX_ARRAY_BYTES'] = '25000000'
	from pkg_resources import require
	require('cothread')
	import cothread
	from cothread.catools import *

#Before launching the function:
import numpy as np
import scipy as sp
from PyQt4 import *
from time import *
import matplotlib.pylab as plt
import Image
#import cv2
#plt.ion()



# COMMAND LINE EXAMPLES:
# os.getcwd()
# os.listdir('.') 
# os.chdir("dir path or name")
# os.makedirs('dir name')
# os.removedirs(path)
# execfile("Startup.py")
# execfile("file name",global_vars,local_vars)
# print Img.dtype

# %s%s_%4.4d.tiff