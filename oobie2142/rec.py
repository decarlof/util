#!/usr/bin/env python
# coding: utf-8

import dxchange
import matplotlib.pyplot as plt
import tomopy
import numpy as np

proj = dxchange.read_tiff_stack('/Users/decarlo/Downloads/Converted_To_Tiff/Scan-8_9_2019 10_45_13 AM000000.tif', range(0, 900))
proj.shape, proj.min(), proj.max()


# Adjusted pixel sizes to match flat and dark panel size
hshift = 30
vshift = 150

flat = dxchange.read_tiff('/Users/decarlo/Downloads/Converted_To_Tiff/lite_1024avg.tif', slc=((vshift, vshift+422, 1),(hshift,hshift+876,1)),)
dark = dxchange.read_tiff('/Users/decarlo/Downloads/Converted_To_Tiff/dark_1024avg.tif', slc=((vshift, vshift+422, 1),(hshift,hshift+876,1)),)

# force dark to same value
dark = np.zeros(dark.shape) + 100

data = tomopy.normalize(proj, flat, dark)
print(hshift, vshift, data.min(), data.max())

data = tomopy.minus_log(data)

data = tomopy.remove_nan(data, val=0.0)
data = tomopy.remove_neg(data, val=0.00)
data[np.where(data == np.inf)] = 0.00


plt.imshow(data[:, 200, :])
plt.colorbar()
plt.show()

theta = tomopy.angles(data.shape[0], 0, 360)

rot_center = 424.5

# padding 
N = data.shape[2]
data_pad = np.zeros([data.shape[0],data.shape[1],3*N//2],dtype = "float32")
data_pad[:,:,N//4:5*N//4] = data
data_pad[:,:,0:N//4] = np.reshape(data[:,:,0],[data.shape[0],data.shape[1],1])
data_pad[:,:,5*N//4:] = np.reshape(data[:,:,-1],[data.shape[0],data.shape[1],1])
data = data_pad
rot_center = rot_center + N//4

recon = tomopy.recon(data, theta, center=rot_center, algorithm='gridrec')

# padding 
recon = recon[:,N//4:5*N//4,N//4:5*N//4]

# Mask each reconstructed slice with a circle.
recon = tomopy.circ_mask(recon, axis=0, ratio=0.80)

plt.figure(dpi=150)
plt.imshow(recon[200, :,:])
plt.colorbar()
plt.show()