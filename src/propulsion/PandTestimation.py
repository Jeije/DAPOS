# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:31:57 2019

@author: Jeije
"""

import numpy as np
import matplotlib.pyplot as plt
import nrlmsise_00 as atm

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
    
    def minisp(self, V_b ,c_d, n_c):
        isp=0.5*V_b*c_d/n_c/self.g0
        return isp

        
    


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (response_model.py)
"""
if __name__ == "__main__":
    pr = Propulsion()
    thing=2
    
    if thing==1:
        c_d = np.linspace(2.0,3.2,6)
        V_b= 7.8e3
        n_c = np.linspace(0.1,0.6,20)
        
        minispvec=np.vectorize(pr.minisp)
        
        out=[]
        for x in range(len(c_d)):
            out.append(minispvec(V_b,c_d[x],n_c))
            plt.plot(n_c,out[x])
            
        
        print(out)
            
        plt.ylim(0,4000)
        plt.xlim(0.2,0.6)
        plt.ylabel("ISP (s)")
        plt.xlabel("Collection efficiency (-)")
        plt.show()
    elif thing==2:
        print("hoi")
    else:
        print("8==D")
        