
import os
import sys
import argparse

import dxfile.dxtomo as dx
from dxchange.reader import read_hdf5


def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="file name of a tomographic dataset: /data/ or /data/sample.hdf")
    args = parser.parse_args()

    proj_fname = args.fname

    head_tail = os.path.split(proj_fname)

    dark_fname = head_tail[0] + os.sep + "proj_0203.hdf"
    white_fname = head_tail[0] + os.sep + "proj_0202.hdf"
    converted_fmame = head_tail[0] + os.sep + os.path.splitext(head_tail[1])[1] + '.h5'

    print(proj_fname)
    print(dark_fname)
    print(white_fname)
    print(converted_fmame)

    return
    exchange_base = "exchange"

    tomo_grp = '/'.join([exchange_base, 'data'])
    flat_grp = '/'.join([exchange_base, 'data_white'])
    dark_grp = '/'.join([exchange_base, 'data_dark'])
    theta_grp = '/'.join([exchange_base, 'theta'])
    tomo = read_hdf5(proj_fname, tomo_grp)
    flat = read_hdf5(white_fname, flat_grp)
    dark = read_hdf5(dark_fname, dark_grp)
    theta = read_hdf5(proj_fname, theta_grp)

    # Open DataExchange file
    f = dx.File(converted_fmame, mode='w') 

    f.add_entry(dx.Entry.data(data={'value': tomo, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_white={'value': flat, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_dark={'value': dark, 'units':'counts'}))
    f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])