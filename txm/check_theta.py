#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check theta generation
"""

from __future__ import print_function

import os
import tomopy
import dxchange
import numpy as np


if __name__ == '__main__':
    # Set data collection angles as equally spaced between 0-180 degrees.
    theta_r = np.linspace(0. * np.pi / 180., 180. * np.pi / 180., 1501)
    theta_d = np.linspace(0, 180, 1501) * np.pi / 180.

    res = theta_r - theta_d
    for index in range(len(res)):
        print (res[index])
    
