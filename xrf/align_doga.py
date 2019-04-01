
import numpy as np 
import dxchange as dx 
import tomopy
import shutil
import os


mydir = '/Users/decarlo/conda/mic_tools/data'

fname = []

fname = list(filter(lambda x: x.endswith(('.h5', '.hdf')), os.listdir(mydir)))

print(fname)
f = fname[4]

print("FFFFF: ", f)
prj = np.zeros((61, 101, 151), dtype='float32')

for m in range(len(fname)):
    print(fname[m])
    prj += dx.read_hdf5(os.path.join(mydir, fname[m]), dataset='/exchange/data').astype('float32').copy()
    ang = dx.read_hdf5(os.path.join(mydir, f), dataset='/exchange/theta').astype('float32').copy()
    ang *= np.pi / 180.


# Clean folder.
try:
    shutil.rmtree('tmp/iters')
except:
    pass


prj = tomopy.remove_nan(prj, val=0.0)
prj = tomopy.remove_neg(prj, val=0.0)
prj[np.where(prj == np.inf)] = 0.0
# prj = tomopy.median_filter(prj, size=3)

print (prj.min(), prj.max())

prj, sx, sy, conv = tomopy.align_joint(prj, ang, iters=100, pad=(0, 0),
                    blur=True, rin=0.8, rout=0.95, center=None,
                    algorithm='pml_hybrid',
                    upsample_factor=100,
                    save=True, debug=True)
# np.save('tmp/sx.npy', sx)
# np.save('tmp/sy.npy', sy)
