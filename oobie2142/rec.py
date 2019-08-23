#!/usr/bin/env python
# coding: utf-8

import dxchange
import matplotlib.pyplot as plt
import tomopy

proj = dxchange.read_tiff_stack('/Users/decarlo/Downloads/Converted_To_Tiff/Scan-8_9_2019 10_45_13 AM000000.tif', range(0, 900))
proj.shape, proj.min(), proj.max()

# Adjusted pixel sizes to match flat and dark panel size
flat = dxchange.read_tiff('/Users/decarlo/Downloads/Converted_To_Tiff/lite_1024avg.tif', slc=((150, 150+422, 1),(30,30+876,1)),)
dark = dxchange.read_tiff('/Users/decarlo/Downloads/Converted_To_Tiff/dark_1024avg.tif', slc=((150, 150+422, 1),(30,30+876,1)),)
flat.shape, dark.shape

proj = tomopy.normalize(proj, flat, dark)
proj.min(), proj.max()

plt.imshow(proj[:, 200, :])
plt.colorbar()
plt.show()

theta = tomopy.angles(proj.shape[0], 0, 360)
recon = tomopy.recon(proj, theta, center=430, algorithm='gridrec')

# Mask each reconstructed slice with a circle.
recon = tomopy.circ_mask(recon, axis=0, ratio=0.80)

plt.figure(dpi=150)
plt.imshow(recon[400, :,:])
plt.colorbar()
plt.show()