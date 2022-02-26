import numpy as np

def Force_Calculation(input,qF,qC,r,S,mu):
    # To calculate force on wing
    
    # Extract input vars.
    cRoot = input[1]
    cTip  = input[2]
    xTip  = input[3]
    zTip  = input[4]
    b     = input[5]
    vInf  = input[6]
    iB1   = input[7]
    jB    = input[8]
    dxW   = input[9]
    uInf  = input[10]
    wInf  = input[11]
    
    # Number of wing panel chordwise
    iB  = iB1 - 1
    
    # Initialization of array
    Cp = np.zeros([iB,jB])
    dL = np.zeros([iB,jB])
    dD = np.zeros([iB,jB])
    CL = 0
    CD = 0
    CM = 0
    
    rF = np.zeros(3)
    rR = np.zeros(3)
    d2 = np.zeros(3)
    d3 = np.zeros(3)
    dr = np.zeros(3)
    
    # Compute velocity using finite difference
    for j in range(jB):
        for i in range(iB):
            i1 = i - 1
            i2 = i + 1
            j1 = j - 1
            j2 = j + 1
            if (i == 0):
                i1 = 0
            if (i == (iB-1)):
                i2 = iB - 1
            if (j == 0):
                j1 = 0
            if (j == (jB-1)):
                j2 = jB - 1
            
            rF[:] = 0.5*(qF[i+1,j,:] + qF[i+1,j+1,:])
            rR[:] = 0.5*(qF[i,j,:] + qF[i,j+1,:])
            d2[:] = qC[i2,j,:] - rF
            d3[:] = qC[i1,j,:] - rR
            dl1   = np.linalg.norm(rF-rR)
            dl2   = np.linalg.norm(d2)
            dl3   = np.linalg.norm(d3)
            dll   = dl1 + dl2 + dl3
            if (i == 0):
                dll = dl1/2 + dl2
            if (i == (iB-1)):
                dll = dl1/2 + dl3
            ql    = - (mu[i2,j] - mu[i1,j])/dll
            dr[:] = qC[i,j2,:] - qC[i,j1,:]
            delR  = np.linalg.norm(dr)
            qm    = - (mu[i,j2] - mu[i,j1])/delR
            ql    = ql + qm*(dr[0]**2 + dr[2]**2)/delR
            qm    = qm*(dr[1]**2 + dr[2]**2)/delR
            qInf  = uInf*r[i,j,8] - wInf*r[i,j,6]
            Cp[i,j] = 1.0 - ((qInf + ql)**2 + qm**2)/(vInf**2)
            dL[i,j] = - Cp[i,j]*S[i,j]*r[i,j,8]
            dD[i,j] = Cp[i,j]*S[i,j]*r[i,j,6]
            CL = CL + dL[i,j]
            CD = CD + dD[i,j]
            CM = CM + dL[i,j]*qC[i,j,0]

    # Compute mean aerodynamic chord
    lam   = cTip/cRoot
    cMean = (2*cRoot/3)*(1+lam+lam**2)/(1+lam)
    
    # Compute force coefficient
    CL = CL/(0.25*(cRoot+cTip)*b)
    CD = CD/(0.25*(cRoot+cTip)*b)
    CM = CM/(0.25*(cRoot+cTip)*b*cMean)
    
    return Cp, CL, CD, CM