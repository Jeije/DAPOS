import numpy as np
import matplotlib.pyplot as plt

#Assumptions: Circular Orbit (i.e. e=0)


#Returns orbit time in seconds
#Input is orbital altitude in meters (h)
def torb(h:float):
    re = 6371000
    g = 6.67430e-11
    M = 5.972e24
    a = h+re
    mu = g*M
    return 2*np.pi*np.sqrt(a**3/mu)

#Returns orbit distance in meters
#Input is orbital altitude in meters (h)
def orbd(h:float):
    re = 6371000
    a = h + re
    return 2*np.pi*a

#Returns orbit energy at given orbital height (h)
#Input is orbital altitude in meters (h)
def orbtoe(h:float):
    re = 6371000
    g = 6.67430e-11
    M = 5.972e24
    mu = g*M
    a = h + re
    ke = 0.5*mu/a
    pe = -mu/a
    return ke+pe

#Returns orbital altitude in meters for a given orbital energy
#Input is orbital energy in meters (h)
def etoorb(e:float):
    re = 6371000
    g = 6.67430e-11
    M = 5.972e24
    mu = g*M
    return -mu/(2*e)-re

#State start and end orbital altitude for orbit altitude increase manouvre
#Calculate chnage in energy between both orbits
h_start = 195000
h_end = 250000
t = np.linspace(0.0001,0.001,100)

deltae = orbtoe(h_end)-orbtoe(h_start)
timelst = []

#Performing numerical integration untile the requiere change in energy is obtained
for idx,x in enumerate(t):
    h = 200000.0
    e = 0.0
    time = 0.0
    while deltae > e:
        #print(h,time,e)
        de = (x/1000)*orbd(h)
        time += torb(h)
        e += de
        h = etoorb(de+orbtoe(h))
    timelst.append(time/(60*60*24*365))
    a = idx/len(t)
    print('Progress:',a)

#Plotting results for time vs thrust
plt.plot(t,timelst)
plt.ylabel('Years')
plt.xlabel('MilliNewtons (mN)')
plt.title('Time (years) vs Thrust')
plt.grid(True)
plt.show()