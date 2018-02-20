
import os
import sys
import argparse

import struct
import numpy as np

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg

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


def read_data(filename, width, height):
    with open(filename, 'r') as infile:
        # Skip the header
        infile.seek(512)
        data = np.fromfile(infile, dtype=np.uint8)
    # Reshape the data into a 3D array. (-1 is a placeholder for however many
    # images are in the file... E.g. 2000)
    return data.reshape((-1, height, width))


def read_header(filename):
	
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


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Full file name: /data/fname.raw")

    args = parser.parse_args()

    fname = args.fname
    nflat, ndark, nimg, height, width = read_header(fname)
    print("Image Size:", width, height)
    print("Number of images:", nimg)
    print("Number of flat, dark images:", nimg, nflat, ndark)
    data = read_data(fname, width, height)

    slider(data)

if __name__ == "__main__":
    main(sys.argv[1:])
