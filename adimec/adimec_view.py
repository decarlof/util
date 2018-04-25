
import os
import sys
import argparse

import struct
import numpy as np

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg

import tomopy
import dxchange 

class slider():
    def __init__(self, data):
        self.data = data

        ax = pl.subplot(111)
        pl.subplots_adjust(left=0.25, bottom=0.25)

        self.frame = 0
        self.l = pl.imshow(self.data[self.frame,:,:], cmap='gray') 

        axcolor = 'lightgoldenrodyellow'
        axframe = pl.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
        self.sframe = wdg.Slider(axframe, 'Frame', 0, self.data.shape[0]-1, valfmt='%0.0f')
        self.sframe.on_changed(self.update)

        pl.show()

    def update(self, val):
        self.frame = int(np.around(self.sframe.val))
        self.l.set_data(self.data[self.frame,:,:])


def _slice_array(arr, slc):
    """
    Perform slicing on ndarray.

    Parameters
    ----------
    arr : ndarray
        Input array to be sliced.
    slc : sequence of tuples
        Range of values for slicing data in each axis.
        ((start_1, end_1, step_1), ... , (start_N, end_N, step_N))
        defines slicing parameters for each axis of the data matrix.

    Returns
    -------
    ndarray
        Sliced array.
    """
    if slc is None:
        logger.debug('No slicing applied to image')
        return arr[:]
    axis_slice = _make_slice_object_a_tuple(slc)
    logger.debug('Data sliced according to: %s', axis_slice)
    return arr[axis_slice]


def read_adimec_header(filename):
	
	file_size = os.path.getsize(filename)
	with open(filename, 'rb') as bdata:
	    header_size = 96 # in bytes           
	    bheader = bdata.read(header_size)
	    header_data = struct.unpack('iiiiiiiiiiiiiiiiiidiiii', bheader)
	    data_type = header_data[0]
	    ndims = header_data[1]
	    size_x = header_data[2]
	    size_y = header_data[3]
	    offset_x = header_data[4]
	    offset_y = header_data[5]
	    binning_x = header_data[6]
	    binning_y = header_data[7]
	    reverse_x = header_data[8]
	    reverse_y = header_data[9]
	    dummy_0  = header_data[10]
	    dummy_1  = header_data[11]
	    dummy_2  = header_data[12]
	    dummy_3  = header_data[13]
	    dummy_4  = header_data[14]
	    dummy_5  = header_data[15]
	    unique_id  = header_data[16]
	    data_size  = header_data[17]
	    adimec_ts = header_data[18]
	    epics_time_sec = header_data[19]
	    epics_time_ns = header_data[20]
	    nflat = header_data[21]
	    ndark = header_data[22]

	nimg = (file_size - 512) / size_x / size_y

	return nflat, ndark, nimg, size_y, size_x

def read_adimec_stack(filename, img=None, sino=None, dtype=None):

    nflat, ndark, nimg, height, width = read_adimec_header(filename)

    img_to_skip = img[0]*width*height
    img_to_load= (img[1]-img[0])*width*height

    # Select projection range to read.
    with open(filename, 'r') as infile:
        # Skip the header
        infile.seek(512)
        if (img != None): 
            infile.seek(img_to_skip, 1)
        rdata = np.fromfile(infile, dtype=np.uint8, count=img_to_load)
    # Reshape the data into a 3D array. (-1 is a placeholder for however many
    # images are in the file... E.g. 2000)
	data = rdata.reshape((-1, height, width))
    return data


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Full file name: /data/fname.raw")
    parser.add_argument("--start", nargs='?', type=int, default=0, help="First image to read")
    parser.add_argument("--nimg", nargs='?', type=int, default=1, help="Number of images to read")
    parser.add_argument("--ndark", nargs='?', type=int, default=10, help="Number of dark images")
    parser.add_argument("--nflat", nargs='?', type=int, default=10, help="Number of white images")

    args = parser.parse_args()

    fname = args.fname
    start = args.start
    end = args.start + args.nimg

    nflat, ndark, nimg, height, width = read_adimec_header(fname)
    print("Image Size:", width, height)
    print("Dataset metadata (nflat, ndark, nimg:", nflat, ndark, nimg)

    # override nflat and ndark from header with the passed parameter
    # comment the two lines below if the meta data in the binary 
    # file for nflat and ndark is correct
    nflat = args.nflat
    ndark = args.ndark

    proj = read_adimec_stack(fname, img=(start, end))
    print("Projection:", proj.shape)
    # slider(proj)

    flat = read_adimec_stack(fname, img=(nimg-ndark-nflat, nimg-ndark))
    print("Flat:", flat.shape)
    # slider(flat)

    dark = read_adimec_stack(fname, img=(nimg-ndark, nimg))
    print("Dark:", dark.shape)
    # slider(dark)

    nproj = tomopy.normalize(proj, flat, dark)
    print("Normalized projection:", nproj.shape)
    # slider(proj)

    
    proj = nproj[:,100:110, :]
    print("Sino chunk:", proj.shape)
    slider(proj)
    
    theta = tomopy.angles(proj.shape[0])
    print(theta.shape)

    proj = tomopy.minus_log(proj)

    proj = tomopy.remove_nan(proj, val=0.0)
    proj = tomopy.remove_neg(proj, val=0.00)
    proj[np.where(proj == np.inf)] = 0.00

    rot_center = 1280
    # Reconstruct object using Gridrec algorithm.
    rec = tomopy.recon(proj, theta, center=rot_center, algorithm='gridrec')

    # Mask each reconstructed slice with a circle.
    rec = tomopy.circ_mask(rec, axis=0, ratio=0.95)

    # Write data as stack of TIFs.
    dxchange.write_tiff_stack(rec, fname='recon_dir/recon')


if __name__ == "__main__":
    main(sys.argv[1:])
