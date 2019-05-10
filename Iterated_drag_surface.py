# -*- coding: utf-8 -*-
"""
Created on Thu May  9 16:48:59 2019

@author: msjor
"""

import numpy as np
import matplotlib.pyplot as plt
Isp = 3300   #[s]
#massf_thrust_lit = 0.0306834  #[mg/s/mN]
#massf_thrust = massf_thrust_lit*10**-3  #[kg/s/N]
massf_thrust = 1/(Isp*9.81)
density = 1*10**-10   #[kg/m^3]
velocity = 7800     #[m/s]
intake_eff = 0.4    #[-]
thrust_power = 20*10**3 #[W/N]

def A_to_Drag(A):
    return density*(velocity**2)*(1.+np.pi/6.)*np.sqrt(A/np.pi)*A

def Drag_to_A(D):
    return np.cbrt((D/(density*velocity**2*(1+np.pi/6)))**2*np.pi)

def thrust_to_A(T):
    return T/(density*velocity*intake_eff/massf_thrust)

def A_to_thrust(A):
    return density*A*velocity*intake_eff/massf_thrust


A_init = 0.0001   #[m^2]
drag_init = A_to_Drag(A_init)
thrust_init = A_to_thrust(A_init)

thrust_t = thrust_init
drag_t = drag_init

areal = [A_init]
dragl = [drag_init]
thrustl = [thrust_init]
while np.abs(thrust_t-drag_t)>0.00000001:

    drag = thrust_t
    area =Drag_to_A(drag)
    thrust = A_to_thrust(area)
    print (drag-thrust)
    drag_t = drag
    thrust_t = thrust
        
      
    areal.append(area)
    dragl.append(drag)
    thrustl.append(thrust)
    

plt.plot(areal, dragl, "red")
plt.plot(areal,thrustl, "blue")
plt.show()  
   
print ("Area = ", area, "[m^2]")
print ("Thrust/Drag = ", drag, "[N]")
print ("Massflow =", area*density*velocity*intake_eff, "[kg/s]")
print ("Power required = ", thrust*thrust_power, "[W]")


area_list = np.arange(0.,10.,0.2)
drag_list = []
thrust_list = []
for i in area_list:
    drag_list.append(A_to_Drag(i))
    thrust_list.append(A_to_thrust(i))
    
plt.plot(area_list, drag_list, "red")
plt.plot(area_list, thrust_list, "blue")
plt.show()

