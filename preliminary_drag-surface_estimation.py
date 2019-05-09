# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:21:52 2019

@author: flori
"""
import numpy 
from math import pi, sqrt
import matplotlib.pyplot as plt

massflow = 0.22* (10**-6) /0.4 #[kg/s]
    
rho = [6*10**(-7), 6*10**(-8), 1.6*10**(-8), 2.7*10**(-9), 8.6*10**(-10), 3.4*10**(-10), 1.5*10**(-10), 6.8*10**(-11), 3.5*10**(-11), 2.5*10**(-11)]   #[kg/m^3]
alt = [100, 110, 120, 140, 160, 180, 200, 220, 240, 250]
V = 7800        #[m/s]


Intake = [massflow/(x*V) for x in rho] 
Other = 0.15

S = [x + Other for x in Intake]

CD = [2*(1+(pi/6)*sqrt(x/pi)) for x in S] 

steps = [rho[i]*S[i]*CD[i] for i in range(len(rho))]

D = [0.5*x*(V**2) for x in steps]

plt.plot(alt,S)
plt.plot(alt,D)

plt.show()