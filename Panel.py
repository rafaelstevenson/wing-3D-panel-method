import numpy as np
from numpy import linalg as LA

def Panel(r1,r2,r3,r4):
    # To compute basis of the panel based on coordinate of cornerpoints 
    
    # Calculate vector A and chordwise vector (c)
    A = np.zeros(3)
    A = ((r2-r1) + (r4-r3))/2. # A is average chordwise vector of two sides
    c = A/LA.norm(A)           # c is normalization of A
    
    # Calculate another vector on the plane (B)
    B = r4 - r1
    
    # Calculate normal vector of the plane (v)
    v = np.cross(c,B)  # v is cross product of c and B
    v = v/LA.norm(v)   # normalization of v
    
    # Calculate tangential vector on the plane (t)
    t = np.cross(v,c)  # t is cross product of v and c
    
    # Calculate panel area (S)
    E  = r3 - r1        # define first vector in edge
    F  = r2 - r1        # define second vector in edge
    E1 = np.cross(B,E)  # cross product of first half-triangle
    F1 = np.cross(F,B)  # cross product of second half-triangle
    S1 = LA.norm(E1)    # area of first parallelogram
    S2 = LA.norm(F1)    # area of second parallelogram
    S  = 0.5*(S1 + S2)  # area of panel is half of area of parallelogram
    
    # Save c, t, v in r
    r = np.zeros(9)
    r[0:3] = c  # arah flowfield x
    r[3:6] = t  # arah tangensial y
    r[6:9] = v  # arah normal panel
    
    return r, S