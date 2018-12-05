import dxchange
import dxchange.reader as dxreader
import tomopy

h5fname = '/local/data/2018-03/Lindley/Exp005_subsea_bolt_sample_1_26C_04_YPos12.2mm_FriMar23_15_11_42_2018_edge_2x_750mm_800.0msecExpTime_0.12DegPerSec_Rolling_20umLuAG_1mmAl15mmSi4mmSn0.5mmCu_0.0mrad_USArm1.25_monoY_-16.0_AHutch/proj_0005.hdf'

zinger_level = 800                  # Zinger level for projections
zinger_level_w = 1000               # Zinger level for white


# Read the txrm raw data.
start = 0
end = start + 2000
sino = (start, end)

# Read APS 32-BM raw data.
data, flat, dark, theta = dxchange.read_aps_32id(h5fname, sino=sino)

# zinger_removal
#proj = tomopy.misc.corr.remove_outlier(proj, zinger_level, size=15, axis=0)
#flat = tomopy.misc.corr.remove_outlier(flat, zinger_level_w, size=15, axis=0)
    
# Flat-field correction of raw data.
#data = tomopy.normalize(proj, flat, dark, cutoff=1.4)

dxchange.write_tiff_stack(data, fname='/local/data/2018-03/Lindley/Exp005_02/recon_')