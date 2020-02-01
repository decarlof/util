

import dxfile.dxtomo as dx
import dxchange 

projfname = '/loca/data/proj_201.hdf'
fixedfmame = '/loca/data/proj_201.h5'

head_tail = os.path.split(projfname)
darkfname = head_tail[0] + os.sep + "proj_0203.hdf"
whitefname = head_tail[0] + os.sep + "proj_0202.hdf"

exchange_base = "exchange"

tomo_grp = '/'.join([exchange_base, 'data'])
flat_grp = '/'.join([exchange_base, 'data_white'])
dark_grp = '/'.join([exchange_base, 'data_dark'])
theta_grp = '/'.join([exchange_base, 'theta'])
tomo = dxreader.read_hdf5(projfname, tomo_grp)
flat = dxreader.read_hdf5(whitefname, flat_grp)
dark = dxreader.read_hdf5(darkfname, dark_grp)
theta = dxreader.read_hdf5(projfname, theta_grp)

# Open DataExchange file
f = dx.File(fixedfmame, mode='w') 

f.add_entry(dx.Entry.data(data={'value': data, 'units':'counts'}))
f.add_entry(dx.Entry.data(data_white={'value': data_white, 'units':'counts'}))
f.add_entry(dx.Entry.data(data_dark={'value': data_dark, 'units':'counts'}))
f.add_entry(dx.Entry.data(theta={'value': theta, 'units':'degrees'}))

f.close()