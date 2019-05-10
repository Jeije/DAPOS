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
        
    


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (response_model.py)
"""
if __name__ == "__main__":
    pr = Propulsion()
    
    
    
    
    
    
    
    T,yout, xout=control.step_response(sys,return_x=True,transpose=True)
    plt.figure(1)
    plt.plot(T,xout)
    plt.yscale('log')