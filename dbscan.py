# -*- coding: utf-8 -*-
import numpy as np

def findDistance(n, arr):
    dist=np.sqrt(np.sum((arr-n)**2, axis=1))
    return dist
        
