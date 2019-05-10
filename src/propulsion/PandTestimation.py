# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:31:57 2019

@author: Jeije
"""

import numpy as np
import matplotlib.pyplot as plt

class Propulsion:
    def __init__(self):
        self.isp = 3546            #s
        self.Pspec = 70e3          #W/N
        self.g0 = 9.81#
        
    def thrust4mdot(self, mdot):
        T = mdot*self.isp*self.g0
        return T
    
    def power4thrust(self, thrust):
        P=thrust*self.Pspec
        return P
    
    def minisp@(self, V_b ,c_d, n_c):
        minisp=0.5*V_b*c_d/n_c/g0
        return minisp

        
    


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (response_model.py)
"""
if __name__ == "__main__":
    pr = Propulsion()
    
    
    cd = np.linspace(2.0,3.2,6)
    V_b= 7.8e3
    n_c = np.linspace()
    
    
    
    
    T,yout, xout=control.step_response(sys,return_x=True,transpose=True)
    plt.figure(1)
    plt.plot(T,xout)
    plt.yscale('log')