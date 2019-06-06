# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:30:38 2019

@author: msjor
"""
import numpy as np
from scipy.linalg import eigh, eig
import matplotlib.pyplot as plt
#beam properties
E = 69*10**9
I = 2.9268*10**(-9)
L = 2.5
ax = 0

#define mass distribution
m_base = 100
def m(x):
    #return m_base-(m_base/L)*x
    return m_base
def intm(x):
    #return m_base*x-m_base/2/L*x**2-m_base*L+m_base/2*L
    return m_base*(x-L)

#define stiffness distribution5
def II(x):
    return I

def dIdx(x):
    return 0

def ddIddx(x):
    return 0

#discretisation of beam
i_tot = 5       #number of modes considered
j_tot = i_tot       #number of collocation points

x_list = []

for i in range(j_tot):
    x_list.append((L/(j_tot)/2+(L/(j_tot))*(i)))
    
#define mode 1 to be considered  (cantilver root, free tip)

def m1(x, i):
    if i == 0:
        M1 = -1.14285714*np.cos(np.pi/2/L*x)-0.28571429*np.sin(np.pi/2/L*x)-0.07142857*np.cos(np.pi/L*x)+0.14285714*np.sin(np.pi/L*x)+1.21428571
        if i == 0:
            return M1

    if i == 1: 
        M2 = 1/(3*L**4)*x**4-4/(3*L**3)*x**3+2/(L**2)*x**2
        if i==1:
            return M2

    if i==2:
        M3 =  -0.57042254*np.cos(np.pi/L*x)-0.38028169*np.sin(np.pi/L*x)-0.11267606*np.cos(3*np.pi/2/L*x)+0.25352113*np.sin(3*np.pi/2/L*x)+0.68309859
        if i==2:
            return M3

    if i==3:
        M4 = -0.5*np.cos(np.pi/L*x)-0.125*np.cos(2*np.pi/L*x)+0.625
        if i == 3:
            return M4
    
    if i==4:
        M5 = -0.64*np.cos(3*np.pi/2/L*x)-0.36*np.sin(3*np.pi/2/L*x)-0.2025*np.cos(2*np.pi/L*x)+0.27*np.sin(2*np.pi/L*x)+0.8425
        if i==4:
            return M5
def dm1dx(x, i):
    if i == 0:
        M1 = 1.14285714*(np.pi/2/L)*np.sin(np.pi/2/L*x)-0.28571429*(np.pi/2/L)*np.cos(np.pi/2/L*x)+0.07142857*(np.pi/L)*np.sin(np.pi/L*x)+0.14285714*(np.pi/L)*np.cos(np.pi/L*x)
        if i == 0:
            return M1

    if i == 1:
        M2 =  4/(3*L**4)*x**3-12/(3*L**3)*x**2+4/(L**2)*x
        if i==1:
            return M2

    if i==2:
        M3 =  0.57042254*(np.pi/L)*np.sin(np.pi/L*x)-0.38028169*(np.pi/L)*np.cos(np.pi/L*x)+0.11267606*(3*np.pi/2/L)*np.sin(3*np.pi/2/L*x)+0.25352113*(3*np.pi/2/L)*np.cos(3*np.pi/2/L*x)
        if i==2:
            return M3

    if i==3:
        M4 = 0.5*(np.pi/L)*np.sin(np.pi/L*x)+0.125*(2*np.pi/L)*np.sin(2*np.pi/L*x)
        if i == 3:
            return M4

    if i==4:
        M5 = 0.64*(3*np.pi/2/L)*np.sin(3*np.pi/2/L*x)-0.36*(3*np.pi/2/L)*np.cos(3*np.pi/2/L*x)+0.2025*(2*np.pi/L)*np.sin(2*np.pi/L*x)+0.27*(2*np.pi/L)*np.cos(2*np.pi/L*x)
        if i==4:
            return M5
def ddm1ddx(x, i):
    if i == 0:
        M1= 1.14285714*(np.pi/2/L)**2*np.cos(np.pi/2/L*x)+0.28571429*(np.pi/2/L)**2*np.sin(np.pi/2/L*x)+0.07142857*(np.pi/L)**2*np.cos(np.pi/L*x)-0.14285714*(np.pi/L)**2*np.sin(np.pi/L*x)
        if i == 0:
            return M1
     
    if i ==1:   
        M2= 12/(3*L**4)*x**2-24/(3*L**3)*x+4/(L**2)
        if i==1:
            return M2

    if i==2:
        M3= 0.57042254*(np.pi/L)**2*np.cos(np.pi/L*x)+0.38028169*(np.pi/L)**2*np.sin(np.pi/L*x)+0.11267606*(3*np.pi/2/L)**2*np.cos(3*np.pi/2/L*x)-0.25352113*(3*np.pi/2/L)**2*np.sin(3*np.pi/2/L*x)
        if i==2:
            return M3

    if i==3:
        M4= 0.5*(np.pi/L)**2*np.cos(np.pi/L*x)+0.125*(2*np.pi/L)**2*np.cos(2*np.pi/L*x)
        if i == 3:
            return M4

    if i==4:
        M5 = 0.64*(3*np.pi/2/L)**2*np.cos(3*np.pi/2/L*x)+0.36*(3*np.pi/2/L)**2*np.sin(3*np.pi/2/L*x)+0.2025*(2*np.pi/L)**2*np.cos(2*np.pi/L*x)-0.27*(2*np.pi/L)**2*np.sin(2*np.pi/L*x)
        if i==4:
            return M5
def dddm1dddx(x, i):
    if i == 0:
        M1= -1.14285714*(np.pi/2/L)**3*np.sin(np.pi/2/L*x)+0.28571429*(np.pi/2/L)**3*np.cos(np.pi/2/L*x)-0.07142857*(np.pi/L)**3*np.sin(np.pi/L*x)-0.14285714*(np.pi/L)**3*np.cos(np.pi/L*x)
        if i == 0:
            return M1

    if i==1:
        M2= 24/(3*L**4)*x-24/(3*L**3)
        if i==1:
            return M2

    if i==2:
        M3= -0.57042254*(np.pi/L)**3*np.sin(np.pi/L*x)+0.38028169*(np.pi/L)**3*np.cos(np.pi/L*x)-0.11267606*(3*np.pi/2/L)**3*np.sin(3*np.pi/2/L*x)-0.25352113*(3*np.pi/2/L)**3*np.cos(3*np.pi/2/L*x)
        if i==2:
            return M3
    if i==3:
        M4= -0.5*(np.pi/L)**3*np.sin(np.pi/L*x)-0.125*(2*np.pi/L)**3*np.sin(2*np.pi/L*x)
        if i == 3:
            return M4

    if i==4:
        M5 = -0.64*(3*np.pi/2/L)**3*np.sin(3*np.pi/2/L*x)+0.36*(3*np.pi/2/L)**3*np.cos(3*np.pi/2/L*x)-0.2025*(2*np.pi/L)**3*np.sin(2*np.pi/L*x)-0.27*(2*np.pi/L)**3*np.cos(2*np.pi/L*x)
        if i==4:
            return M5
def ddddm1ddddx(x, i):
    if i == 0:
        M1= -1.14285714*(np.pi/2/L)**4*np.cos(np.pi/2/L*x)-0.28571429*(np.pi/2/L)**4*np.sin(np.pi/2/L*x)-0.07142857*(np.pi/L)**4*np.cos(np.pi/L*x)+0.14285714*(np.pi/L)**4*np.sin(np.pi/L*x)
        if i == 0:
            return M1
    if i==1:
        M2= 24/(3*L**4)
        if i==1:
            return M2

    if i==2:
        M3= -0.57042254*(np.pi/L)**4*np.cos(np.pi/L*x)-0.38028169*(np.pi/L)**4*np.sin(np.pi/L*x)-0.11267606*(3*np.pi/2/L)**4*np.cos(3*np.pi/2/L*x)+0.25352113*(3*np.pi/2/L)**4*np.sin(3*np.pi/2/L*x)
        if i==2:
            return M3
    if i==3:
        M4 = -0.5*(np.pi/L)**4*np.cos(np.pi/L*x)-0.125*(2*np.pi/L)**4*np.cos(2*np.pi/L*x)
        if i == 3:
            return M4

    if i==4:
        M5 = -0.64*(3*np.pi/2/L)**4*np.cos(3*np.pi/2/L*x)-0.36*(3*np.pi/2/L)**4*np.sin(3*np.pi/2/L*x)-0.2025*(2*np.pi/L)**4*np.cos(2*np.pi/L*x)+0.27*(2*np.pi/L)**4*np.sin(2*np.pi/L*x)
        if i==4:
            return M5
#find first mode natural frequency
K = np.zeros((j_tot,j_tot))
M = np.zeros((j_tot,j_tot))
for i in range(j_tot):
    for j in range(j_tot):
        xj = x_list[j]
        K[i][j]=E*II(xj)*ddddm1ddddx(xj,i)+2*E*dIdx(xj)*dddm1dddx(xj,i)+E*ddIddx(xj)*ddm1ddx(xj,i)+ax*intm(xj)*ddm1ddx(xj,i)-m(xj)*ax*m1(xj,i)
        M[i][j]=m(xj)*m1(xj,i)
    
freqs, vecs = eig(K,M)
freqs = np.sqrt(freqs)      #natural frequencies in rad/sec
freqsHz = freqs/2/np.pi  #natural frequencies in Hz

# plot modes for shits and giggles
x_plot = np.linspace(0.,L,50)
m1_plot = []
m2_plot = []
m3_plot = []
m4_plot = []
m5_plot = []
for k in x_plot:
    m1_plot.append(m1(k,0))
    m2_plot.append(m1(k,1))
    m3_plot.append(m1(k,2))
    m4_plot.append(m1(k,3))
    m5_plot.append(m1(k,4))
plt.plot(x_plot, m1_plot, "red", linestyle = "--")
plt.plot(x_plot, m2_plot, "blue", linestyle = "-.")
plt.plot(x_plot, m3_plot, "green", linestyle = "-")
plt.plot(x_plot, m4_plot, "black", linestyle = "--")
plt.plot(x_plot, m5_plot, "yellow", linestyle = "--")
plt.show()
    