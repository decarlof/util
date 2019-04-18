import numpy as np
import h5py as h5

import os, glob, fnmatch

path = '/local/data/2019-04/Toney/'

h5files = fnmatch.filter(os.listdir(path), '*.h5')
h5files.sort()

for file in h5files:
	with h5.File(os.path.join(path, file)) as ff:
		count_time = ff['measurement']['instrument']['detector']['exposure_time'].value
		#if (ff['exchange']['data_dark'].shape[0] != 20) or (np.round(count_time[0], 1) == 0.5):
		if (np.round(count_time[0], 1) == 0.5):
			print(f"{file}, Dark Frames: {ff['exchange']['data_dark'].shape[0]}, White Frames: {ff['exchange']['data_white'].shape[0]}, Count Time: {count_time}")
			#print(f"{file}, {ff['exchange']['data_dark'].shape[0]}")