from src.orbit.OrbitDragCalc import OrbitAtmosCalc
import matplotlib.pyplot as plt
import numpy as np

hmin = 210
hmax = 250

yearmax = [1990]
yearmin = [1986,1994,2008]
monthlst = [1,2,3,4,5,6,7,8,9,10,11,12]
daylst = [3,5,7,10,13,15,17,20,22]
sec = 10

dens_lst = []

i=0

for year in yearmax:
    i+=300
    for month in monthlst:
        for day in daylst:
            i+=1
            print(year,month,day)
            a = OrbitAtmosCalc(150,year,month,day,sec,hmax).return_pros()
            dens = [i,a[0][5],a[1][5],a[2][5]]
            dens_lst.append(dens)

dens_lst = np.array(dens_lst)
plt.plot(dens_lst[:,0],dens_lst[:,1])
plt.show()
