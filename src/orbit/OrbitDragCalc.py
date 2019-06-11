'''Importing Required Modules from Folder'''
from src.orbit.SatGroundTrack.GroundTrack import GroundTrackCalc
from src.atmos.nrlmsise00.IndexFindr.IndexReturn import Indexer
from src.atmos.nrlmsise00.AtmosCalc import nrl00,nrl00_cond

'''Importing Required Modules'''
import time
import os
import numpy as np
import datetime as dt
import pandas as pd
from astropy import units as u


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

class OrbitAtmosCalc1Day(object):
    def __init__(self, t:int=100, date: dt.datetime= dt.datetime(2010, 10, 2), inc:float = 94.7 * u.deg, h:float= 200 * u.km,
                 lat0: float = 12.77*u.deg, longi0: float = -91.37*u.deg):

        self.__date = date
        self.__inc = inc.to(u.deg)
        self.__h = h.to(u.km)
        self.__lat0 = lat0.to(u.deg)
        self.__longi0 = longi0.to(u.deg)
        self.__indices = Indexer(date).return_indices()[1:]
        self.__pos = GroundTrackCalc(dt = t, inc = inc.to(u.deg), h = h.to(u.meter), lat0 = lat0.to(u.deg),
                                     longi0=longi0.to(u.deg), n=0).return_data()

        self.__vals = np.zeros([len(self.__pos),20])
        self.__procs = np.zeros([3,11])

        for i in range(len(self.__pos)):
            self.__data = nrl00(self.__date,h ,self.__pos['Lat [deg]'][i]*u.deg, self.__pos['Lon [deg]'][i]*u.deg,
                                self.__indices)
            self.__date = date + dt.timedelta(0, self.__pos['time [s]'][i])
            self.__vals[i][0] = self.__date.year
            self.__vals[i][1] = self.__date.month
            self.__vals[i][2] = self.__date.day
            self.__vals[i][3] = self.__date.hour
            self.__vals[i][4] = self.__date.minute
            self.__vals[i][5] = self.__date.second
            self.__vals[i][6] = self.__pos['Lat [deg]'][i]
            self.__vals[i][7] = self.__pos['Lon [deg]'][i]
            self.__vals[i][8] = self.__pos['V_rel [m/s]'][i]
            self.__vals[i][9:18]=self.__data.d
            self.__vals[i][18:20]=self.__data.t

        self.df()
        self.save_csv(self.__df)

    def df(self):
        self.__df = pd.DataFrame(self.__vals)
        self.__df.columns = ['Year','Month','Day','Hour','Minute','Second','Lat','Long','V_rel',
                                 'He','O','N2','O2','Ar','Density','H','N','Anomalous Oxygen','Exospheric Temp','Temp']

    def return_vals(self):
        return self.__df

    def save_csv(self,dataframe: pd.DataFrame, filepath: str = r'\\'.join(os.getcwd().split('\\')[:-2]) +
                                                          '\\data\\atmosorbitdata\\'):
        '''Function save_csv'''
        '''PARAM 1: Pandas DataFrame containing processed AP data'''
        '''PARAM 2: Filepath to save processed AP data'''
        filepath = filepath + str(self.__inc.value) + ',' + str(self.__h.value) + ',' + str(self.__lat0.value) + ',' \
                   + str(self.__longi0.value) + ',' + str(self.__indices[0]) + ',' + str(self.__indices[1]) + ',' + \
                   str(self.__indices[2]) + '.csv'
        dataframe.to_csv(filepath)

if __name__ == "__main__":
    a = OrbitAtmosCalc1Day()
    b = a.return_vals()
    print(time.process_time())
