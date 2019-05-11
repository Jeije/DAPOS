# -*- coding: utf-8 -*-
"""
Created on Thu May  9 09:23:36 2019

@author: Andrew.ia
"""
import numpy as np

###Constants

G_e   = 6.6725*10**(-11)                                                   #Nm^2/kg
miu_e = 3.986005*10**(14)                                                  #m^3/s^2
R_e   = 6378100.                                                            # m
w_e   = 7.3*10**(-5)



### inputs
#h  satellite altitude in m
r     = h+R_e
#C_D
#A  sat area
#m  mass
#th elevation


### outputs for circular obit

V_circ  = np.sqrt(miu_e/r)                                                 # m/s

V_esc   = np.sqrt(2.*miu_e/r)                                              # m/s
P       = 2.*np.pi*np.sqrt((r**3.)/miu_e)                                  # s
V_ang   = 2.*np.pi*/P                                                      # rad/s
csi     = -miu_e/(2.*r)                                                    #J  satellite energy
T_ecl   = (r/np.pi)*P                                                      # s max eclipse time
s_node  = 2.*np.pi*(P/1436.07)                                             # rad  long btw successive ascending/descending nodes




i_ss    = np.arccos(-0.098922*(1+ h/R_e)**(3.5))                           #inclination of ss orbit.Larger than 90 deg: retrograde
prec    = -2.06474 * 10. **14 *r**(-7./2.)*np.cos(i_ss)                    # rad/day node precession rate: rate of rotation in inertial space
r_day   = 1436.07/P                                                        # [-] revolutions per sidereal day
V_gt    = 2.*np.pi*R_e/P                                                   # m/s ground track velocity
DV_al   = (np.pi*(C_D)*A/m)*rho *r *V_circ/P                               #m/s per year. Mean DV to mainstain altitude
phi     = -th +np.arccos(R_e*np.cos(th)/(R_e+h))                           #semi angle over which it is visible by groundstation
w_ex    = np.sqrt(w_e**2. + V_ang**2. - 2.*w_e*V_ang*np.cos(i_ss))
tau     = 2.*phi/w_es