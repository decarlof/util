'''
    Log PV in a file
    
'''
from __future__ import print_function

import datetime
import time

from epics import PV

variableDict = {'PreDarkImages': 0,
        'PreWhiteImages': 0,
        'Projections': 1500,
        'PostDarkImages': 20,
        'PostWhiteImages': 20,
        'SampleXIn': 0.0,
        'SampleXOut': 5,
        'SampleRotStart': 0.0,
        'SampleRotEnd': 180.0,
        'ExposureTime': 0.1,
        'IOC_Prefix': 'PCOIOC3:', 
        'EnergyMono': 24.9,
        'Station': '2-BM-A'
        }

global_PVs = {}


def init_general_PVs(global_PVs, variableDict):

    # shutter PVs
    global_PVs['LoadVoltage'] = PV('2bmS1:D1Dmm_raw')
    global_PVs['LoadNewton'] = PV('2bmS1:D1Dmm_calc')
    global_PVs['HDF1_FullFileName_RBV'] = PV(variableDict['IOC_Prefix'] + 'HDF1:FullFileName_RBV')


def main():

    logfile = 'load'
    fname = logfile + '.txt'
    
    init_general_PVs(global_PVs, variableDict)
    try:
        with open(fname, 'a+') as f:
            while True:
                f.write('%s %s; Load: %4.4f V %4.4f N\n' % (global_PVs['HDF1_FullFileName_RBV'].get(), \
                        datetime.datetime.now().isoformat(), global_PVs['LoadNewton'].get(), \
                        global_PVs['LoadVoltage'].get()))
                print('%s %s; Load: %4.4f V %4.4f N' % (global_PVs['HDF1_FullFileName_RBV'].get(), \
                        datetime.datetime.now().isoformat(), global_PVs['LoadNewton'].get(), \
                        global_PVs['LoadVoltage'].get()))
                time.sleep(2)	
    except KeyboardInterrupt:
	
        print('interrupted!')
    
    
if __name__ == '__main__':
    main()
