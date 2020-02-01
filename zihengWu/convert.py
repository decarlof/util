
import os
import sys
import argparse

import dxfile.dxtomo as dx
from dxchange.reader import read_hdf5


def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="file name of a tomographic dataset: /data/ or /data/sample.hdf")
    args = parser.parse_args()

    projfname = args.fname

    head_tail = os.path.split(projfname)

    darkfname = head_tail[0] + os.sep + "proj_0203.hdf"
    whitefname = head_tail[0] + os.sep + "proj_0202.hdf"
    fixedfmame = head_tail[0] + os.sep + 'proj_201.h5'

    exchange_base = "exchange"

    tomo_grp = '/'.join([exchange_base, 'data'])
    flat_grp = '/'.join([exchange_base, 'data_white'])
    dark_grp = '/'.join([exchange_base, 'data_dark'])
    theta_grp = '/'.join([exchange_base, 'theta'])
    tomo = read_hdf5(projfname, tomo_grp)
    flat = read_hdf5(whitefname, flat_grp)
    dark = read_hdf5(darkfname, dark_grp)
    theta = read_hdf5(projfname, theta_grp)

    # Open DataExchange file
    f = dx.File(fixedfmame, mode='w') 

    f.add_entry(dx.Entry.data(data={'value': data, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_white={'value': data_white, 'units':'counts'}))
    f.add_entry(dx.Entry.data(data_dark={'value': data_dark, 'units':'counts'}))
    f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

    f.close()


if __name__ == "__main__":
    main(sys.argv[1:])