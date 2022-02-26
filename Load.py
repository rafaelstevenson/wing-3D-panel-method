import numpy as np
import os

def Load_Airfoil(fileName):
    # To load airfoil coordinate from .dat file in repo Airfoil_DAT_Selig
    
    # Define the number of header lines in the file
    hdrlns = 1
    if (fileName == 'nasasc2-0714'):
        hdrlns = 3
    elif (fileName == 's1020'):
        hdrlns = 2
        
    # Load the data from the text file
    crpth = os.path.dirname(__file__)
    flpth = crpth +"/Airfoil_DAT_Selig/"
    flnm = flpth + fileName + ".dat"
    dataBuffer = np.loadtxt(flnm,skiprows=hdrlns)
    
    return dataBuffer