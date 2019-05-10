from math import *
import matplotlib.pyplot as plt
import numpy as np

#parameters
G = 6.67*10**-11
M = 5.972*10**24
r = 250000 + 6371000
g = 9.80665

rho = 0.2
V = sqrt(G*M/r)
A = pi


cd = [2, 2.25, 2.5, 2.75, 3, 3.2]

Ft = [.5*rho*V**2*A*x for x in cd]

Isp = np.arange(1, 4001,1)

eff = np.empty([len(cd), len(Isp)])

for i in range(len(cd)):
    for j in range(len(Isp)):
        eff[i,j] = .5*V*cd[i]/g/Isp[j]
    plt.plot(eff[i,:], Isp)


plt.xlim(0,1)
plt.ylim(0,4000)
plt.xlabel('Collection Efficiency [%]')
plt.ylabel('Specific Impulse [s]')
plt.show()

print(eff)