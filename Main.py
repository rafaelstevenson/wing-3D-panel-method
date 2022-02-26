import numpy as np
from Grid import Grid
from Compute_A_RHS import Compute_A_RHS
from Force_Calculation import Force_Calculation

import time

# starting time
start = time.time()
# %% INPUT

input = [2.0,        # alpha
         1.0,        # cRoot (root chord)
         #0.6,        # cTip  (tip chord)
         0.8,0.0,
         #0.1,        # xTip  (aft sweep of tip)
         0.0,        # zTip  (aft sweep of tip)
         10.0,       # b     (span)
         1.0,        # vInf  (freestream vel.)
         int(51),   # iB1   (number of airfoil points)
         int(9)]     # jB    (number of panel spanwise (half span))

input.append(input[5]*100)                        # dxW  (length of wake) ## PERHATIIN DXW
input.append(input[6]*np.cos(input[0]*np.pi/180)) # uInf (v in x dir.)
input.append(input[6]*np.sin(input[0]*np.pi/180)) # wInf (v in z dir.)

# Airfoil name
input.append('naca4412')    

#input new
wake_divider = 9 ## WAKE DIVIDER
input.append(wake_divider) #jadi input 13
len_per_wake = input[9]/wake_divider
input.append(len_per_wake) #jadi input 14
gamma = 2.0 #input 15
input.append(gamma)

# Extract iB1 and jB
iB1   = input[7]
jB    = input[8]

# %% GRID GENERATION

# Grid generation using function
qF, qC, r, S, sig, cR = Grid(input)

iB  = iB1 - 1 # number of wing panel chordwise
iB2 = iB1 + 1 # number of points chordwise
jB1 = jB  + 1 # number of points spanwise

# %% AERODYNAMIC CALCULATIONS

# Compute matrix A and vector RHS using function
A, rhs = Compute_A_RHS(input,qF,qC,r,S,sig,cR)

# Solve the system of equation for doublet strength mu
mu1 = np.linalg.solve(A,rhs)

# Reshape vector mu1 into matrix of panel
mu  = np.zeros([iB1,jB])
mu[0:iB,:] = np.reshape(mu1,(iB,jB))

# Compute doublet strength for wake
for j in range(jB):
    mu[iB,j] = mu[0,j] - mu[iB-1,j]

# %% FORCE CALCULATIONS

# Calculate force coefficient for wing using function
Cp, Cl, Cd, Cm = Force_Calculation(input,qF,qC,r,S,mu) 

print('CL :',Cl)
print('CM :',Cm)

# end time
end = time.time()

# total time taken
print(f"Runtime of the program is {end - start}")

#%% Visualization

file1 = open("Panel.dat","w") 
#file1.write("Hello \n") 
#file1.write("%d %d\n" % ((iB1)*jB1,(iB)*jB))
file1.write("%d %d\n" % ((iB1+wake_divider)*jB1,(iB+wake_divider)*jB)) #number of nodes & number of elements

#print nodes
index = 0
#nodes = np.zeros((iB1*jB1,3))
nodes = np.zeros(((iB1+wake_divider)*jB1,3))
#for i in range(iB1):
#    for j in range(jB1):
for i in range(iB1+wake_divider):
    for j in range(jB1):
        file1.write("%d " %(index+1))
        for k in range(3):
            nodes[index][k] = qF[i][j][k]
            file1.write("%f " % (nodes[index][k]))
        file1.write("\n")
        index += 1
        
#print elements(panel)
index = 0
#elem = np.zeros((iB*jB,4))
elem = np.zeros(((iB+wake_divider)*jB,4))
for i in range(iB+wake_divider):
    for j in range(jB):
        elem[index][0] = i*jB1 + j
        elem[index][1] = i*jB1 + (j+1)
        elem[index][2] = (i+1)*jB1 + (j+1)
        elem[index][3] = (i+1)*jB1 + j
        
        file1.write("%d %d %d %d %d %d\n" % (index+1,9,elem[index][0]+1,elem[index][1]+1,elem[index][2]+1,elem[index][3]+1)) 
        index += 1

#print data at each element
index = 0
data = np.zeros((iB*jB,2)) #cp and area
for i in range(iB):
    for j in range(jB):
        data[index][0] = Cp[i][j]
        data[index][1] = S[i][j]
        
        file1.write("%d %f %f\n" % (index+1,data[index][0],data[index][1])) 
        index += 1
file1.close()









