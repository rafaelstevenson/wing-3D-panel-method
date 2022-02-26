import numpy as np
import math as m

def Influence(rC,cR):
    # To compute influence coefficient of panel (cR) to point rC
    
    eps = 0.000001
    rF  = np.reshape(cR,(4,3))
    
    # Calculate distance for 'Influence Calculation'
    r  = np.zeros(4)
    e  = np.zeros(4)
    h  = np.zeros(4)
    d  = np.zeros(4)
    for i in range(4):
        r[i] = np.sqrt((rC[0]-rF[i,0])**2 + (rC[1]-rF[i,1])**2 + rC[2]**2)
        e[i] = (rC[0]-rF[i,0])**2 + rC[2]**2
        h[i] = (rC[0]-rF[i,0])*(rC[1]-rF[i,1])
        if (i != 3):
            d[i] = np.sqrt((rF[i+1,0]-rF[i,0])**2 + (rF[i+1,1]-rF[i,1])**2)
        else:
            d[i] = np.sqrt((rF[0,0]-rF[i,0])**2 + (rF[0,1]-rF[i,1])**2)
    
    # Calculate 'Influence Component'
    s = np.zeros(4)
    q = np.zeros(4)
    A = 0
    B = 0
    for i in range(4):
        if (d[i] < eps):
            s[i] = 0
            q[i] = 0
        else:
            if (i != 3):
                F    = (rF[i+1,1]-rF[i,1])*e[i] - (rF[i+1,0]-rF[i,0])*h[i]
                G    = (rF[i+1,1]-rF[i,1])*e[i+1] - (rF[i+1,0]-rF[i,0])*h[i+1]
                num  = rC[2]*(rF[i+1,0]-rF[i,0])*(F*r[i+1]-G*r[i])
                den  = (rC[2]*(rF[i+1,0]-rF[i,0]))**2*r[i]*r[i+1] + F*G
                q[i] = m.atan2(num,den)
                num  = (rC[0]-rF[i,0])*(rF[i+1,1]-rF[i,1])
                num  = num - (rC[1]-rF[i,1])*(rF[i+1,0]-rF[i,0])
                s[i] = (num/d[i])*m.log((r[i]+r[i+1]+d[i])/(r[i]+r[i+1]-d[i]))
            else:
                F = (rF[0,1]-rF[i,1])*e[i] - (rF[0,0]-rF[i,0])*h[i]
                G = (rF[0,1]-rF[i,1])*e[0] - (rF[0,0]-rF[i,0])*h[0]
                num  = rC[2]*(rF[0,0]-rF[i,0])*(F*r[0]-G*r[i])
                den  = (rC[2]*(rF[0,0]-rF[i,0]))**2*r[i]*r[0] + F*G
                q[i] = m.atan2(num,den)
                num  = (rC[0]-rF[i,0])*(rF[0,1]-rF[i,1])
                num  = num - (rC[1]-rF[i,1])*(rF[0,0]-rF[i,0])
                s[i] = (num/d[i])*m.log((r[i]+r[0]+d[i])/(r[i]+r[0]-d[i]))
                
        A = A + q[i]
        B = B + s[i]
        
    A = - A/(4*np.pi)
    if (abs(rC[2]) < eps):
        A = 0
        
    B = - B/(4*np.pi) - rC[2]*A
    
    return A, B