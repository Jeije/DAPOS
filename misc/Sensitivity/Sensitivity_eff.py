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
collection_eff = np.array([[0.25], 
                           [0.325],
                           [0.40],
                           [0.291]])
isp =  np.array([[3500]])#s
CD = np.array([[2.5]])

g = 9.81 #m/s
P =  1500 #W
T_P = (30e-6)/f #N/W
T = T_P*P #N
massflow = T/(g*collection_eff*isp) #[kg/s]
if set_parameter == 3:
    o = np.count_nonzero(collection_eff)
    m = np.count_nonzero(isp)
if set_parameter == 4:
    o = len(collection_eff)
    m = np.count_nonzero(CD)
else:
    o = len(collection_eff)
    m = np.count_nonzero(isp)

    
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

alt_loc = np.zeros(o)
for a in range(o):
    for n in range(k):
        if (D[n,a,0] - D_design) < 0.00000000001:
            alt_loc[a] = n
            break
less = (alt_loc[1]-alt_loc[0])/abs((1-(collection_eff[3][0]/collection_eff[1][0]))*100)
more = (alt_loc[3]-alt_loc[1])/abs((1-(collection_eff[2][0]/collection_eff[1][0]))*100)

#plt.plot(altitude, D[:,0,0], linestyle='--', label='Min. CDA for min. density')
plt.plot(altitude, D[:,0,0], linestyle='--', label=r'$\eta$ = 0.250')
plt.plot(altitude, D[:,1,0], linestyle='--', label= r'$\eta$ = 0.325')
plt.plot(altitude, D[:,2,0], linestyle='--', label= r'$\eta$ = 0.400')
plt.plot(altitude, D[:,3,0], linestyle='-', label= r'$\eta$ = 0.291')



plt.axhline(y=D_design, linestyle='-', color='k', label='Max. Thrust Level for 1500W')
    
plt.xlim(150,300)
plt.ylim(0.01,0.025)

handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.title('Intake Efficiency Sensitivity')
plt.xlabel('Altitude [km]')
plt.ylabel('D [N]')

  


plt.show()
    
