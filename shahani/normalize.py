import os
import sys
import h5py
import argparse
import tomopy
import dxchange
import dxchange.reader as dxreader
import numpy as np

def get_dx_dims(fname, dataset):
    """
    Read array size of a specific group of Data Exchange file.

    Parameters
    ----------
    fname : str
        String defining the path of file or file name.
    dataset : str
        Path to the dataset inside hdf5 file where data is located.

    Returns
    -------
    ndarray
        Data set size.
    """

    grp = '/'.join(['exchange', dataset])

    with h5py.File(fname, "r") as f:
        try:
            data = f[grp]
        except KeyError:
            return None

        shape = data.shape

    return shape


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="file name of a single dataset to normalize: /data/sample.h5")

    args = parser.parse_args()

    fname = args.fname

    if os.path.isfile(fname):
        data_shape = get_dx_dims(fname, 'data')

        # Select projgram range to reconstruct.
        proj_start = 0
        proj_end = data_shape[0]

        chunks = 6          # number of projgram chunks to reconstruct
                            # only one chunk at the time is converted
                            # allowing for limited RAM machines to complete a full reconstruction

        nProj_per_chunk = (proj_end - proj_start)/chunks
        print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((proj_end - proj_start), proj_start, proj_end, chunks, nProj_per_chunk))            

        strt = 0
        for iChunk in range(0,chunks):
            print('\n  -- chunk # %i' % (iChunk+1))
            proj_chunk_start = np.int(proj_start + nProj_per_chunk*iChunk)
            proj_chunk_end = np.int(proj_start + nProj_per_chunk*(iChunk+1))
            print('\n  --------> [%i, %i]' % (proj_chunk_start, proj_chunk_end))
                    
            if proj_chunk_end > proj_end: 
                break

            nproj = (int(proj_chunk_start), int(proj_chunk_end))
            # Reconstruct.
            proj, flat, dark, dummy = dxchange.read_aps_32id(fname, proj=nproj)

            # Flat-field correction of raw data.
            data = tomopy.normalize(proj, flat, dark, cutoff=0.9)                    

            # Write data as stack of TIFs.
            tifffname = os.path.dirname(fname) + os.sep + os.path.splitext(os.path.basename(fname))[0]+ '_tiff/' + os.path.splitext(os.path.basename(fname))[0]
            print("Converted files: ", tifffname)
            dxchange.write_tiff_stack(data, fname=tifffname, start=strt)
            strt += nproj[1] - nproj[0]
    else:
        print("File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])
