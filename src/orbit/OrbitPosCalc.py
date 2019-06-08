'''Python Script for Plotting Satellite Groundtrack'''
#Import Numpy and Pandas Modules for Data Processing
import numpy as np
import pandas as pd

# Poliastro modules
from poliastro.twobody import Orbit
from poliastro.bodies import Earth

# Astropy modules
from astropy import coordinates as coord
from astropy import units as u

# Plotting modules
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from poliastro.plotting import *

class OrbitGroundTrack(object):
    def __init__(self, dt:int=1000, orbvec:np.array=np.array([6621000.1,0.0,94.3,180,0,0]), plot = False, coordinate = 'spherical'):

        re = 6.3781e3

        #Setting Classical Orbital Parameters
        self.__a = orbvec[0]*u.meter
        self.__ecc = orbvec[1]*u.one
        self.__inc = orbvec[2] * u.deg
        self.__raan = orbvec[3]*u.deg
        self.__argp = orbvec[4]*u.deg
        self.__nu = 0*u.deg

        #Generate Satellite Orbit
        self.__ss = Orbit.from_classical(Earth, self.__a, self.__ecc, self.__inc, self.__raan, self.__argp, self.__nu)

        # Transform GCRS to ITRS
        self.__ss_gcrs = self.__ss.sample(dt)
        self.__ss_itrs = self.__ss_gcrs.transform_to(coord.ITRS(obstime=self.__ss_gcrs.obstime))

        # Convert to lat and lon
        self.__latlon_itrs = self.__ss_itrs.represent_as(coord.SphericalRepresentation)

        self.__vals = np.zeros([dt,4])

        self.timedata()

        if coordinate == 'spherical':
            self.sphericalpos(dt,re)
            self.__df = pd.DataFrame(self.__vals,columns=['Time [s]','Lat [deg]','Lon [deg]','Height [km]'])

        if coordinate == 'cartesian':
            self.cartesianpos(dt)
            self.__df = pd.DataFrame(self.__vals,columns=['Time [s]','X [m]','Y [m]','Z [m]'])

        if plot == True:
            self.GroundPlot()
            #self.OrbitPlot()

    def return_orbit(self):
        return self.__ss

    def return_df(self):
        return self.__df

    def sphericalpos(self, dt,re):
        for idx in range(dt):
            self.__vals[idx][1] = self.__latlon_itrs.lat.to(u.deg).value[idx]
            self.__vals[idx][2] = self.__latlon_itrs.lon.to(u.deg).value[idx]
            self.__vals[idx][3] =self.__latlon_itrs.distance.value[idx] - re

    def cartesianpos(self,dt):
        for idx in range(dt):
            self.__vals[idx][1] = self.__ss_itrs.data._values[idx][0]
            self.__vals[idx][2] = self.__ss_itrs.data._values[idx][1]
            self.__vals[idx][3] = self.__ss_itrs.data._values[idx][2]
        return np.array(self.__ss_itrs._data._values)

    def timedata(self):
        t0 = self.__ss_itrs.obstime.datetime[0]
        for idx,t in enumerate(self.__ss_itrs.obstime.datetime):
            self.__vals[idx][0] = (t-t0).total_seconds()

    def GroundPlot(self):
        # Plotting the groundtrack
        fig, ax = plt.subplots()
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        ax.plot(self.__latlon_itrs.lon.to(u.deg), self.__latlon_itrs.lat.to(u.deg), 'b', transform=ccrs.Geodetic(), label='ITRS');
        ax.legend(loc='upper right', shadow=True, fontsize='x-large')
        ax.plot()

    def OrbitPlot(self):
        frame = OrbitPlotter3D()
        #frame.plot(Orbit.from_body_ephem(Earth), label=Earth)
        frame.plot(self.__ss, label="Earth Orbit")

if __name__ == "__main__":
    a = OrbitGroundTrack(plot = True)
    b = a.return_orbit()
    v = a.return_df()
    plt.show()
