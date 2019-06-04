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
from solarpanels import *

set_parameter = 1 + 2 # 1=collection_eff, 2=isp, 3=CD

n = 1;
k = 150

#density = [5*10**(-5),5*10**(-6) ,5*10**(-7) , 1*10**(-8), 5*10**(-9),2.148*10**(-9), 1*10**(-9), 5*10**(-10), 3*10**(-10), 1*10**(-10), 8*10**(-11),5*10**(-11)]   #[kg/m^3]
altitude = 200000 #m

Earth_R = 6371000 #m
R = Earth_R + altitude
G = 6.674*10**(-11) #m^3/kgs^2
Earth_M = 5.972*10**24 #kg

#INPUTS
t_o     = sqrt((4*(pi**2)*R**3)/(G*Earth_M))
t_e     = (2*t_o*np.arcsin(Earth_R/R))/(2*pi)
pr_eclipse  = 1500
theta       = pi/8
sr          = 1358
T           = 10
eff         = 0.25
eff_c       = 0.92
eff_dc      = 0.92
pr_extra_day= 40
wkg         = 150
d           = 0.97

thetas       = [0, pi/8, pi/4]
Ts           = [5, 10, 15]
effs         = [0.20, 0.25, 0.30]
eff_cs       = [0.85, 0.92, 0.99]
eff_dcs      = [0.85, 0.92, 0.99]
pr_extra_days= [0, 40, 80]
wkgs         = [100, 150, 200]
ds           = [0.95, 0.97, 0.99]

panelA = np.zeros(27)
panelM = np.zeros(27)

panelA[0] = panel_area(t_o, t_e, pr_eclipse,thetas[0], T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]      
panelA[1] = panel_area(t_o, t_e, pr_eclipse,thetas[1], T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[2] = panel_area(t_o, t_e, pr_eclipse,thetas[2], T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelM[0] = panel_area(t_o, t_e, pr_eclipse,thetas[0], T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[1] = panel_area(t_o, t_e, pr_eclipse,thetas[1], T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[2] = panel_area(t_o, t_e, pr_eclipse,thetas[2], T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]

panelA[3] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[4] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[5] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelM[3] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[4] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[5] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]

panelA[6] = panel_area(t_o, t_e, pr_eclipse,theta, Ts[0], eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[7] = panel_area(t_o, t_e, pr_eclipse,theta, Ts[1], eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[8] = panel_area(t_o, t_e, pr_eclipse,theta, Ts[2], eff, eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelM[6] = panel_area(t_o, t_e, pr_eclipse,theta, Ts[0], eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[7] = panel_area(t_o, t_e, pr_eclipse,theta, Ts[1], eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[8] = panel_area(t_o, t_e, pr_eclipse,theta, Ts[2], eff, eff_c, eff_dc, pr_extra_day, wkg, d)[1]

panelA[9]  = panel_area(t_o, t_e, pr_eclipse,theta, T, effs[0], eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[10] = panel_area(t_o, t_e, pr_eclipse,theta, T, effs[1], eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelA[11] = panel_area(t_o, t_e, pr_eclipse,theta, T, effs[2], eff_c, eff_dc, pr_extra_day, wkg, d)[0]
panelM[9]  = panel_area(t_o, t_e, pr_eclipse,theta, T, effs[0], eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[10] = panel_area(t_o, t_e, pr_eclipse,theta, T, effs[1], eff_c, eff_dc, pr_extra_day, wkg, d)[1]
panelM[11] = panel_area(t_o, t_e, pr_eclipse,theta, T, effs[2], eff_c, eff_dc, pr_extra_day, wkg, d)[1]

panelA[12] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_cs[0], eff_dc, pr_extra_day, wkg, d)[0]
panelA[13] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_cs[1], eff_dc, pr_extra_day, wkg, d)[0]
panelA[14] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_cs[2], eff_dc, pr_extra_day, wkg, d)[0]
panelM[12] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_cs[0], eff_dc, pr_extra_day, wkg, d)[1]
panelM[13] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_cs[1], eff_dc, pr_extra_day, wkg, d)[1]
panelM[14] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_cs[2], eff_dc, pr_extra_day, wkg, d)[1]

panelA[15] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dcs[0], pr_extra_day, wkg, d)[0]
panelA[16] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dcs[1], pr_extra_day, wkg, d)[0]
panelA[17] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dcs[2], pr_extra_day, wkg, d)[0]
panelM[15] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dcs[0], pr_extra_day, wkg, d)[1]
panelM[16] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dcs[1], pr_extra_day, wkg, d)[1]
panelM[17] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dcs[2], pr_extra_day, wkg, d)[1]

panelA[18] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_days[0], wkg, d)[0]
panelA[19] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_days[1], wkg, d)[0]
panelA[20] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_days[2], wkg, d)[0]
panelM[18] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_days[0], wkg, d)[1]
panelM[19] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_days[1], wkg, d)[1]
panelM[20] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_days[2], wkg, d)[1]

