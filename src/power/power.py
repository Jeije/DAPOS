import numpy as np

def panel_area(t_o, t_e, pr_day, pr_eclipse):
    #INPUTS
    wm = 200 #[W/m^2] not really needed as we are mainly concerned with solar radiation and panel efficiencies
    wkg = 1000 #[W/kg]
    #t_o = 14095 #orbital period in [s]
    #t_e = 5920 #eclipse time [s]
    t_d = t_o - t_e #day time [s]
    sr = 1400 #solar radiation [W/m^2]
    theta = 0 #solar panel incidence angle [rad]
    T = 10 #mission lifetime [years]
    d = 0.99 #yearly degradation
    eff = 0.09 #solar panel efficiency
    eff_c = 0.99 #battery charging efficiency
    eff_dc = 0.99 #battery discharging efficiency
    #pr_day = 500 #power required during the day EOL [W]
    pr_eclipse = pre_eclipse/eff_c/eff_dc #power required during eclipse EOL [W]
    
    #EQUATIONS
    pbol = ((pr_day*t_d+pr_eclipse*t_e)/(t_d)/(d**T))/np.cos(theta) #bol power accounting for degradation, eclipse time, incidence angle
    
    psol = pbol/eff #power that needs to be generated by solar panels accounting for their efficiency
    
    A = psol/sr #area
    m = psol/wkg #mass
    
    #print('power =', psol, 'A=', A, 'm =', m)
    
    return A, m
    