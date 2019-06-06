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
from nlrmsise_00_dens_max import *

set_parameter = 1 + 2 # 1=collection_eff, 2=isp, 3=CD

n = 1;
k = 150
f=2.1813361684615

T_D = 1.0
collection_eff = np.array([[0.325]]) 
#                           [0.35],
#                           [0.4]])
isp =  np.array([[3500]])#s
CD = np.array([[2.5]])

g = 9.81 #m/s
P =  1500 #W
T_P_init = 14.147593*10**(-6) #N/W
T_P = np.array([[(20*10**(-6))/f, (30*10**(-6))/f, (40*10**(-6))/f]])
T = np.array(T_P*P) #N
massflow = T/(g*collection_eff*isp) #[kg/s]
m = np.count_nonzero(T_P)
o = np.count_nonzero(collection_eff)

    
#density = [5*10**(-5),5*10**(-6) ,5*10**(-7) , 1*10**(-8), 5*10**(-9),2.148*10**(-9), 1*10**(-9), 5*10**(-10), 3*10**(-10), 1*10**(-10), 8*10**(-11),5*10**(-11)]   #[kg/m^3]
altitude = range(150, 300)

Earth_R = 6371000 #m
G = 6.674*10**(-11) #m^3/kgs^2
Earth_M = 5.972*10**24 #kg

D = np.zeros((k,o,m))
D_max = np.zeros((k,o,m))
P = np.zeros((k,o,m))
#CDA = np.zeros((k,o,m))
CDA_design = np.zeros((k,o,m))
CDA_design_max = np.zeros((k,o,m))
S = np.zeros((k,o,m))
dens = np.zeros(k)
dens_max = np.zeros(k)
#CD = np.zeros((k,o,m))

for b in range(k):
    alt = altitude[b]
    dens[b] = nlrmsise00_dens_max(alt)
    dens_max[b] = nlrmsise00_dens_max(alt)
    rho = dens[b]
    rho_max = dens_max[b]
    D_design = T/T_D
    V = sqrt(G*Earth_M/(Earth_R+alt))        #[m/s]

    Intake = massflow*(rho*V)**(-1)
    Intake_max = massflow*(rho_max*V)**(-1)
    non_intake = 0.2
    s = Intake + non_intake
    s_max = Intake_max + non_intake
        
    S[b][:][:] = s
#    CDA_design[b][:][:] = D_design/(0.5*rho*V**2) 
#    CDA_design_max[b][:][:] = D_design/(0.5*rho_max*V**2)
#   Cd = np.zeros((o,m))
#    for i in range(o):
#        for j in range(m):
#            Cd[i][j] = CD_change[i][j]*2*(1+(pi/6)*sqrt(s[i][i]/pi)) 
#    CD[b][:][:] = Cd

    D[b][:][:] = 0.5*(rho*CD*s*(V**2))
    D_max[b][:][:] = 0.5*rho_max*CD*s*V**2
#    CDA[b][:][:] = D[b][:][:]/(0.5*rho*V**2)  


#plt.plot(altitude, D[:,0,0], linestyle='--', label='Min. CDA for min. density')
plt.plot(altitude, D[:,0,0], linestyle='--', color='g', label='T/P = 9.17 mN/kW')
plt.plot(altitude, D[:,0,1], linestyle='-', color='y', label='T/P = 13.8 mN/kW')
plt.plot(altitude, D[:,0,2], linestyle=':', color='k', label='T/P = 18.3 mN/kW')


plt.axhline(y=D_design[0][0], linestyle='--', color='g', label='T/P = 9.17 mN/kW')
plt.axhline(y=D_design[0][1], linestyle='-', color='y', label='T/P = 13.8 mN/kW')
plt.axhline(y=D_design[0][2], linestyle=':', color='k', label='T/P = 18.3 mN/kW')

x_loc = np.zeros(3)
for a in range(3):
    for n in range(k):
        if (D[n,0,a] - D_design[0][a]) < 0.00000000001:
            x_loc[a] = n
            break

r = int(x_loc[0])
v = int(x_loc[1])
e = int(x_loc[2])

x0 = [altitude[r], D[r,0,0]]
x1 = [altitude[v], D[v,0,0]]
x2 = [altitude[e], D[e,0,2]]

less = (x_loc[0]-x_loc[1])/abs((1-(T_P[0][0]/T_P[0][1]))*100)
more = (x_loc[1]-x_loc[2])/abs((1-(T_P[0][2]/T_P[0][1]))*100)

plt.plot([x0[0], x2[0]], [x0[1], x2[1]], color='k', linestyle='-', marker='')

plt.xlim(150,300)
plt.ylim(0.005,0.03)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.title('Thrust/Power-ratio Sensitivity')
plt.xlabel('Altitude [km]')
plt.ylabel('D [N]')

  


plt.show()
    
