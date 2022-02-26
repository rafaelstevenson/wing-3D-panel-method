import numpy as np
from Convert import Convert
from Influence import Influence

def Compute_A_RHS(input,qF,qC,r,S,sig,cR):
    # To compute matrix A (influence matrix) and vector RHS
    # Input is wing geometry
    
    # Extract input vars.
    cRoot = input[1] # root chord 
    cTip  = input[2] # tip chord
    xTip  = input[3] # beda jarak leading edge antara root dan tip
    zTip  = input[4] # beda jarak tinggi leading edge antara root dan tip
    b     = input[5] # wingspan 
    vInf  = input[6] # v infinity
    iB1   = input[7] # number of airfoil points
    jB    = input[8] # number of panel spanwise
    dxW   = input[9] # length of wake
    uInf  = input[10] # v in x direction
    wInf  = input[11] # v in z dirention
    
    # Number of wing panel chordwise
    iB    = iB1 - 1
    
    # Initialization of matrix and vector
    A    = np.zeros([iB*jB,iB*jB])
    rhs  = np.zeros(iB*jB)
    dDub = np.zeros(jB)
    qCi  = np.zeros(3)
    
    k    = - 1
    for i in range(iB):
        for j in range(jB):
            k  = k + 1 # Control panel counter
            l  = - 1
            rh = 0
            # Define image of control panel
            qCi[:] = qC[i,j,:]
            qCi[1] = - qCi[1]
            dDub[:] = 0.0
            for i1 in range(iB):
                for j1 in range(jB):
                    l = l + 1 # Influence panel counter
                    #===============================ini nanti di benerin lagi ====================
                    if (i1 == 0):
                        '''
                        # Convert control panel to wake panel frame of ref.
                        rC = Convert(qC[iB,j1,:],qC[i,j,:],r[iB,j1,:])
                        
                        # Calculate wake influence
                        wDub, dSig = Influence(rC,cR[iB,j1,:])
                        
                        # Convert image to wake panel frame of ref.
                        rC = Convert(qC[iB,j1,:],qCi,r[iB,j1,:])
                        
                        # Calculate image influence
                        wDub1, dSig = Influence(rC,cR[iB,j1,:])
                        
                        # Save wake doublet influence
                        dDub[j1] = wDub + wDub1
                        dMu2 = dDub[j1]
                        '''
                        
                        for y in range(input[13]):
                            rC = Convert(qC[iB+y,j1,:],qC[i,j,:],r[iB+y,j1,:])
                        
                            wDub, dSig = Influence(rC,cR[iB+y,j1,:])
                        
                            rC = Convert(qC[iB+y,j1,:],qCi,r[iB+y,j1,:])
                         
                            wDub1, dSig = Influence(rC,cR[iB+y,j1,:])
                        
                            dDub[j1] += wDub + wDub1
                            # cara ini gakepake kalo wakenya dipotong-potong, butuh cara lain.
                            # pake += atau = aja?? 
                        dMu2 = dDub[j1]
                        
                    else:
                        dMu2 = 0.
                        
                    if (i1 == (iB-1)):
                        dMu2 = - dDub[j1]
                    #===============================================================================    
                    # Convert control panel to influence panel frame of ref.
                    rC = Convert(qC[i1,j1,:],qC[i,j,:],r[i1,j1,:])
                    
                    # Calculate panel influence
                    dMu, dSig = Influence(rC,cR[i1,j1,:])
                    if (i1 == i and j1 == j):
                        dMu = - 0.5
                        
                    # Convert image to influence panel frame of ref.
                    rC = Convert(qC[i1,j1,:],qCi,r[i1,j1,:])
                    
                    # Calculate panel influence
                    dMu1, dSig1 = Influence(rC,cR[i1,j1,:])
                    
                    # Influence matrix coefficient
                    A[k,l] = dMu + dMu1 - dMu2   # matriks A udah dikali sama negatif. jadi persamaanya -Axmu = Bxsigma
                    rh     = rh + (dSig + dSig1)*sig[i1,j1]
                    
            rhs[k] = rh
            
    return A, rhs