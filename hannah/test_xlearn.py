# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 15:08:35 2018

@author: Hannah
"""


import dxchange
import matplotlib.pyplot as plt

from xlearn.transform import train
from xlearn.transform import model

batch_size=800
nb_epoch=10
dim_img=20
nb_filters=32
nb_conv=3
patch_step=4
patch_size=(dim_img, dim_img)

img_x=dxchange.read_tiff('C:/Users/Hannah/Downloads/python programs/original_input/image235/235_normal.tif')
img_y=dxchange.read_tiff('C:/Users/Hannah/Downloads/python programs/original_input/image235/235_label.tif')

plt.imshow(img_x, cmap='Greys_r')
plt.show()

plt.imshow(img_y, cmap='Greys_r')
plt.show()

mdl=train(img_x, img_y, patch_size, patch_step, dim_img, nb_filters, nb_conv, batch_size, nb_epoch)
mdl.save_weights('training_weights.h5')
