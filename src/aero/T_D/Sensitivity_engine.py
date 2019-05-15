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

set_parameter = 1 + 3 # 1=collection_eff, 2=isp, 3=CD

n = 1;
k = 100


T_D = 1.0
collection_eff = np.array([[0.35]]) 
#                           [0.35],
#                           [0.4]])
isp =  np.array([[4000]])#s
CDA = np.array([[1, 2, 3, 4, 5, 6]])

g = 9.81 #m/s
P =  1000 #W
T_P = 14.147593*10**(-6) #N/W
T = T_P*P #N
massflow = T/(g*collection_eff*isp) #[kg/s]
if set_parameter == 3:
    o = len(collection_eff)
    m = np.count_nonzero(isp)
if set_parameter == 4:
    o = len(collection_eff)
    m = np.count_nonzero(CDA)
else:
    o = len(collection_eff)
    m = np.count_nonzero(isp)

    
#density = [5*10**(-5),5*10**(-6) ,5*10**(-7) , 1*10**(-8), 5*10**(-9),2.148*10**(-9), 1*10**(-9), 5*10**(-10), 3*10**(-10), 1*10**(-10), 8*10**(-11),5*10**(-11)]   #[kg/m^3]
altitude = range(150, 250)

Earth_R = 6371000 #m
G = 6.674*10**(-11) #m^3/kgs^2
Earth_M = 5.972*10**24 #kg

D = np.zeros((k,o,m))
P = np.zeros((k,o,m))
#CDA = np.zeros((k,o,m))
CDA_design = np.zeros((k,o,m))
S = np.zeros((k,o,m))
dens = np.zeros(k)
#CD = np.zeros((k,o,m))

for b in range(k):
    alt = altitude[b]
    dens[b] = nlrmsise00_dens(alt)
    rho = dens[b]
    D_design = T/T_D
    V = sqrt(G*Earth_M/(Earth_R+alt))        #[m/s]

    Intake = massflow*(rho*V)**(-1)
    non_intake = 0.2
    s = Intake + non_intake
    
        
    S[b][:][:] = s
    CDA_design[b][:][:] = D_design/(0.5*rho*V**2) 
#    Cd = np.zeros((o,m))
#    for i in range(o):
#        for j in range(m):
#            Cd[i][j] = CD_change[i][j]*2*(1+(pi/6)*sqrt(s[i][i]/pi)) 
#    CD[b][:][:] = Cd

    D[b][:][:] = 0.5*(rho*CDA*(V**2))
    
#    CDA[b][:][:] = D[b][:][:]/(0.5*rho*V**2)  


plt.plot(altitude,CDA_design[:,0,0], linestyle='--')


colors = np.array([['m','y','c','k','b','g']])
names = np.array([['CDA = 1', 'CDA = 2', 'CDA = 3', 'CDA = 4', 'CDA = 5', 'CDA = 6']])
for u in range(m):
    plt.axhline(y=CDA[0][u], linestyle='-', color=colors[0][u], label=names[0][u])
    
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.title('CDA Sensitivity')
plt.xlabel('Altitude [km]')
plt.ylabel('CDA [-]')

plt.ylim((0,8))  
plt.xlim(150,250)


plt.show()
    
