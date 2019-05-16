# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:12:59 2019

@author: msjor
"""
import numpy as np
from scipy.optimize import fsolve
############################    Functions   ############################

def elevationangle(longitude_ground, latitude_ground, longitude_sub, latitude_sub, elevation_min):

    
    ############     INPUTS      ###############
    
    
#    longitude_ground= [deg] Lt ground station (ESA Svalbard)
#    latitude_ground= [deg] delta_t ground station (ESA Svalbard)
#    
#    longitude_sub= [deg] Ls subsatellite point (groundtrack to centre of the earth) get data from orbit model 
#    latitude_sub= [deg] delta_s subsatellite point (groundtrack to centre of the earth) get data from orbit model 

    #INSTANTANEOUS POSITION OF S/C
    #FROM SMAD PAG 109-111
    
    R_E= 6378 #[km]
    rho_rad= np.arcsin(R_E/(R_E+h)) #[rad] angular radius of Earth 
    rho=np.rad2deg(rho_rad) #[deg]
    lambda_0=90-rho #[deg] angular radius measured at the centre of the earth of the region as seen from s/c
    lambda_0_rad= np.deg2rad(lambda_0) #[rad]
    D_max= R_E*np.tan(lambda_0_rad)#[km] distance to the horizon 
    Delta_L= np.abs(longitude_sub-longitude_ground)
    latitude_sub_rad=np.deg2rad(latitude_sub)
    latitude_ground_rad=np.deg2rad(latitude_ground)
    Delta_L_rad=np.deg2rad(Delta_L)
    lambda_Earth_rad= np.arccos(   np.sin(latitude_sub_rad)*np.sin(latitude_ground_rad)+np.cos(latitude_sub_rad)*np.cos(latitude_ground_rad)*np.cos(Delta_L_rad)   ) #[rad] earth centered angle, measured from subsatellite point to target        
    lambda_Earth=np.rad2deg(lambda_Earth_rad) #[deg]
    eta_rad= np.arctan(  np.sin(rho_rad)*np.sin(lambda_Earth_rad)/(1-np.sin(rho_rad)*np.cos(lambda_Earth_rad))   ) #[rad] angle from nadir
    eta= np.rad2deg(eta_rad)  #[deg] angle from nadir
    elevation= 90- eta -lambda_Earth   #[deg] elevation angle
    D=R_E*np.sin(lambda_Earth_rad)/np.sin(eta_rad) #[km]
    
    elevation_min_rad=np.deg2rad(elevation_min)
    
    #FROM NOW ON; ASSUMPTION OF CIRCULAR ORBIT
    
    etaMAX_rad= np.arcsin(  np.sin(rho_rad)*np.cos(elevation_min_rad)   ) #[rad] angle from nadir
    etaMAX= np.rad2deg(etaMAX_rad)  #[deg] angle from nadir
    lambdaMAX= 90-etaMAX-elevation_min
    elevation_max= 180-elevation_min
    lambdaMIN=7 #[deg]   #assumption (can be calculated using the inclination and ascending node of the S/C from SMAD p 116)
    lambdaMIN_rad=np.deg2rad(lambdaMIN)
    lambdaMAX_rad=np.deg2rad(lambdaMAX)
    contact_time =(t_o/180)*np.rad2deg(np.arccos(np.cos(lambdaMAX)/np.cos(lambdaMIN))) #[s]
    
    return elevation, contact_time





def comms_mass(power_transmitter, area_antenna, dens_antenna):
    specific_power = 2.9 #W/kg
    dens_trans = 0.75*(10**-3) #kg/m3
    mass_trans = power_transmitter/specific_power  #kg
    vol_trans = mass_trans/dens_trans  #m3
    mass_amp = 0.07*power_transmitter+0.634 #kg
    mass_antenna = dens_antenna * area_antenna #kg, antenna on board of spacecraft
    total_mass = (mass_antenna + mass_amp + mass_trans)*1.3
    return total_mass, vol_trans


def comms(h, freq, G_trans, D_receiver, Ts, R):
    
    #[103] A New Approach for Enhanced Communication to LEO Satellites
    E_opt= 45.-0.00446*h #[deg]     optimal elevation angle for communications
    
    dish_eff = 0.55   
    rain = 2 #dB from table page 534 smad using optimal elevation angle and iterative estimation of the power
    space = 147.55-20.*np.log10(h*10.**3.)-20.*np.log10(freq)
    G_rec = -159.59+20.*np.log10(D_receiver)+20.*np.log10(freq)+10.*np.log10(dish_eff)
    line = 0.89
    G_trans = G_trans
    E_N = 7
    #E_N = P_trans*L_line*G_trans*Ls*La*G_reciever/k/Ts/R#energy per bit to noise density
    
    #La= transmission path loss
    #Ls= space loss
    #Ts= system noise temperature
    #R= data rate
    
    P= 10.**((E_N-line-G_trans-space-rain-G_rec-228.6+10.*np.log10(Ts)+10.*np.log10(R))/10.)
    
    
    
    return P, E_opt







#ESA SVALBARD https://www.esa.int/Our_Activities/Navigation/Galileo/Galileo_IOV_ground_stations_Svalbard
#SvalSat and KSAT's Troll Satellite Station (TrollSat) in Antarctica are the only ground stations that can see a low altitude polar orbiting satellite 
#(e.g., in sun-synchronous orbit) on every revolution as the earth rotates.
longitude_ground= 15.399 #[deg] Lt ground station (ESA Svalbard)
latitude_ground= 78.228 #[deg] delta_t ground station (ESA Svalbard)
longitude_sub= 185 #20 #[deg] Ls subsatellite point (groundtrack to centre of the earth) get INSTANTANEOUS data from orbit model 
latitude_sub= 10#90 #[deg] delta_s subsatellite point (groundtrack to centre of the earth) get INSTANTANEOUS data from orbit model 
elevation_min=5 #[deg] minimum elevation angle above the horizon to make contact with ground

elevation, contact_time= elevationangle(longitude_ground, latitude_ground, longitude_sub, latitude_sub, elevation_min)


#define orbit parameters 
t_o = (87.49+37.8)*60.  #[s] orbital period
t_e = 37.8*60.   #eclipse period
h = 250.   #orbital altitude #[km]
density = 3.64*(10**-10.)  #[kg/m^3]
velocity = 7787. #[m/s]

#communication parameters 
freq = 8. #communication frequency [GHz] X band, typical data rate 150 Mbit/s
freq = freq*10.**9. #communications frequency [Hz]
G_trans = 15. #gain satellite antenna [dBi]
D_receiver = 1.5 #diameter reciever on ground [m]
Ts = 600. #system noise temperature [K]
datarate_imaging = 2632.*10.**6. #[bps]
compression_rat = 3./5.   #[-]
data_orbit = datarate_imaging*(t_o-t_e)*compression_rat     #data produced during orbit [bits]
#contact_time = 0.010*t_o       #[s]   #this has to be substituted with the 
R = data_orbit/contact_time    #data rate [bps]



#find power required for communication system 
P_comm, E_opt = comms(h, freq, G_trans, D_receiver, Ts, R)





power_transmitter=P_comm  #[W]
area_antenna=(0.3**2)*np.pi  #from ref [101] conservative estimation
dens_antenna=8.                  #from ADSEE reader
total_mass, vol_trans = comms_mass(power_transmitter, area_antenna, dens_antenna)  #estimations from adsee reader




print('Data rate Gbs', R/10**9, 'Power required for communications [W]', P_comm)