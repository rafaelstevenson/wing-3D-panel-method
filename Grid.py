import numpy as np
import math as m
from scipy.interpolate import CubicSpline
from Load import Load_Airfoil
from Panel import Panel
from Convert import Convert

def Grid(input):
    # To generate grid of wing based on input
    
    # Extract input vars.
    cRoot = input[1] # root chord 
    cTip  = input[2] # tip chord
    xTip  = input[3] 
    zTip  = input[4] # beda jarak tinggi leading edge antara root dan tip
    b     = input[5] # wingspan 
    iB1   = input[7] # number of airfoil points
    jB    = input[8] # number of panel spanwise
    dxW   = input[9] # length of wake
    uInf  = input[10] # v in x direction
    wInf  = input[11] # v in z dirention
    gamma = input[15]
    dgamma = 0#gamma / input[13]
    #REMEMBER WE USE X, Z, Y [X ke kanan, Z ke atas, Y ke dalam]

    #=============================== Baca airfoil, interpolasi titik, buat panel 2D di airfoil
    # Load airfoil coordinates
    rA = Load_Airfoil(input[12])
    
    # Find LE
    dist = 0
    for i in range(len(rA[:,0])):
        temp = (rA[i,0]-rA[0,0])**2 - (rA[i,1]-rA[0,1])**2
        dist = max(dist,temp)
        if (dist != temp):
            nLE = i - 1
            break
  
    # Transform x coordinate to psi
    ch = np.abs(rA[nLE,0] - rA[0,0])
    psi = np.zeros(len(rA[:,0]))
    for i in range(len(rA[:,0])):
        phiA   = m.acos((rA[i,0]-0.5*ch)/(0.5*ch)) 
        if (i <= nLE):
            psi[i] = phiA
        elif (i >= nLE):
            psi[i] = 2*np.pi - phiA
            
    # Cubic spline yA as function of psi
    cs = CubicSpline(psi,rA[:,1])
        
    # Define new psi
    psiA = np.linspace(0,2*np.pi,iB1)
    
    # Compute new airfoil coordinate
    rB      = np.zeros([iB1,2])
    rB[:,0] = 0.5*ch*(1+np.cos(psiA))
    rB[:,1] = cs(psiA)
    
    # Check for direction of points
    area = 0
    for i in range(iB1-1):
        area = area + 0.5*(rB[i+1,0]-rB[i,0])*(rB[i+1,1]+rB[i,1])
    
    # If panels are CCW, flip them
    if (area < 0):
        rB = np.flipud(rB) 
    #================================================================================

    # Define number of panels
    iB  = iB1 - 1 #number of wing panel chordwise
    iB2 = iB1 + 1 #number of points chordwise
    jB1 = jB  + 1 #number of points spanwise
    
    # Initialization of qF, qC, r (c, t, v), S, sig
    qF  = np.zeros([iB2+input[13]-1,jB1,3]) # matriks axbx3 dengan besar [number of points chordwise, number of points spanwise, [x,y,z]]
    qC  = np.zeros([iB1+input[13]-1,jB,3]) # matriks axbx3 dengan besar [number of aifoil points, number of panelss spanwise, [x,y,z]]
    r   = np.zeros([iB1+input[13]-1,jB,9]) # matriks axbx9 [number of airfoil points, number of panels spanwise, [9]]
    S   = np.zeros([iB1+input[13]-1,jB]) # matriks axb [number of airfoil points, number of panels spanwise]
    sig = np.zeros([iB1+input[13]-1,jB]) # Source strength [number of airfoil points, number of panels spanwise]
    cR  = np.zeros([iB1+input[13]-1,jB,12]) # corner points [number of airfoil points, number of panels spanwise, 1x,1y,1z,2x,2y,2z,3x,3y,3z,4x,4y,4z]
    
    # Move airfoil data from rB to qF
    qF[0:iB1,0,0] = rB[:,0] # point arah x airfoil
    qF[0:iB1,0,2] = rB[:,1] # point arah z airfoil
    
    # Close TE point
    #nilai point paling depan bakal sama dengan nilai point sebelum wake
    qF[0,0,2] = 0.5*(qF[0,0,2]+qF[iB,0,2]) 
    qF[iB,0,2] = qF[0,0,2] 
    
    # Calculate panel cornerpoints
    for j in range(jB1):
        
        # Define y, LE position, and chord
        y    = (0.5*b/jB)*j #ngebikin chordnya jalan ke arah y
        dxLE = xTip*2*y/b  #ngebikin sayapnya sweep 
        dzLE = zTip*2*y/b  #ngebikin sayapnya dihedral
        chrd = cRoot - (cRoot - cTip)*2*y/b #local chord
        
        # c1                 
        # |             c2  } >dx
        # |            |
        # |  - - -> y  |  
        # |            |
        # |            |
        # |            |
        #              |
        #

        # Define cornerpoints of panels on wing
        for i in range(iB1):
            qF[i,j,0] = qF[i,0,0]*chrd + dxLE
            qF[i,j,1] = y 
            qF[i,j,2] = qF[i,0,2]*chrd + dzLE

        #===========================================ini di benerin lagi nanti ===================== !!!!!!
        # Define wake cornerpoints #calon perubahan
        #qF[iB1,j,0]   = qF[iB,j,0] + dxW
        #qF[iB1,j,1:2] = qF[iB,j,1:2]  #real code
        gamma  = input[15]
        #==========================================================================================!!!
        h = 0
        for i in range(input[13]): # 0-4
            qF[iB1+i,j,0] = qF[iB,j,0] + m.cos(m.radians(gamma))*(input[14] * (i+1)) 
            qF[iB1+i,j,1] = qF[iB,j,1]
            qF[iB1+i,j,2] = m.sin(m.radians(gamma))*(input[14] * (i+1)) + qF[iB1+i,j,2]
            #qF[iB1+i,j,2] = m.sin(m.radians(gamma))*(input[14] * (i+1)) + h
            # gamma ini sudut lengkungan wake clockwise
            if (gamma < 0):
                gamma += abs(dgamma)
            elif(gamma > 0):
                #if m.sin(m.radians(gamma))*(input[14] * (i+1)) > 0 :
                #    h = h + m.sin(m.radians(gamma))*(input[14] * (i+1))
                gamma -= abs(dgamma)

            elif(gamma == 0):
                gamma = 0
            #print(gamma)
        
        #==========================================================================================!!!!!!!! 
        #qF[iB1,j,0] = qF[iB,j,0] + m.cos(m.radians(gamma))*(dxW) 
        #qF[iB1,j,1] = qF[iB,j,1]
        #qF[iB1,j,2] = dxW * m.sin(m.radians(gamma))
        #==========================================================================================!!!!!!!!!
       #------- * menunjukkan lokasi 4 titik panel, gamma menunjukkan kemiringannya dia, liat low speed aero ada gambar wake lengkung (laporan edwin ada )
       # *  
       #   *
       #       *   
       #             *
       #                      *          *      *    
    #  starts from i = 0, j = 0 untuk * maupun o
    #
    #  *----------*----------*----------* 
    #  |          |          |          |          
    #  |          |          |          | 
    #  |    o     |    o     |    o     |  airfoil panel
    #  |          |          |          |
    #  |          |          |          |
    #  *----------*----------*----------*
    #  |          |          |          |
    #  |          |          |          |   airfoil panel
    #  |    o     |    o     |    o     |
    #  |          |          |          |
    #  |          |          |          |
    #  *----------*----------*----------*
    #  |          |          |          |
    #  |          |          |          | 
    #  |          |          |          |
    #  |    o     |    o     |    o     |
    #  |          |          |          |
    #  |          |          |          |  wake panel
    #  |          |          |          |  
    #  *----------*----------*----------*
    #
    # variabel yang mengisi * adalah qf
    # variable yang mengisi o adalah qc
    # di dalam o ada S, r, sigma, cR


    # Define wing collocation points
    for j in range(jB): #sebanyak number of panels wingspan
        for i in range(iB1 + input[13]-1): #sebanyak number of airfoil points  #diubahhhh
            qC[i,j,:] = (qF[i,j,:]+qF[i,j+1,:]+qF[i+1,j+1,:]+qF[i+1,j,:])/4.
            
            # Call panel subroutines
            r[i,j,:], S[i,j] = Panel(qF[i,j,:],qF[i+1,j,:],qF[i,j+1,:],qF[i+1,j+1,:])
            
            # Calculate sigma distribution
            sig[i,j] = r[i,j,6]*uInf + r[i,j,8]*wInf
            
            # Transform cornerpoints into panel frame of ref.
            cR[i,j,0:3]  = Convert(qC[i,j,:],qF[i,j,:],r[i,j,:])
            cR[i,j,3:6]  = Convert(qC[i,j,:],qF[i+1,j,:],r[i,j,:])
            cR[i,j,6:9]  = Convert(qC[i,j,:],qF[i+1,j+1,:],r[i,j,:])
            cR[i,j,9:12] = Convert(qC[i,j,:],qF[i,j+1,:],r[i,j,:])
    
    return qF, qC, r, S, sig, cR