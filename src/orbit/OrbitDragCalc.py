from src.orbit.OrbitPosCalc import OrbitGroundTrack
from src.atmos.nrlmsise00.IndexReturn import Indexer
from src.atmos.nrlmsise00.denscalc import nlrmsise00

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

import numpy as np


year = 1970
month = 2
day = 30
s = 0


Indices = Indexer(year,month,day,s).return_indices()
Pos = OrbitGroundTrack(1000).return_df()
lat = np.array(Pos['Lat [deg]'])
lon = np.array(Pos['Lon [deg]'])
sec = np.array(Pos['Time [s]'])
h = np.array(Pos['Height [km]'])

anslst = []

for i in range(len(lat)):
    ans = nlrmsise00(year,month,day,sec[i],h[i],lat[i],lon[i],Indices)
    anslst.append(ans.d[5])

a = np.array(anslst)

# plt.plot(sec,anslst)
# plt.ylabel('Atmospheric Density [kg/m^3]')
# plt.xlabel('Time [s]')

# # Plotting the groundtrack
# fig, ax = plt.subplots()
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.stock_img()
# ax.plot(lon, lat, 'b', transform=ccrs.Geodetic(),
#         label='ITRS')
# ax.legend(loc='upper center', shadow=True, fontsize='x-large')
# ax.plot()


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


# Create a set of line segments so that we can color them individually
# This creates the points as a N x 1 x 2 array so that we can stack points
# together easily to get the segments. The segments array for line collection
# needs to be (numlines) x (points per line) x 2 (for x and y)
points = np.array([lon, lat]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig, ax = plt.subplots()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.plot(lon, lat, 'b', transform=ccrs.Geodetic(),
        label='ITRS');
ax.legend(loc='upper center', shadow=True, fontsize='x-large')

# Create a continuous norm to map from data points to colors
norm = plt.Normalize(a.min(), a.max())
lc = LineCollection(segments, cmap='viridis', norm=norm)
# Set the values used for colormapping
lc.set_array(a)
lc.set_linewidth(2)
line = ax.add_collection(lc)
fig.colorbar(line, ax=ax)


plt.show()