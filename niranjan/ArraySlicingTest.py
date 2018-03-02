import matplotlib as mpl
import matplotlib.pyplot as plt

import os
import sys
import argparse
import fnmatch
from os.path import expanduser
import dxchange
import numpy as np
import scipy.ndimage as ndi

import pandas as pd
from pandas import DataFrame, Series  # for convenience

import trackpy as tp

import ximage

top = '/local/dataraid/ImageProcessingTest/'

# Read the raw data
index_start = 1292
frames = ximage.load_raw(top, index_start)

print(frames.shape)

cropped_frames = frames[1:2, 1:2, 1:2]
print(cropped_frames.shape)
