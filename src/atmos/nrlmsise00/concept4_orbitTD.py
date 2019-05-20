# -*- coding: utf-8 -*-
"""
Created on Fri May 10 10:59:13 2019

author: Joey
"""

import numpy as np
import matplotlib.pyplot as plt

from nrlmsise_00_dens import nlrmsise00_dens

## INPUT DATA -----------------------------------------------------------------
# orbit data
lower_limit     = 160       # km (heating and molecular flow reasons)
upper_limit     = 400       # km (no air and debris considerations)

# Earth data
R_e             = 6370      # km, Earth's radius
g_0             = 0.00981   # km/s^2, Earth's surface gravity
mu              = 398600.44 # km^3/s^2, Earth's gravitational constant

# engine and vehicle data
m_tot           = 100       # kg, spacecraft total mass
#power_vs_thrust = 64        # W/mN
P_max           = 500       # W, maximum power

Isp             = 3.5*1e3   # s, Isp
X_d             = 0.75      # -, fraction of particles for drag, between 0.5-0.75 for entire s/c

eta             = 0.35      # -, collection efficiency
A_in            = 0.65      # m^2, intake area
A_f             = 1.0       # m^2, frontal area
C_D             = 2.6       # -, drag coefficient

# simulation data
N               = 720       # -, number of points per orbit



## CALCULATED DATA ------------------------------------------------------------

print()
print("Altitude range from",lower_limit,"km to",upper_limit,"km")

fig, ax = plt.subplots(1, 2)
fig.suptitle("Performance graphs for altitudes from {} km to {} km".format(lower_limit, upper_limit))

# orbit parameters
theta  = np.linspace(0, 2*np.pi, N)              # rad, orbit angle
a      = (lower_limit + upper_limit + 2 * R_e)/2 # km, semi-major axis
r_a    = upper_limit + R_e                       # km, appocentre radius
r_p    = lower_limit + R_e                       # km, pericentre radius
e      = r_a/a - 1                               # -, eccentricity
r      = a * (1 - e*e) / (1 + e * np.cos(theta)) # km, orbit radius
h      = r - R_e                                 # km, orbit height
V_orb  = np.sqrt( mu * ( (2/r) - (1/a) ) )       # km/s, orbital velocity
T_orb  = 2 * np.pi * np.sqrt(a**3 / mu)          # s, orbital period

# engine and vehicle parameters
B      = m_tot/(C_D*A_f)                         # kg/m^2, ballistic coefficient
m_d_r  = 1.54*1e-07                              # kg/s, minimum mass flow (Martijn)

print("Ballistic coefficient = {} kg/m^2".format(B))
print()

for P_max in np.linspace(300, 1200, 19):

    print("Power = {} W".format(round(P_max, 1)))

    T_max  = P_max*0.0000156 - 0.00069068            # N, maximum thrust

    print("Maximum thrust produced = {} mN".format(round(T_max*1000, 1)))

    # atmospheric data
    alts   = np.linspace(lower_limit, upper_limit, int(N/2))
    rho_oneside = np.array([nlrmsise00_dens(alt) for alt in alts])
    rho    = np.hstack((rho_oneside, rho_oneside[::-1]))

    m_dot  = rho * A_in * V_orb*1000                 # kg/s, mass flow

    # thrust and drag
    T      = np.ones(N) * T_max
    D      = C_D * 0.5 * rho * (V_orb*V_orb*1e6) * A_f # N, drag
    TD_new = T/D

    # power
    Power  = (T + 0.00069068) / 0.0000156 # W, required engine power


    # decay estimations (altitude loss and delta V per orbit)
    Per = T_orb / (3600 * 24 * 365) # yr, orbital period
    decay_rate = -2*np.pi * (1/B) * rho * (r*r*1e6) / Per # m/yr, orbital decay rate
    decay_rate_s = decay_rate / (3600 * 24 * 365) # m/s, orbital decay rate

    n = 2 * np.pi / T_orb # s^-1, mean motion
    delta_T_tot = (theta/n)[np.where( T < D )] # s, time spend where T < D
    delta_T = np.hstack( (np.diff(delta_T_tot[np.where(delta_T_tot < T_orb/2)]),
                          np.diff(delta_T_tot[np.where(delta_T_tot > T_orb/2)]) ) )

    loss_part = np.where(np.logical_or(delta_T_tot < T_orb/2, delta_T_tot > T_orb/2))
    decay = sum( decay_rate_s[loss_part][1:-1] * delta_T ) # m, total decay (simple 'integration')


    delta_V_req = np.pi * (1/B) * rho * (r * V_orb * 1e6) / Per # m/s/yr, required delta V for orbit keeping
    delta_V_mss = delta_V_req / (3600 * 24 * 365)               # m/s/s, required delta V for orbit keeping
    delta_V_tot = sum( delta_V_mss[loss_part][1:-1] * delta_T ) # m/s, total delta V


    # possible delta V accounting for drag and minimum mass flow
    index       = np.where( T > D )
    t_TD1       = (theta/n)[index]            # s, time where T > D
    prod_del_V  = 0                           # m/s, total delta V produced
    h_min       = 0
    h_max       = 0

    T = np.where(rho > m_d_r / ( A_in * V_orb * 1000), T, 0)
    #print(T)
    #print(orbit(lower_limit, upper_limit, B, rho, T, D, True))

    for i in range(len(t_TD1)-1):
        rho_req  = m_d_r / ( A_in * V_orb[index][i]*1000)
        rho_real = rho[index][i]

        if rho_real >= rho_req:
            # YES WE CAN (THRUST)!
            Drag = D[index][i]
            F_r  = T_max - Drag
            prod_del_V += F_r * (t_TD1[i+1] - t_TD1[i])

            h_thrust = h[index][i]
            if h_min == 0:
                h_min = h_thrust
            elif h_max < h_thrust:
                h_max = h_thrust


    # required thrust time assuming constant maximum thrust
    #t_req     = m_tot * delta_V_tot / T_max   # s, thrust time required
    #t_TD1     = (theta/n)[np.where( T > D )]  # s, time where T > D
    #t_TD1_tot = max(t_TD1) - min(t_TD1)       # s, total time spent with T > D

    print("Maximum altitude with T < D = {} km".format(round(max(h[np.where(T < D)]), 1)))
    print("Estimated altitude decay = {} km".format(round(decay/1000, 3)))
    print("Estimated total delta V required = {} m/s".format(round(delta_V_tot, 2)))
    print("Estimated total producable delta V = {} m/s".format(round(prod_del_V, 2)))
    print("Altitude range in with losses are compensated = {} km to {} km".format(round(h_min, 1), round(h_max, 1)))
    #print("Estimated thrust time required at max thrust = {} s".format(round(t_req, 1)))
    #print("Estimated time with T > D = {} s".format(round(t_TD1_tot, 1)))
    print()


