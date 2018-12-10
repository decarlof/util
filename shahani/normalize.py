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
        data_shape = get_dx_dims(fname, 'data')

        # Select sinogram range to reconstruct.
        sino_start = 0
        sino_end = data_shape[1]

        chunks = 6          # number of sinogram chunks to reconstruct
                            # only one chunk at the time is converted
                            # allowing for limited RAM machines to complete a full reconstruction

        nSino_per_chunk = (sino_end - sino_start)/chunks
        print("Reconstructing [%d] slices from slice [%d] to [%d] in [%d] chunks of [%d] slices each" % ((sino_end - sino_start), sino_start, sino_end, chunks, nSino_per_chunk))            

        strt = 0
        for iChunk in range(0,chunks):
            print('\n  -- chunk # %i' % (iChunk+1))
            sino_chunk_start = np.int(sino_start + nSino_per_chunk*iChunk)
            sino_chunk_end = np.int(sino_start + nSino_per_chunk*(iChunk+1))
            print('\n  --------> [%i, %i]' % (sino_chunk_start, sino_chunk_end))
                    
            if sino_chunk_end > sino_end: 
                break

            sino = (int(sino_chunk_start), int(sino_chunk_end))
            # Reconstruct.
            proj, flat, dark, dummy = dxchange.read_aps_32id(h5fname, sino=sino)

            # Flat-field correction of raw data.
            data = tomopy.normalize(proj, flat, dark)                    

            # Write data as stack of TIFs.
            fname = os.path.dirname(fname) + '/' + os.path.splitext(os.path.basename(fname))[0]+ '_tiff/' + os.path.splitext(os.path.basename(fname))[0]
            print("Reconstructions: ", fname)
            dxchange.write_tiff_stack(data, fname=fname, start=strt)
            strt += sino[1] - sino[0]
    else:
        print("File Name does not exist: ", fname)

if __name__ == "__main__":
    main(sys.argv[1:])