panelA[21] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkgs[0], d)[0]
panelA[22] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkgs[1], d)[0]
panelA[23] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkgs[2], d)[0]
panelM[21] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkgs[0], d)[1]
panelM[22] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkgs[1], d)[1]
panelM[23] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkgs[2], d)[1]

panelA[24] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, ds[0])[0]
panelA[25] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, ds[1])[0]
panelA[26] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, ds[2])[0]
panelM[24] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, ds[0])[1]
panelM[25] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, ds[1])[1]
panelM[26] = panel_area(t_o, t_e, pr_eclipse,theta, T, eff, eff_c, eff_dc, pr_extra_day, wkg, ds[2])[1]

#panelM[:] = panelM[:] - panelM[4]
#panelA[:] = panelA[:] - panelA[4]

#plt.plot(altitude, D[:,0,0], linestyle='--', label='Min. CDA for min. density')
plt.scatter(panelM[0],panelA[0], c='k', marker='|', label=r'$\theta$ = $0$ rad')
plt.scatter(panelM[1],panelA[1], c='k', marker='o', label=r'$\theta$ = $pi/8$ rad')
plt.scatter(panelM[2],panelA[2], c='k', marker='+', label=r'$\theta$ = $pi/4$ rad')

plt.scatter(panelM[6],panelA[6], c='y', marker='|', label=r'T = 5 years')
plt.scatter(panelM[7],panelA[7], c='y', marker='o', label=r'T = 10 years')
plt.scatter(panelM[8],panelA[8], c='y', marker='+', label=r'T = 15 years')

plt.scatter(panelM[9],panelA[9], c='c', marker='|', label=r'$\eta_{solar}$ = 0.20')
plt.scatter(panelM[10],panelA[10], c='c', marker='o', label=r'$\eta_{solar}$ = 0.25')
plt.scatter(panelM[11],panelA[11], c='c', marker='+', label=r'$\eta_{solar}$ = 0.30')

plt.scatter(panelM[12],panelA[12], c='lime', marker='|', label=r'$\eta_{charging}$ = 0.85')
plt.scatter(panelM[13],panelA[13], c='lime', marker='o', label=r'$\eta_{charging}$ = 0.92')
plt.scatter(panelM[14],panelA[14], c='lime', marker='+', label=r'$\eta_{charging}$ = 0.99')

plt.scatter(panelM[15],panelA[15], c='r', marker='|', label=r'$\eta_{discharging}$ = 0.85')
plt.scatter(panelM[16],panelA[16], c='r', marker='o', label=r'$\eta_{discharging}$ = 0.92')
plt.scatter(panelM[17],panelA[17], c='r', marker='+', label=r'$\eta_{discharging}$ = 0.99')

plt.scatter(panelM[18],panelA[18], c='g', marker='|', label=r'extra power daytime = 0 W')
plt.scatter(panelM[19],panelA[19], c='g', marker='o', label=r'extra power daytime = 40 W')
plt.scatter(panelM[20],panelA[20], c='g', marker='+', label=r'extra power daytime = 80 W')

plt.scatter(panelM[21],panelA[21], c='darkorange', marker='|', label=r'$Power Density$ = 100 W/kg')
plt.scatter(panelM[22],panelA[22], c='darkorange', marker='o', label=r'$Power Density$ = 150 W/kg')
plt.scatter(panelM[23],panelA[23], c='darkorange', marker='+', label=r'$Power Density$ = 200 W/kg')

plt.scatter(panelM[24],panelA[24], c='darkgrey', marker='|', label=r'degradation = 0.95')
plt.scatter(panelM[25],panelA[25], c='darkgrey', marker='o', label=r'degradation = 0.97')
plt.scatter(panelM[26],panelA[26], c='darkgrey', marker='+', label=r'degradation = 0.99')

plt.scatter(panelM[4], panelA[4], c='r', marker='o')
#plt.plot(altitude, D[:,3,0], linestyle='-', label= r'$\eta$ = 0.291')
#
#plt.xscale('log')
#plt.yscale('log')
#
#plt.axhline(y=D_design, linestyle='-', color='k', label='Max. Thrust Level for 1500W')
#    
#plt.xlim(150,300)
#plt.ylim(0.01,0.025)

#handles, labels = plt.gca().get_legend_handles_labels()
#by_label = OrderedDict(zip(labels, handles))
#plt.legend(by_label.values(), by_label.keys())
plt.legend(loc='upper center', bbox_to_anchor=(1.45, 1.03), shadow=True, ncol=2)

plt.title('Sensitivity Regarding Solar Panel Weight & Power')
plt.xlabel('Total Weight Power System [kg]')
plt.ylabel('Solar Panel Area [m^2]')

  


plt.show()
    
