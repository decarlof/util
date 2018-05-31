#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example script 
"""

from __future__ import print_function
from xlearn.transform import train
import dxchange


batch_size = 800
nb_epoch = 10
dim_img = 20
nb_filters = 32
nb_conv = 3
patch_step = 4

patch_size = (dim_img, dim_img)

# read the training data

train_folder ='/local/dataraid/cnn/Al-10Sn-4Si-1Cu-Er-Zr/train/'

img_x = dxchange.read_tiff(train_folder + 'Slice_0563-segmentation.tiff')
img_y = dxchange.read_tiff(train_folder + 'Slice_0563.tiff')

# train and save the model
model = train(img_x, img_y, patch_size, patch_step, dim_img, nb_filters, nb_conv, batch_size, nb_epoch)
model.save_weights('transform_training_weights_al10.h5')

