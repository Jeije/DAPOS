# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:12:59 2019

@author: msjor
"""
import numpy as np
############################    Functions   ############################
#instead of import from power in src folder, as import doesn't work 
def panel_area(t_o, t_e, pr_day, pr_eclipse):
    #INPUTS
    wm = 200 #[W/m^2] not really needed as we are mainly concerned with solar radiation and panel efficiencies
    wkg = 100 #[W/kg]
    #t_o = 14095 #orbital period in [s]
    #t_e = 5920 #eclipse time [s]
    t_d = t_o - t_e #day time [s]
    sr = 1358 #solar radiation [W/m^2]
    theta = 0 #solar panel incidence angle [rad]
    T = 10 #mission lifetime [years]
    d = 0.9725 #yearly degradation
    eff = 0.28 #solar panel efficiency
    eff_c = 0.9 #battery charging efficiency
    eff_dc = 0.85 #battery discharging efficiency
    pr_day = pr_day/eff_c #power required during the day EOL [W]
    pr_eclipse = pr_eclipse/eff_dc #power required during eclipse EOL [W]
    
    #EQUATIONS
    pbol = ((pr_day*t_d+pr_eclipse*t_e)/(t_d)/(d**T))/np.cos(theta) #bol power accounting for degradation, eclipse time, incidence angle
    
    psol = pbol/eff #power that needs to be generated by solar panels accounting for their efficiency
    
    A = psol/sr #area
    m = pbol/wkg #mass
    
    #print('power =', psol, 'A=', A, 'm =', m)
    
    return A, m

def comms_mass(power_transmitter, area_antenna, dens_antenna):
   specific_power = 2.9 #W/kg
   dens_trans = 0.75*10**-3 #kg/m3
   mass_trans = power_transmitter/specific_power  #kg
   vol_trans = mass_trans/dens_trans  #m3
   mass_amp = 0.07*power_transmitter+0.634 #kg
   mass_antenna = dens_antenna * area_antenna #kg, antenna on board of spacecraft
   total_mass = (mass_antenna + mass_amp + mass_trans)*1.3

   return total_mass, vol_trans
#area to drag and power relations 
def A_to_Drag(A):
    #return density*(velocity**2)*(1.+np.pi/6.*np.sqrt(A/np.pi))*A
    return density*(velocity**2)*A*0.5*2.6

def panel_drag(A_p):
    #return 0.3*A_p*0.5*density*velocity**2
    return 0.05*A_p/length_intake/2*density*velocity**2

def area_panel_drag(D_p):
    return D_p*2/0.3/density/velocity**2

def massf_to_A(mf):
    return mf/intake_eff/density/velocity

def comms(h, freq, G_trans, D_reciever, Ts, R):
    dish_eff = 0.5
    rain = 4+3/13*(freq*10**(-9)-27)
    space = 147.55-20*np.log10(h*10**3)-20*np.log10(freq)
    G_rec = -159.59+20*np.log10(D_reciever)+20*np.log10(freq)+10*np.log10(dish_eff)
    line = 0.89
    G_trans = G_trans
    E_N = 10
    
    return 10**((E_N-line-G_trans-space-rain-G_rec-228.6+10*np.log10(Ts)+10*np.log10(R))/10)

def thrust_power(T):
    return (T+0.00069068)/0.0000156

################################    main     #############################
#body or not
body = True
#define orbit parameters 
t_o = 3600*1.5  #orbital period
t_e = t_o*0.177777   #eclipse period (0.17777 to 0.3222222)
h = 250   #orbital altitude #[km]
density = 1*10**-10  #[kg/m^3]
velocity = 7800 #[m/s]

#propulsion parameters
intake_eff = 0.40    #[-]
if body:
    area_correction = 1.2
else:
    area_correction = 1.1
T_over_D = 1.1
massf_req = 7/45.37 #[mg/s]
massf_req = massf_req/(10**6) #[kg/s]

#communication parameters 
freq = 36 #communication frequency [GHz]
freq = freq*10**9 #communications frequency [Hz]
G_trans = 5 #gain satellite antenna [dBi]
D_reciever = 1. #diameter reciever on ground [m]
Ts = 700 #system noise temperature [K]
datarate_imaging = 2632*10**6 #[bps]
compression_rat = 1/10  #[-]
data_orbit = datarate_imaging*(t_o-t_e)*compression_rat     #data produced during orbit [bits]
contact_time = 0.25*t_o       #[s]
R = data_orbit/contact_time    #data rate [bps]

#other input parameters
batt_dens = 250     #[Wh/kg]
aspect_ratio = 5    #[-]
coating_t = 100*10**-9  #[m]
coating_rho = 2800#[kg/m^3]
body_percent = 0.8 #[-] (percentage of the body that can be effectively used for solar panels)


#find power required for communication system 
P_comm = comms(h, freq, G_trans, D_reciever, Ts, R)

#power needed for other subsystems (from power budget)
P_camera = 10.

P_misc = 200.

#compute intake and frontal area based on the massflow requirement
intakeA = massf_to_A(massf_req)
frontalA = intakeA*area_correction
#compute drag (without solar panels)
drag_sat = A_to_Drag(frontalA)

#compute intial thrust and power needed for purely the satellite (no panels)
thrust = drag_sat*T_over_D
power_init = thrust_power(thrust)

#size solar panels for intial requirements
length_intake = np.sqrt(intakeA)*aspect_ratio
panel_body = length_intake*np.sqrt(frontalA/np.pi)*body_percent*2

power_day_i = power_init+P_comm+P_camera+P_misc
power_eclipse_i = power_init+P_comm+P_misc
panelA_i, panelM_i = panel_area(t_o, t_e, power_day_i, power_eclipse_i)

if panel_body>panelA_i:
    panel_body = panelA_i
    
#added drag due to the solar panels
if body:
    drag_panel = panel_drag(panelA_i-panel_body)
else:
    drag_panel = panel_drag(panelA_i)

panelA = panelA_i
power_thrust = power_init
#iterate to find total power requirement
while np.abs((drag_sat+drag_panel)*T_over_D-thrust)>0.0000000001:
    #set thrust to counteract new drag force
    thrust = T_over_D*(drag_sat+drag_panel)
    #compute power needed for new thrust force
    power_thrust = thrust_power(thrust)
    power_day = power_thrust+P_comm+P_camera+P_misc
    power_eclipse = power_thrust+P_comm+P_misc
    #size solar panels at new power
    panelA, panelM = panel_area(t_o, t_e, power_day, power_eclipse)
    #compute new drag
    if body:
        drag_panel = panel_drag(panelA-panel_body)
    else:
        drag_panel = panel_drag(panelA)

#print resulting design
print ("---------------------------------General performance---------------------------------")
print ("massflow required for engine operations [kg/s]:", massf_req)  
print ("Intake area [m^2] = ", intakeA)
print ("Total panel area [m^2]= ", panelA)
print ("Panel area on body [m^2] = ", panel_body*body)
print ("Panel area on arrays [m^2] = ", panelA-panel_body*body)
print ("Thrust, drag [N] and T/D", thrust, "|", drag_panel+drag_sat, "|", thrust/(drag_panel+drag_sat))
print (" ")
print ("---------------------------------Mass budget----------------------------------------")
print ("Panel mass [kg] = ", panelM)
print ("Battery mass [kg] = ", power_eclipse*t_e/3600/(batt_dens)*10/0.9)
print ("Power management system [kg]=", 0.33333*(panelM+ power_eclipse*t_e/3600/(batt_dens)*10/0.9))
print ("Power system total [kg] = ", (panelM+power_eclipse*t_e/3600/(batt_dens)*10/0.9)*1.333333)
coating_A = panelA*2+frontalA*2*aspect_ratio
print ("Additional mass due to coating [kg] = ", coating_A*coating_t*coating_rho)
print (" ")
print ("----------------------------------Power budget---------------------------------------")
print ("Power required to operate engine [W]= ", power_thrust)
print ("Power required for communications [W] =", P_comm)
print ("Power required for payload operations [W] =", P_camera)
print ("Total power required during operations [W] =", power_thrust+P_camera+P_comm+P_misc)
print ("Total power required during eclipse [W] =", power_thrust+P_comm+P_misc)
print (" ")
print ("----------------------------------Other---------------------------------------------")
print ("Intake length [m] = ", length_intake)
print ("Width of the solar panels [m] (GOCE style) =", panelA/np.sqrt(intakeA)/aspect_ratio/2)