## PLOTTING -------------------------------------------------------------------
    ax[0].plot(h, TD_new, label="P = {} W".format(round(P_max, 1)))

    ax[1].plot(h, T)



ax[0].set(xlabel="orbit altitude [km]", ylabel="T/D-ratio [-]", ylim=[-0.1, 1.1],
          xlim=[lower_limit, 300], title="T/D-ratios")

ax[1].plot(h, D, color="black", label="Drag")
ax[1].set(xlabel="orbit altitude [km]", ylabel="Force [N]", ylim=[-0.001, 0.03],
          title="Drag and maximum thrust")

fig.legend()

plt.show()




# thrust and drag (old)
#TD = Isp * g_0 / (V_orb * X_d) # -, thrust over drag ratio JPL paper
#T_no_lim = eta * m_dot * g_0*1000 * Isp # N, thrust without power maximum
#T = np.array([min([T_i, T_max]) for T_i in T_no_lim])

#D_2 = rho * (V_orb*V_orb*1e6) * A_f * C_D * 0.5 # (1 + (np.pi/6 * np.sqrt(A_f/np.pi)))
#D = np.hstack((D[np.where(h<120)],D[np.where(h>120)] /1.1))




# =============================================================================
# ## orbital decay from SMAD
# P = T_orb / (3600 * 24 * 365) # yr, orbital period
# decay_rate = -2*np.pi * B * rho * r*r / P # km/yr, orbital decay rate
# decay_rate_s = decay_rate / (3600 * 24 * 365) * 1000 # m/s, orbital decay rate
#
# n = 2 * np.pi / T_orb # s^-1, mean motion
# delta_T_tot = (theta/n)[np.where( T < D_2 )]
# delta_T = np.hstack( (np.diff(delta_T_tot[np.where(delta_T_tot < T_orb/2)]),
#                       np.diff(delta_T_tot[np.where(delta_T_tot > T_orb/2)]) ) )
#
# loss_part = np.where(np.logical_or(delta_T_tot < T_orb/2, delta_T_tot > T_orb/2))
# decay = sum( decay_rate_s[loss_part][1:-1] * delta_T )
#
# print("Ballistic coefficient =",B,"kg/m^2")
# print("Total estimated altitude loss =",decay,"m")
#
#
# fig1, ax1 = plt.subplots(1, 1)
# fig1.suptitle("Orbital decay rate per altitude from {} km to {} km".format(min(h), max(h)))
# ax1.plot(h, decay_rate_s)
# ax1.set(xlabel="orbit altitude [km]", ylabel="decay rate [m/s]")
# plt.show()
#
#
#
#
#
# ## Energy loss per orbit
# loss_index = np.where(D_2 - T > 0)
# print("Maximum altitude with T < D =",max(h[loss_index]))
# =============================================================================


# # estimate loss by work done from resulting force
# F_res = (D_2 - T)[loss_index] # only interested in decay
# r_res = r[loss_index] # orbital radius with D > T
# theta_res = np.arccos( (a * (1 - e*e) / r_res - 1 ) / e ) # angles with D > T
# s = theta_res * r_res # km, total arc length
#
# energy_loss = np.sum(F_res[:-1] * np.diff(s)) # kJ, energy loss it's sort of a numerical integration so use the change in arclength
# print("energy loss =",energy_loss)
#
# # calculate total energy you had, maybe use one side of vis-visa equation?
# V_orb_res = V_orb[loss_index[0][0] - 1]
# r_res = r[loss_index[0][0] - 1]
#
# E_kin = 0.5 * (V_orb_res * V_orb_res) # kJ
# E_pot = mu/r_res # kJ
# E_tot = E_kin - E_pot # kJ
# print("new total energy =",E_tot)
#
# # calculate new total energy
# E_tot_new = E_tot - energy_loss
#
# # calculate new velocity (in pericentre? or at end of loss?)
# # calculate new semi-major axis and appocentre
# a_new = 1/(-2*E_tot_new/mu)
# print("new semi-major axis =",a_new)
# print("old semi-major axis =",a)

# boom! done?
