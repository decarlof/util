import os
import sys
import argparse
import tomopy
import dxchange
import dxchange.reader as dxreader

fname = '/Downloads/161006_TLS629_Curvothynnus_female_2.94um_head.txm'

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="file name of a single dataset to normalize: /data/sample.h5")

    args = parser.parse_args()

    fname = args.fname

    if os.path.isfile(fname):
        # Read the txrm raw data.
        proj, flat, dark, dummy = dxchange.read_aps_32id(h5fname)

        # zinger_removal
        proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
        flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)

        # Flat-field correction of raw data.
        ##data = tomopy.normalize(proj, flat, dark, cutoff=0.8)
        data = tomopy.normalize(proj, flat, dark)

    else:
        print("File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])
