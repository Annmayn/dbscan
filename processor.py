# -*- coding: utf-8 -*-
import numpy as np

#finds distance between point n and every point in arr
def findNeighbor(n, arr, e):
    #ultimately finds all neighbor points within radius e from point n
    #size of n: (1,2) or (2,)
    #size of arr: (x, 2) ; x=number of points in problem domain
    dist=np.sqrt(np.sum((arr-n)**2, axis=1))
    #return the index of all such points that satisfy the condition distance <= e
    return np.where(dist<=e)[0]     #return the array part of tuple