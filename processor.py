# -*- coding: utf-8 -*-
import numpy as np

def findDistance(n, arr, e):
    dist=np.sqrt(np.sum((arr-n)**2, axis=1))
    #return the index of all such points that satisfy the condition val<e
    return np.where(dist<=e)[0]     #return the array part of tuple