import numpy as np

def Convert(rO,rB,r):
    # To convert rB into panel frame of ref. (rO and r)
    #
    # rO is origin coordinate (frame of ref.)
    # rB is coordinate to be converted
    # r  is basis of panel in array 1D
    
    r  = np.reshape(r,(3,3))  # reshape r to 3x3
    rP = np.matmul(r,(rB-rO)) # basis * relative coordinate
    
    return rP