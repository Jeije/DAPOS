# -*- coding: utf-8 -*-
"""
Created on Thu May  9 16:48:59 2019

@author: msjor
"""

import numpy as np
import matplotlib.pyplot as plt
def Drag_Thrust_Area_iteration(Isp, density,intake_eff, velocity, thrust_power):
    #Isp = specific impulse engine   #[s]
    massf_thrust = 1/(Isp*9.81)     #[kg/s/N]
    #intake_eff  intake efficiency
    #thrust_power =power needed per newton of thrust#[W/N]
    
    def A_to_Drag(A):
        return density*(velocity**2)*(1.+np.pi/6.)*np.sqrt(A/np.pi)*A
    
    def Drag_to_A(D):
        return np.cbrt((D/(density*velocity**2*(1+np.pi/6)))**2*np.pi)
    
    def thrust_to_A(T):
        return T/(density*velocity*intake_eff/massf_thrust)
    
    def A_to_thrust(A):
        return density*A*velocity*intake_eff/massf_thrust
    
    #intial estimate to be able to start the iteration later
    A_init = 0.0001   #[m^2]
    drag_init = A_to_Drag(A_init)
    thrust_init = A_to_thrust(A_init)
    
    #set testing values to intial values
    thrust_t = thrust_init
    drag_t = drag_init
    
    #set up lists for plotting
    areal = [A_init]
    dragl = [drag_init]
    thrustl = [thrust_init]
    
    #stop when iteration has converged
    while np.abs(thrust_t-drag_t)>0.00000001:
        
        #set drag equal to the thrust to move towards intersection
        drag = thrust_t
        #compute new area based on this drag value
        area =Drag_to_A(drag)
        #compute the thrust produced at this area
        thrust = A_to_thrust(area)
        #print to see difference between drag and thrust
        #print (drag-thrust)
        #set new testing values for next iteration
        drag_t = drag
        thrust_t = thrust
            
          
        areal.append(area)
        dragl.append(drag)
        thrustl.append(thrust)
        
    #plot results iteration
    plt.plot(areal, dragl, "red")
    plt.plot(areal,thrustl, "blue")
    plt.show()  
    
#    #print results 
#    print ("Area = ", area, "[m^2]")
#    print ("Thrust/Drag = ", drag, "[N]")
#    print ("Massflow =", area*density*velocity*intake_eff, "[kg/s]")
#    print ("Power required = ", thrust*thrust_power, "[W]")
    
    #return the results from function (area, thrust/drag, massflow, power required for engine)
    return area, drag, area*density*intake_eff,thrust*thrust_power


    ##plotting of both drag and thrust as a function of the inlet area for reference
    #area_list = np.arange(0.,10.,0.2)
    #drag_list = []
    #thrust_list = []
    #for i in area_list:
    #    drag_list.append(A_to_Drag(i))
    #    thrust_list.append(A_to_thrust(i))
    #    
    #plt.plot(area_list, drag_list, "red")
    #plt.plot(area_list, thrust_list, "blue")
    #plt.show()

