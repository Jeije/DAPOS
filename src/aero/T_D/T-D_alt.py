# -*- coding: utf-8 -*-
"""
Created on Fri May 10 12:03:12 2019

@author: flori
"""
from collections import OrderedDict
import matplotlib.pyplot as plt
from matplotlib import *
from math import *
import numpy as np
from nrlmsise_00_header import *
from nrlmsise_00_data import *
from nrlmsise_00_start import *
from nlrmsise_00_dens import *

n = 1;
k = 100


T_D = 1.0
collection_eff = np.array([[0.35]])
isp =  np.array([[4000]])#s
g = 9.81 #m/s
P =  1000 #W
T_P = 14.147593*10**(-6) #N/W
T = T_P*P #N
massflow = T/(g*collection_eff*isp) #[kg/s]
o = len(collection_eff)
w = np.count_nonzero(isp)

#density = [5*10**(-5),5*10**(-6) ,5*10**(-7) , 1*10**(-8), 5*10**(-9),2.148*10**(-9), 1*10**(-9), 5*10**(-10), 3*10**(-10), 1*10**(-10), 8*10**(-11),5*10**(-11)]   #[kg/m^3]
altitude = range(150, 250)

Earth_R = 6371000 #m
G = 6.674*10**(-11) #m^3/kgs^2
Earth_M = 5.972*10**24 #kg

D = np.zeros((k,o,w))
P = np.zeros((k,o,w))
CD = np.zeros((k,o,w))
S = np.zeros((k,o,w))
dens = np.zeros(k)

for b in range(k):
    alt = altitude[b]
    dens[b] = nlrmsise00_dens(alt)
    rho = dens[b]
    D_design = T/T_D
    V = sqrt(G*Earth_M/(Earth_R+alt))        #[m/s]

    Intake = massflow*(rho*V)**(-1)
    non_intake = 0.2
    if Intake < 1:
        s = Intake + non_intake
    else:
        s = 1.2* Intake
    
    S[b][:][:] = s
    
    Cd = np.zeros((o,w))
    for i in range(o):
        for j in range(w):
            Cd[i][j] = 0.9*2*(1+(pi/6)*sqrt(s[i][j]/pi)) 
    CD[b][:][:] = Cd

    D[b][:][:] = 0.5*(rho*s)*Cd*(V**2)
    


print(D_design)   
for t in range(w):
    plt.plot(altitude,D[:,o-1,t], color='r', label='efficiency = 0.35')
    plt.axhline(y=D_design, color='k' , linestyle='-')
    #axhline(D_design)
    plt.ylim((0,.02))  
    plt.xlim(180,200)

#    plt.plot(altitude,D[:,o-2,t], color='m', label='efficiency = 0.40')
#    plt.plot(altitude,D[:,0-3,t], color='y', label='efficiency = 0.35')
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())


plt.show()
    
