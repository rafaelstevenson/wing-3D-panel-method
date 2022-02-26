Wing Simulation Code

Run Program :
-> Run Main.py 
 
In input section:
-> we can change the airfoil geometry by inputting the file name (Make sure that the airfoil exists inside the Airfoil_DAT_Selig folder, if not just add the .dat inside that folder)

-> we can also change the wing geometry (include: root chord, tip chord, wing swept, and wing span in meter)

-> we can also change the number of grid by determining the number of airfoil points and number of panel spanwise (recommend : 51 airfoil points and 9 wing span panels (half span) for good result)

-> we can choose the aerodynamic input (angle of attack, and free stream velocity)

The program function includes grid generation, aerodynamic calculation, force calculation, and visualization

Output:
-> CL, CM, and time will be shown on the console
-> Panel.dat will be printed out

For visualization using ParaView:
-> run print_vtu.cpp using c++ compiler (It will convert Panel.dat into Panel.vtu which can be read by ParaView)

if using MinGW : type 	-> g++ print_vtu.cpp
						->./a.exe

Panel.vtu file will be created

Visualization (Inside ParaView):
(Install first, if it has not been installed)

Open file -> choose Panel.vtu
change Soild color to -> cp (to visualize the pressure coefficient)
change surface to -> surface with edges (to visualize the wing panels)
opacity could be changed for transparency







