import process_variables as pv
import numpy as np
from time import *


def ff_norm_off():
    wait = 50
    pv.ccd_EnableFlatField.put(0, wait=True, timeout=wait) # disable the flat-field
    print '*** Flat-field disabled...'

    return
    
