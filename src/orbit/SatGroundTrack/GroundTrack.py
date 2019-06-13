'''Importing Required Modules'''
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
from astropy import units as u

'''This code was provided by Group 08 Supervisor Mark Rovira'''
''' Thanks Mark!'''

'''Class GroundTackCalc'''
'''Calculates Satellite Ground Track and other relevant parameters for a 'frozen orbit' '''
'''
* INPUT 1: Discretization Step per Orbit (keep above 300)
* INPUT 2: Inclination Angle of Orbit 
* INPUT 3: Orbital Altitude 
* INPUT 4: Initial Lattitude of Satellite
* INPUT 5: Initial Longitude
* INPUT 6: Amount of Orbits to be Computed
If n = 0, it will determine the revolutions within one day

* PARAM 1: plot, set True if orbit ground track plot is required

* OUTPUT 1: Dataframe structure containing the calculated orbit data in columns:
['time [s]','Lat [deg]','Lon [deg]','V_rel [m/s]','V [rad/s]','Azimuth [deg]'] 
for each discretization step along the requested orbit
'''

class GroundTrackCalc(object):
    def __init__(self, dt:int=1000, inc:float= 94.3*u.deg, h:float= 200*u.km, lat0:float= 12.77*u.deg,
                 longi0:float= -91.397*u.deg, n:int= 1, plot = False):
        '''Set Gravitational Constants'''
        T_day = 86164.1004
        mu_E = 5.972e24*6.67430e-11
        DA = -1

        '''Convert Inputs to Proper Values'''
        inc = inc.to(u.deg).value
        h = h.to(u.meter).value
        lat0 = lat0.to(u.deg).value
        longi0 = longi0.to(u.deg).value

        '''Calculate Satellite Parameters'''
        T_sat = 2 * np.pi * np.sqrt((6371000+h) ** 3 / mu_E)

        w1 = -2 * np.pi / T_day
        w2 = 2 * np.pi / T_sat

        a_sat = (mu_E / w2 ** 2) ** (1 / 3)

        rho1 = inc
        rho2 = 90

        '''Determines Orbits in one Day'''
        if n == 0:
            n = 86164.1004/T_sat

        if longi0 < 0:
            phi10, phi20 = self.initial_values(rho1, 360 + lat0, longi0, DA)
        else:
            phi10, phi20 = self.initial_values(rho1, lat0, longi0, DA)

        self.t = np.linspace(0, n * T_sat, int(n * dt))
        self.latP = np.zeros(len(self.t))
        self.alpha = np.zeros(len(self.t))
        self.V_rel = np.zeros(len(self.t))
        self.V_azimuth = np.zeros(len(self.t))
        self.azimuth = np.zeros(len(self.t))

        for idx, i in enumerate(self.t):
            latP_val, alpha_val, V_val, azimuth_val = self.ground_track(w1, w2, rho1, rho2, phi10, phi20, i)
            if alpha_val > 180:
                alpha_val = alpha_val - 360
            self.latP[idx] = latP_val
            self.alpha[idx] = alpha_val
            self.V_azimuth[idx] = V_val
            self.V_rel[idx] = V_val*a_sat
            self.azimuth[idx] = azimuth_val

        if plot == True:
            self.PlotGroundTrack()

    def return_data(self):
        self.__df = pd.DataFrame(np.stack((self.t,self.latP,self.alpha,self.V_rel,self.V_azimuth,self.azimuth), axis=1))
        self.__df.columns = ['time [s]','Lat [deg]','Lon [deg]','V_rel [m/s]','V [rad/s]','Azimuth [deg]']
        return self.__df

    def hemisphere_function(self,angle):
        if angle>=0 and angle <= np.pi:
            H=1
        elif angle > np.pi and angle <=2*np.pi:
            H=-1
        else:
            raise ValueError
        return H

    def acos2(self,cosine,H):
        if H == 1:
            if cosine>1:
                angle=0
            elif cosine<-1:
                angle=np.pi
            else:
                angle=np.arccos(cosine)
        elif H ==-1:
            if cosine>1:
                angle=0
            elif cosine<-1:
                angle=np.pi
            else:
                angle=2*np.pi-np.arccos(cosine)
        else:
            raise ValueError
        return angle

    def zero_2pi(self,angle0):
        angle=np.arctan2(np.sin(angle0),np.cos(angle0))
        if angle<0:
            angle=2*np.pi+angle
        return angle

    def initial_values(self,rho1,lat,longi,DA):
        deg_rad = np.pi/180
        rho1 = rho1*deg_rad
        lat = lat*deg_rad
        longi = longi*deg_rad
        colat = np.pi/2-lat

        phi2 = self.acos2((np.cos(colat))/(np.sin(rho1)),DA)
        phi1 = self.acos2((-np.cos(colat)*np.cos(rho1))/(np.sin(colat)*np.sin(rho1)),self.hemisphere_function(phi2))
        phi1=longi+phi1

        phi10 = phi1/deg_rad
        phi20 = phi2/deg_rad
        return phi10,phi20

    def ground_track(self,w1,w2,rho1,rho2,phi10,phi20,t):
        deg_rad = np.pi/180
        rho1 = deg_rad*rho1
        rho2 = deg_rad*rho2
        phi1 = deg_rad*phi10+w1*t
        phi2 = deg_rad*phi20+w2*t
        phi1 = self.zero_2pi(phi1)
        phi2 = self.zero_2pi(phi2)

        colatP = np.arccos(np.cos(rho1)*np.cos(rho2)+np.sin(rho1)*np.sin(rho2)*np.cos(phi2))
        latP = np.pi/2-colatP
        delta_alpha = self.acos2((np.cos(rho2)-np.cos(rho1)*np.sin(latP))/(np.sin(rho1)*np.cos(latP)),
                                 -self.hemisphere_function(phi2))
        alpha = phi1+delta_alpha

        colatE = np.arctan(w2*np.sin(rho1)/(w1+w2*np.cos(rho1)))
        if colatE<0:
            colatE=colatE+np.pi

        wE = np.sqrt(w1**2+w2**2+2*w1*w2*np.cos(rho1))
        rhoE = np.arccos(np.cos(colatP)*np.cos(colatE)+np.sin(colatP)*np.sin(colatE)*np.cos(delta_alpha))
        delta_azimuth = self.acos2((np.cos(colatE)-np.cos(rhoE)*np.sin(latP))/(np.sin(rhoE)*np.cos(latP)),
                                   self.hemisphere_function(delta_alpha))
        azimuth = delta_azimuth-np.pi/2
        V = wE*np.sin(rhoE)

        latP = latP/deg_rad
        alpha=self.zero_2pi(alpha)/deg_rad
        azimuth = self.zero_2pi(azimuth)/deg_rad
        return latP,alpha,V,azimuth

    def PlotGroundTrack(self):
        fig, ax = plt.subplots()
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        ax.plot(self.alpha, self.latP, 'b', transform=ccrs.Geodetic(), label='ITRS')
        ax.plot()


if __name__ == "__main__":
    '''Testing Program Against Reference Values'''
    '''Setting Constants of Test'''
    rho1 = 40
    rho2 = 20
    phi1 = 5
    phi2 = 90
    w1 = 1
    w2 = 3
    '''Answer: 56.08, 37.05, 1.132, 334.66'''
    a = GroundTrackCalc(plot=False).ground_track(w1,w2,rho1,rho2,phi1,phi2,0)

    b = GroundTrackCalc(n=1,plot=True)
    c = b.return_data()