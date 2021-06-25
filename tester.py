# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 18:46:18 2021

@author: dorwa
"""

import tester
import numpy as np
import pandas as pd


j = 0
def multikulti( *argv):
    y =np.array([0.0])
    for i in (argv) :
        
        y[j] = i**2
    return y
    
