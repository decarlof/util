from __future__ import print_function
import dxchange
import numpy as np
import tomopy
import os, glob


#fn = sys.argv[1]
#sinoused = (sys.argv[2],sys.argv[3])

fn = 'blakelyALS'
sinoused = (750,752,1)
cor = 1683

gdata = {}
with open(fn+'.sct') as sct:
	for line in sct:
		(key, val) = line.split(' ',1)
		gdata[key[1:]] = val[:-1]
		
		
i0cycle = int(gdata['i0cycle'])
numangles = int(gdata['nangles'])
numslices = int(gdata['nslices'])
numrays = int(gdata['nrays'])
raysused = (0,numrays,1)

pxsize = float(gdata['pxsize'])/10 # /10 to convert unites from mm to cm
angularrange = float(gdata['arange'])
npad = int(np.ceil(numrays * np.sqrt(2)) - numrays)//2

angle_offset = 270 #this matches convention of other 8.3.2 software

floc = range(0,numangles,i0cycle) #flat_locations

numdrk = len(glob.glob('*'+fn+'drk_'+'*')) #number of dark fields based on how many files have 'drk_' in them in the directory

flatextension = 'bak'
darkextension = 'drk'
fileextension = '.tif'

nslicesused = sinoused[1] - sinoused[0]

tomo = np.empty(shape=(numangles,nslicesused,numrays),dtype=np.uint16)
flat = np.empty(shape=(len(floc),nslicesused,numrays),dtype=np.uint16)
dark = np.empty(shape=(numdrk,nslicesused,numrays),dtype=np.uint16)



for y in range(0,numangles,1):
	if y%25==0:
		print('loading tomo image {:d} of {:d}'.format(y,numangles))
	inputPath = '{}_{:d}{}'.format(fn,y,fileextension)
	tomo[y] = dxchange.reader.read_tiff(inputPath,slc = (sinoused, raysused))

print('loading flat images')
for y in range(0,len(floc)):
	inputPath = '{}{}_{:d}{}'.format(fn,flatextension,floc[y],fileextension)
	flat[y] = dxchange.reader.read_tiff(inputPath,slc = (sinoused, raysused))

print('loading dark images')
for y in range(0,numdrk):
	inputPath = '{}{}_{:d}{}'.format(fn,darkextension,y,fileextension)
	dark[y] = dxchange.reader.read_tiff(inputPath,slc = (sinoused, raysused))	
	
print('normalizing')
tomo = tomo.astype(np.float32)
tomopy.normalize_nf(tomo, flat, dark, floc, out=tomo)

tomopy.minus_log(tomo, out=tomo)

tomo = tomopy.pad(tomo, 2, npad=npad, mode='edge')
rec = tomopy.recon(tomo, tomopy.angles(numangles, angle_offset, angle_offset-angularrange), center=cor+npad, algorithm='gridrec', filter_name='butterworth', filter_par=[.25, 2])
rec = rec[:, npad:-npad, npad:-npad]
rec /= pxsize  # convert reconstructed voxel values from 1/pixel to 1/cm
rec = tomopy.circ_mask(rec, 0)



print('writing recon')
dxchange.write_tiff_stack(rec, fname='rec/'+fn, start=sinoused[0])

