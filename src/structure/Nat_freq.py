# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:30:38 2019

@author: msjor
"""
import numpy as np
from scipy.linalg import eig, null_space
import matplotlib.pyplot as plt
from scipy.integrate import quad
from sympy import Matrix
from trapezoid import trapezoid, centroid, moi
####################################### Inputs from design ##################################################
#beam & material properties
#I = 3.5*10**(-4)     #[m^4]
L = 2.5               #[m] length of the satellite body
disc = 400              #[-] number of sections used for discretisation of the beam 
Ak = 0.4                    #[m^2]  enclosed area
kappa = 0.51                #timoshenko coeffcient

mat = "comp"
if mat == "alu":
    rho = 2700
    E = 69*10**9            #E modulus of material
    syield = 503*10**6      #[MPa] yield stress
    G = 25*10**9                #[Pa]shear modulus
elif mat == "comp":
    rho = 1416              #kg/m^3
    E = 71.58*10**9            #E modulus of material
    syield = 647*10**6      #[MPa] yield stress
#cross-sectional properties
area = 0.4

#loading definitions
g = 9.81                #[m/s^2] gravitational5 acceleration
ax = 0*g                #[m/s^2] average axial acceleration for freqency analysis
ax_max = 10*g           #[m/s^2] Maximum axial acceleration
ay_max=  2*g            #[m/s^2] Maximum lateral acceleration in y direction 
az_max = 2*g            #[m/s^2] Maximum lateral acceleration in z direction 

#define thickness dirbution
def t(x):
    return 0.000135*14
def A(x):
    return (1.079+0.49+2*0.589)*t(x)

#define mass distribution
m_base = 150/L
def m(x):
    return -24*x+90
def intm(x):
    val, err = quad(m,x,L)
    return -val

def integratedM(x):
    val, err = quad(m,0,x)
    return val

mtot = integratedM(L)
#define stiffness distribution
def II(x):
    verts = trapezoid(area, 30)
    cx, cy = centroid(verts, t(x))
    verts[0] = verts[0] - cx
    verts[1] = verts[1] - cy
    return moi(verts,t(x))[0], cy

def dIdx(x):
    moms = []
    for i in range(3):
        k = i-1
        verts = trapezoid(area, 30)
        cx, cy = centroid(verts, t(x-k*L/disc))
        verts[0] = verts[0] - cx
        verts[1] = verts[1] - cy
        moms.append(moi(verts,t(x-k*L/disc))[0])
    return (moms[2]-moms[0])/(2*L/disc)

def ddIddx(x):
    moms = []
    for i in range(3):
        k = i-1
        verts = trapezoid(area, 30)
        cx, cy = centroid(verts, t(x-k*L/disc))
        verts[0] = verts[0] - cx
        verts[1] = verts[1] - cy
        moms.append(moi(verts,t(x-k*L/disc))[0])
    return (moms[2]-2*moms[1]+moms[0])/(L**2/disc**2)


# =============================================================================
# Definition of modes
# =============================================================================
def m1(x, i):
    if i == 0:
        M1 = -1.14285714*np.cos(np.pi/2/L*x)-0.28571429*np.sin(np.pi/2/L*x)-0.07142857*np.cos(np.pi/L*x)+0.14285714*np.sin(np.pi/L*x)+1.21428571
        return M1

    if i == 5 and freq: 
        M2 = 1/(3*L**4)*x**4-4/(3*L**3)*x**3+2/(L**2)*x**2
        return M2

    if i==2:
        M3 =  -0.57042254*np.cos(np.pi/L*x)-0.38028169*np.sin(np.pi/L*x)-0.11267606*np.cos(3*np.pi/2/L*x)+0.25352113*np.sin(3*np.pi/2/L*x)+0.68309859
        return M3

    if i==3:
        M4 = -0.5*np.cos(np.pi/L*x)-0.125*np.cos(2*np.pi/L*x)+0.625
        return M4
    
    if i==1:
        M5 = -0.64*np.cos(3*np.pi/2/L*x)-0.36*np.sin(3*np.pi/2/L*x)-0.2025*np.cos(2*np.pi/L*x)+0.27*np.sin(2*np.pi/L*x)+0.8425
        return M5
    
    if i==5 and not freq:
        M6 = -0.94117647*np.cos(np.pi/2/L*x)+ 0.05882353*np.sin(np.pi/2/L*x)-0.00367647*np.cos(2*np.pi/L*x)-0.01470588*np.sin(2*np.pi/L*x)+0.94485294
        return M6
    
    if i==4:
        M7 = -9.60795248*np.exp(-x/L)+16.40172873*np.exp(-2*x/L)-15.96611887*np.exp(-3*x/L)+6.17571291*np.exp(-4*x/L)+2.99662971
        return M7
    
    if i==6:
        M8 = -249.00521904*np.exp(-x/4/L)+454.19745321*np.exp(-x/2/L)-381.55422106*np.exp(-3*x/4/L)+121.31824395*np.exp(-x/L)+55.04374294
        return M8
    
    if i==7:
        M9 = -0.01498904*np.exp(-4*x/L)+0.3957065*np.exp(-8*x/L)-4.74712819*np.exp(-12*x/L)+3.36624015*np.exp(-16*x/L)+1.00017058
        return M9
def dm1dx(x, i):
    if i == 0:
        M1 = 1.14285714*(np.pi/2/L)*np.sin(np.pi/2/L*x)-0.28571429*(np.pi/2/L)*np.cos(np.pi/2/L*x)+0.07142857*(np.pi/L)*np.sin(np.pi/L*x)+0.14285714*(np.pi/L)*np.cos(np.pi/L*x)
        return M1

    if i == 5 and freq:
        M2 =  4/(3*L**4)*x**3-12/(3*L**3)*x**2+4/(L**2)*x
        return M2

    if i==2:
        M3 =  0.57042254*(np.pi/L)*np.sin(np.pi/L*x)-0.38028169*(np.pi/L)*np.cos(np.pi/L*x)+0.11267606*(3*np.pi/2/L)*np.sin(3*np.pi/2/L*x)+0.25352113*(3*np.pi/2/L)*np.cos(3*np.pi/2/L*x)
        return M3

    if i==3:
        M4 = 0.5*(np.pi/L)*np.sin(np.pi/L*x)+0.125*(2*np.pi/L)*np.sin(2*np.pi/L*x)
        return M4

    if i==1:
        M5 = 0.64*(3*np.pi/2/L)*np.sin(3*np.pi/2/L*x)-0.36*(3*np.pi/2/L)*np.cos(3*np.pi/2/L*x)+0.2025*(2*np.pi/L)*np.sin(2*np.pi/L*x)+0.27*(2*np.pi/L)*np.cos(2*np.pi/L*x)
        return M5

    if i==5 and not freq:
        M6 = 0.94117647*(np.pi/2/L)*np.sin(np.pi/2/L*x)+ 0.05882353*(np.pi/2/L)*np.cos(np.pi/2/L*x)+0.00367647*(np.pi*2/L)*np.sin(2*np.pi/L*x)-0.01470588*(np.pi*2/L)*np.cos(2*np.pi/L*x)
        return M6

    if i==4:
        M7 = 9.60795248*np.exp(-x/L)-2*16.40172873*np.exp(-2*x/L)+3*15.96611887*np.exp(-3*x/L)-4*6.17571291*np.exp(-4*x/L)
        return M7

    if i==6:
        M8 = 249.00521904/4*np.exp(-x/4/L)-454.19745321/2*np.exp(-x/2/L)+3*381.55422106/4*np.exp(-3*x/4/L)-121.31824395*np.exp(-x/L)
        return M8

    if i==7:
        M9 = 4*0.01498904*np.exp(-4*x/L)-8*0.3957065*np.exp(-8*x/L)+12*4.74712819*np.exp(-12*x/L)-16*3.36624015*np.exp(-16*x/L)
        return M9
def ddm1ddx(x, i):
    if i == 0:
        M1= 1.14285714*(np.pi/2/L)**2*np.cos(np.pi/2/L*x)+0.28571429*(np.pi/2/L)**2*np.sin(np.pi/2/L*x)+0.07142857*(np.pi/L)**2*np.cos(np.pi/L*x)-0.14285714*(np.pi/L)**2*np.sin(np.pi/L*x)
        return M1
     
    if i ==5 and freq:   
        M2= 12/(3*L**4)*x**2-24/(3*L**3)*x+4/(L**2)
        return M2

    if i==2:
        M3= 0.57042254*(np.pi/L)**2*np.cos(np.pi/L*x)+0.38028169*(np.pi/L)**2*np.sin(np.pi/L*x)+0.11267606*(3*np.pi/2/L)**2*np.cos(3*np.pi/2/L*x)-0.25352113*(3*np.pi/2/L)**2*np.sin(3*np.pi/2/L*x)
        return M3

    if i==3:
        M4= 0.5*(np.pi/L)**2*np.cos(np.pi/L*x)+0.125*(2*np.pi/L)**2*np.cos(2*np.pi/L*x)
        return M4

    if i==1:
        M5 = 0.64*(3*np.pi/2/L)**2*np.cos(3*np.pi/2/L*x)+0.36*(3*np.pi/2/L)**2*np.sin(3*np.pi/2/L*x)+0.2025*(2*np.pi/L)**2*np.cos(2*np.pi/L*x)-0.27*(2*np.pi/L)**2*np.sin(2*np.pi/L*x)
        return M5
    
    if i==5 and not freq:
        M6 = 0.94117647*(np.pi/2/L)**2*np.cos(np.pi/2/L*x)- 0.05882353*(np.pi/2/L)**2*np.sin(np.pi/2/L*x)+0.00367647*(np.pi*2/L)**2*np.cos(2*np.pi/L*x)+0.01470588*(np.pi*2/L)**2*np.sin(2*np.pi/L*x)
        return M6
    
    if i==4:
        M7 = -9.60795248*np.exp(-x/L)+4*16.40172873*np.exp(-2*x/L)-9*15.96611887*np.exp(-3*x/L)+16*6.17571291*np.exp(-4*x/L)
        return M7

    if i==6:
        M8 = -249.00521904/16*np.exp(-x/4/L)+454.19745321/4*np.exp(-x/2/L)-9*381.55422106/16*np.exp(-3*x/4/L)+121.31824395*np.exp(-x/L)
        return M8

    if i==7:
        M9 = -4*4*0.01498904*np.exp(-4*x/L)+8*8*0.3957065*np.exp(-8*x/L)-12*12*4.74712819*np.exp(-12*x/L)+16*16*3.36624015*np.exp(-16*x/L)
        return M9
def dddm1dddx(x, i):
    if i == 0:
        M1= -1.14285714*(np.pi/2/L)**3*np.sin(np.pi/2/L*x)+0.28571429*(np.pi/2/L)**3*np.cos(np.pi/2/L*x)-0.07142857*(np.pi/L)**3*np.sin(np.pi/L*x)-0.14285714*(np.pi/L)**3*np.cos(np.pi/L*x)
        return M1

    if i==5 and freq:
        M2= 24/(3*L**4)*x-24/(3*L**3)
        return M2

    if i==2:
        M3= -0.57042254*(np.pi/L)**3*np.sin(np.pi/L*x)+0.38028169*(np.pi/L)**3*np.cos(np.pi/L*x)-0.11267606*(3*np.pi/2/L)**3*np.sin(3*np.pi/2/L*x)-0.25352113*(3*np.pi/2/L)**3*np.cos(3*np.pi/2/L*x)
        return M3
    if i==3:
        M4= -0.5*(np.pi/L)**3*np.sin(np.pi/L*x)-0.125*(2*np.pi/L)**3*np.sin(2*np.pi/L*x)
        return M4

    if i==1:
        M5 = -0.64*(3*np.pi/2/L)**3*np.sin(3*np.pi/2/L*x)+0.36*(3*np.pi/2/L)**3*np.cos(3*np.pi/2/L*x)-0.2025*(2*np.pi/L)**3*np.sin(2*np.pi/L*x)-0.27*(2*np.pi/L)**3*np.cos(2*np.pi/L*x)
        return M5

    if i==5 and not freq:
        M6 = -0.94117647*(np.pi/2/L)**3*np.sin(np.pi/2/L*x)- 0.05882353*(np.pi/2/L)**3*np.cos(np.pi/2/L*x)-0.00367647*(np.pi*2/L)**3*np.sin(2*np.pi/L*x)+0.01470588*(np.pi*2/L)**3*np.cos(2*np.pi/L*x)
        return M6

    if i==4:
        M7 = 9.60795248*np.exp(-x/L)-8*16.40172873*np.exp(-2*x/L)+27*15.96611887*np.exp(-3*x/L)-64*6.17571291*np.exp(-4*x/L)
        return M7
    
    if i==6:
        M8 = 249.00521904/64*np.exp(-x/4/L)-454.19745321/8*np.exp(-x/2/L)+27*381.55422106/64*np.exp(-3*x/4/L)-121.31824395*np.exp(-x/L)
        return M8
    
    if i==7:
        M9 = 4*4*4*0.01498904*np.exp(-4*x/L)-8*8*8*0.3957065*np.exp(-8*x/L)+12*12*12*4.74712819*np.exp(-12*x/L)-16*16*16*3.36624015*np.exp(-16*x/L)
        return M9
def ddddm1ddddx(x, i):
    if i == 0:
        M1= -1.14285714*(np.pi/2/L)**4*np.cos(np.pi/2/L*x)-0.28571429*(np.pi/2/L)**4*np.sin(np.pi/2/L*x)-0.07142857*(np.pi/L)**4*np.cos(np.pi/L*x)+0.14285714*(np.pi/L)**4*np.sin(np.pi/L*x)
        return M1
    if i==5 and freq:
        M2= 24/(3*L**4)
        return M2

    if i==2:
        M3= -0.57042254*(np.pi/L)**4*np.cos(np.pi/L*x)-0.38028169*(np.pi/L)**4*np.sin(np.pi/L*x)-0.11267606*(3*np.pi/2/L)**4*np.cos(3*np.pi/2/L*x)+0.25352113*(3*np.pi/2/L)**4*np.sin(3*np.pi/2/L*x)
        return M3
    if i==3:
        M4 = -0.5*(np.pi/L)**4*np.cos(np.pi/L*x)-0.125*(2*np.pi/L)**4*np.cos(2*np.pi/L*x)
        return M4

    if i==1:
        M5 = -0.64*(3*np.pi/2/L)**4*np.cos(3*np.pi/2/L*x)-0.36*(3*np.pi/2/L)**4*np.sin(3*np.pi/2/L*x)-0.2025*(2*np.pi/L)**4*np.cos(2*np.pi/L*x)+0.27*(2*np.pi/L)**4*np.sin(2*np.pi/L*x)
        return M5

    if i==5 and not freq:
        M6 = -0.94117647*(np.pi/2/L)**4*np.cos(np.pi/2/L*x)+ 0.05882353*(np.pi/2/L)**4*np.sin(np.pi/2/L*x)-0.00367647*(np.pi*2/L)**4*np.cos(2*np.pi/L*x)-0.01470588*(np.pi*2/L)**4*np.sin(2*np.pi/L*x)
        return M6

    if i==4:
        M7 = -9.60795248*np.exp(-x/L)+16*16.40172873*np.exp(-2*x/L)-81*15.96611887*np.exp(-3*x/L)+256*6.17571291*np.exp(-4*x/L)
        return M7

    if i==6:
        M8 = -249.00521904/256*np.exp(-x/4/L)+454.19745321/16*np.exp(-x/2/L)-81*381.55422106/256*np.exp(-3*x/4/L)+121.31824395*np.exp(-x/L)
        return M8

    if i==7:
        M9 = -4*4*4*4*0.01498904*np.exp(-4*x/L)+8*8*8*8*0.3957065*np.exp(-8*x/L)-12*12*12*12*4.74712819*np.exp(-12*x/L)+16*16*16*16*3.36624015*np.exp(-16*x/L)
        return M9
def mode_BC(x, i, d):
    if i%4==1:
        if d==0:
            return -1.14285714*np.cos(i*np.pi/2/L*x)-0.28571429*np.sin(i*np.pi/2/L*x)-0.07142857*np.cos(i*np.pi/L*x)+0.14285714*np.sin(i*np.pi/L*x)+1.21428571
        if d==1:
            return 1.14285714*(i*np.pi/2/L)*np.sin(i*np.pi/2/L*x)-0.28571429*(i*np.pi/2/L)*np.cos(i*np.pi/2/L*x)+0.07142857*(i*np.pi/L)*np.sin(i*np.pi/L*x)+0.14285714*(i*np.pi/L)*np.cos(i*np.pi/L*x)
        if d==2:
            return 1.14285714*(i*np.pi/2/L)**2*np.cos(i*np.pi/2/L*x)+0.28571429*(i*np.pi/2/L)**2*np.sin(i*np.pi/2/L*x)+0.07142857*(i*np.pi/L)**2*np.cos(i*np.pi/L*x)-0.14285714*(i*np.pi/L)**2*np.sin(i*np.pi/L*x)
        if d==3:
            return -1.14285714*(i*np.pi/2/L)**3*np.sin(i*np.pi/2/L*x)+0.28571429*(i*np.pi/2/L)**3*np.cos(i*np.pi/2/L*x)-0.07142857*(i*np.pi/L)**3*np.sin(i*np.pi/L*x)-0.14285714*(i*np.pi/L)**3*np.cos(i*np.pi/L*x)
        if d==4:
            return -1.14285714*(i*np.pi/2/L)**4*np.cos(i*np.pi/2/L*x)-0.28571429*(i*np.pi/2/L)**4*np.sin(i*np.pi/2/L*x)-0.07142857*(i*np.pi/L)**4*np.cos(i*np.pi/L*x)+0.14285714*(i*np.pi/L)**4*np.sin(i*np.pi/L*x)
    elif i%4==2:
        if d==0:
            return -0.5*np.cos(i*np.pi/2/L*x)-0.125*np.cos(i*np.pi/L*x)+0.625
        if d==1:
            return 0.5*(i*np.pi/2/L)*np.sin(i*np.pi/2/L*x)+0.125*(i*np.pi/L)*np.sin(i*np.pi/L*x)
        if d==2:
            return 0.5*(i*np.pi/2/L)**2*np.cos(i*np.pi/2/L*x)+0.125*(i*np.pi/L)**2*np.cos(i*np.pi/L*x) 
        if d==3:
            return -0.5*(i*np.pi/2/L)**3*np.sin(i*np.pi/2/L*x)-0.125*(i*np.pi/L)**3*np.sin(i*np.pi/L*x) 
        if d==4:
            return -0.5*(i*np.pi/2/L)**4*np.cos(i*np.pi/2/L*x)-0.125*(i*np.pi/L)**4*np.cos(i*np.pi/L*x)            
    elif i%4==3:
        if d== 0:
            return -1.14285714*np.cos(i*np.pi/2/L*x)+0.28571429*np.sin(i*np.pi/2/L*x)-0.07142857*np.cos(i*np.pi/L*x)-0.14285714*np.sin(i*np.pi/L*x)+1.21428571
        if d==1:
            return 1.14285714*(i*np.pi/2/L)*np.sin(i*np.pi/2/L*x)+0.28571429*(i*np.pi/2/L)*np.cos(i*np.pi/2/L*x)+0.07142857*(i*np.pi/L)*np.sin(i*np.pi/L*x)-0.14285714*(i*np.pi/L)*np.cos(i*np.pi/L*x)
        if d==2:
            return 1.14285714*(i*np.pi/2/L)**2*np.cos(i*np.pi/2/L*x)-0.28571429*(i*np.pi/2/L)**2*np.sin(i*np.pi/2/L*x)+0.07142857*(i*np.pi/L)**2*np.cos(i*np.pi/L*x)+0.14285714*(i*np.pi/L)**2*np.sin(i*np.pi/L*x)
        if d==3:
            return -1.14285714*(i*np.pi/2/L)**3*np.sin(i*np.pi/2/L*x)-0.28571429*(i*np.pi/2/L)**3*np.cos(i*np.pi/2/L*x)-0.07142857*(i*np.pi/L)**3*np.sin(i*np.pi/L*x)+0.14285714*(i*np.pi/L)**3*np.cos(i*np.pi/L*x)
        if d==4:
            return -1.14285714*(i*np.pi/2/L)**4*np.cos(i*np.pi/2/L*x)+0.28571429*(i*np.pi/2/L)**4*np.sin(i*np.pi/2/L*x)-0.07142857*(i*np.pi/L)**4*np.cos(i*np.pi/L*x)-0.14285714*(i*np.pi/L)**4*np.sin(i*np.pi/L*x)


# =============================================================================
# Finding transverse natural frequencies 
# =============================================================================

#discretisation of beam
i_tot = 6       #number of modes considered
j_tot = i_tot       #number of collocation points
freq = True
x_list = []

for i in range(j_tot):
    x_list.append((L/(j_tot)/2+(L/(j_tot))*(i)))
    
#set up matrix problem for eigenvalue problem: K*x = lambda*M*x
K = np.zeros((j_tot,j_tot))
M = np.zeros((j_tot,j_tot))
#using the manually selected modes
for i in range(j_tot):
    for j in range(j_tot):
        xj = x_list[j]
        K[j][i]=E*II(xj)[0]*ddddm1ddddx(xj,i)+2*E*dIdx(xj)*dddm1dddx(xj,i)+E*ddIddx(xj)*ddm1ddx(xj,i)+ax*intm(xj)*ddm1ddx(xj,i)-m(xj)*ax*dm1dx(xj,i)
        M[j][i]=m(xj)*m1(xj,i)
        
#solve eignevalue problem 
freqs, vecs = eig(K,M)
freqs = np.sqrt(freqs)      #natural frequencies in rad/sec
freqsHz = freqs/2/np.pi  #natural frequencies in Hz
print ("Natural frequencies in Hz:", freqsHz)
print ("-------------------------------------")

x_plot = np.linspace(0.,L,disc)

#plot manual modes for natural frequency
plt.figure()
for i in range(j_tot):
    mode = []
    for k in x_plot:
        mode.append(m1(k,i))
    plt.plot(x_plot,mode, label = i)
plt.legend()
plt.show()
    

# =============================================================================
# Design for acceleration loads usingmodes that satisfy all boundary conditions
# =============================================================================
#discretisation of beam
freq = False
i_tot = 7       #number of modes considered
j_tot = i_tot       #number of collocation points


#plot manual modes for deformation
plt.figure()
for i in range(j_tot):
    mode = []
    for k in x_plot:
        mode.append(m1(k,i))
    plt.plot(x_plot,mode, label = i)
plt.legend()
plt.show()

x_list = []
for i in range(j_tot):
    x_list.append((L/(j_tot)/2+(L/(j_tot))*(i)))
 
KBO = np.zeros((j_tot,j_tot))
MBO = np.zeros((j_tot,j_tot))
MO = np.zeros((j_tot,1))
for i in range(j_tot):
    for j in range(j_tot):
        xj = x_list[j]
        KBO[j][i] = E*II(xj)[0]*ddddm1ddddx(xj,i)+2*E*dIdx(xj)*dddm1dddx(xj,i)+E*ddIddx(xj)*ddm1ddx(xj,i)
        MBO[j][i] = -m(xj)*dm1dx(xj,i)*0+(mtot-integratedM(xj)*0)*ddm1ddx(xj,i)
        MO[j] = m(xj)

acc, v = eig(np.matmul(np.linalg.inv(MBO),KBO), 1*np.identity(j_tot))
#acc, v = eig(KBO, -MBO)

#constant case
P_crit = np.pi**2/4/L/L*E*II(0)[0]
print ("Simple cantilever buckling acceleration [m/s]: ", P_crit/mtot)
print ("--------------------------------------")
#solve for stresses experienced during loading 
left_matrixO = KBO+MBO*ax_max
right_vectorO = MO*ay_max
coefficientsO = np.linalg.solve(left_matrixO, right_vectorO)

def buckled(x):
    shape = 0
    for i in range((j_tot)):
        shape+= coefficientsO[i]*m1(x,i)
    return shape

buckled_shapeO =[]

for i in x_plot:
    buckled_shapeO.append(buckled(i))
print ("Maximum deflectio [m]:", np.max(np.abs(buckled_shapeO)))
print ("----------------------------")       
dx = x_plot[1]-x_plot[0]
derivatives = []
moments = []
stresses = []
comps = []
shears = []
compF = []
shearF = []
testM = []

for p in range(len(x_plot)-2):
    loc = x_plot[p]
    if p ==0:
        xi = buckled_shapeO[p] 
        xi1= buckled_shapeO[p+1]
        xi2= buckled_shapeO[p+2]
        xi3 = buckled_shapeO[p+3]
        derivatives.append((2*xi-5*xi1+4*xi2-xi3)/(dx**2))
        moments.append(derivatives[p]*E*II(loc)[0]/1000)
        stresses.append(np.abs(E*derivatives[p]*(0.51-abs(II(loc)[1]))/(10**6)))
        comps.append((mtot-integratedM(loc))*ax_max/A(loc)/(10**3))
        shears.append((mtot-integratedM(loc))*ay_max/A(loc)/(10**3))
        compF.append((mtot-integratedM(loc))*ax_max/(10**3))
        shearF.append((mtot-integratedM(loc))*ay_max/(10**3))
    
    else:
        xib = buckled_shapeO[p-1]
        xi = buckled_shapeO[p]
        xia = buckled_shapeO[p+1]
        derivatives.append((xib-2*xi+xia)/(dx**2))
        moments.append(derivatives[p]*E*II(loc)[0]/1000)
        stresses.append(np.abs(E*derivatives[p]*(0.51-abs(II(loc)[1]))/(10**6)))
        compF.append((mtot-integratedM(loc))*ax_max/(10**3))
        shearF.append((mtot-integratedM(loc))*ay_max/(10**3))
        comps.append((mtot-integratedM(loc))*ax_max/A(loc)/(10**3))
        shears.append((mtot-integratedM(loc))*ay_max/A(loc)/(10**3))
    
    testM.append((L-loc)**3*m_base*ay_max/6/1000)
plt.figure()
plt.title("Shape under loading (blue) and its second derivative (green)")
plt.plot(x_plot, buckled_shapeO, "blue")
#plt.plot(x_plot[:-2], derivatives, "green")

plt.figure()
plt.title("Moments [kNm] (blue), compressive force [kN] (red) and shear force [kN] (green)")
plt.plot(x_plot[:-2], moments, "blue")
plt.plot(x_plot[:-2], shearF, "green")
plt.plot(x_plot[:-2], compF, "red")
#plt.plot(x_plot[:-2], testM, "blue",linestyle= "--")


shear_stresses = shears
tot_stresses = []
comb_stress = []
for i in range(len(stresses)):
    comb_stress.append(stresses[i]+comps[i]/1000)
    tot_stresses.append(np.sqrt(comb_stress[i]**2+(shear_stresses[i]/1000)**2))
    shear_stresses[i] = shear_stresses[i]/1000

    
plt.figure()
plt.title("Compressive stresses (blue), shear stresses (green) and combined stresses (red) [MPa]")
plt.plot(x_plot[:-2], stresses, "blue")
plt.plot(x_plot[:-2], shear_stresses, "green")
plt.plot(x_plot[:-2], tot_stresses, "red")

if np.max(tot_stresses)<syield/1.5:
    print ("structure is fine")
else:
    print ("Failure")

mass = 0.
for x in x_plot:
    mass+= A(x)*dx*rho
    
print ("Total mass estimate [kg]:", mass)











# =============================================================================
# Design for acceleration loads using new modes 
# =============================================================================

#def buckle_modes_sin(x,i,d):
#    if d == 0:
#        return np.sin(i*x*np.pi/2/L)
#    if d == 1:
#        return (np.pi*i/2/L)*np.cos(i*x*np.pi/2/L)
#    if d == 2:
#        return -(np.pi*i/2/L)**2*np.sin(i*x*np.pi/2/L)
#    if d == 3:
#        return -(np.pi*i/2/L)**3*np.cos(i*x*np.pi/2/L)
#    if d == 4:
#        return (np.pi*i/2/L)**4*np.sin(i*x*np.pi/2/L)
#
#def buckle_modes_cos(x,i,d):
#    if d == 0:
#        return np.cos(i*x*np.pi/2/L)
#    if d == 1:
#        return -(np.pi*i/2/L)*np.sin(i*x*np.pi/2/L)
#    if d == 2:
#        return -(np.pi*i/2/L)**2*np.cos(i*x*np.pi/2/L)
#    if d == 3:
#        return (np.pi*i/2/L)**3*np.sin(i*x*np.pi/2/L)
#    if d == 4:
#        return (np.pi*i/2/L)**4*np.cos(i*x*np.pi/2/L)
#    
#def buckle_modes_e(x,i,d):
#    if d == 0:
#        return np.exp(-i*x*np.pi/2/L)
#    if d == 1:
#        return (-i*np.pi/2/L)*np.exp(-i*x*np.pi/2/L)
#    if d == 2:
#        return (-i*np.pi/2/L)**2*np.exp(-i*x*np.pi/2/L)
#    if d == 3:
#        return (-i*np.pi/2/L)**3*np.exp(-i*x*np.pi/2/L)
#    if d == 4:
#        return (-i*np.pi/2/L)**4*np.exp(-i*x*np.pi/2/L)
#
#buckle_mode = 3
#coll = 3*buckle_mode      #number of collocation points
#
#x_list_b = []
#for i in range(coll):
#    x_list_b.append(((L/(coll-1))*(i)))
#    
#KB = np.ones((coll,coll))
#AB = np.ones((coll,coll))
#MYB = np.ones((coll,1))
#
##add sin modes to the matrix
#for i in range(buckle_mode):
#    for j in range(coll):
#        xj = x_list_b[j]
#        mb = i+1
#        KB[j,i] = E*II(xj)*buckle_modes_sin(xj,mb,4)+2*E*dIdx(xj)*buckle_modes_sin(xj,mb,3)+E*ddIddx(xj)*buckle_modes_sin(xj,mb,2)
#        #AB[j,i] = -m(xj)*buckle_modes_sin(xj,mb,1)+(mtot-integratedM(xj))*buckle_modes_sin(xj,mb,2)
#        AB[j,i] = buckle_modes_sin(xj,mb,2)
#        MYB[j] = m(xj)
#
##add cosine modes to the matrix
#for i in range(buckle_mode):
#    for j in range(coll):
#        xj = x_list_b[j]
#        mb = i+1
#        KB[j, i+buckle_mode] = E*II(xj)*buckle_modes_cos(xj,mb,4)+2*E*dIdx(xj)*buckle_modes_cos(xj,mb,3)+E*ddIddx(xj)*buckle_modes_cos(xj,mb,2)
#        #AB[j,i+buckle_mode] = -m(xj)*buckle_modes_cos(xj,mb,1)+(mtot-integratedM(xj))*buckle_modes_cos(xj,mb,2)
#        AB[j, i+buckle_mode] = buckle_modes_cos(xj,mb,2)
#        
##add exponential modes to the matrix
#for i in range(buckle_mode):
#    for j in range(coll):
#        xj = x_list_b[j]
#        mb = i+1
#        KB[j, i+buckle_mode*2] = E*II(xj)*buckle_modes_e(xj,mb,4)+2*E*dIdx(xj)*buckle_modes_e(xj,mb,3)+E*ddIddx(xj)*buckle_modes_e(xj,mb,2)
#        #AB[j,i+buckle_mode] = -m(xj)*buckle_modes_e(xj,mb,1)+(mtot-integratedM(xj))*buckle_modes_e(xj,mb,2)
#        AB[j, i+buckle_mode*2] = buckle_modes_e(xj,mb,2)
#
##replace last equation by BC: displacement(0)=0   
#for i in range(buckle_mode):
#    mb = i+1
#    KB[-1,i] = buckle_modes_sin(0,mb,0)
#    KB[-1,i+buckle_mode] = buckle_modes_cos(0,mb,0)
#    KB[-1,i+buckle_mode*2] = buckle_modes_e(0,mb,0)
#    AB[-1,i] = 0
#    AB[-1,i+buckle_mode] = 0  
#    AB[-1,i+buckle_mode*2] = 0
#    
##replace position s as well to impose zero slope at start
#s= 2 
#for i in range(buckle_mode):
#    mb = i+1
#    KB[s,i] = buckle_modes_sin(0,mb,1)
#    KB[s,i+buckle_mode] = buckle_modes_cos(0,mb,1)
#    KB[s,i+buckle_mode*2] = buckle_modes_e(0,mb,1)
#    AB[s,i] = 0
#    AB[s,i+buckle_mode] = 0  
#    AB[s,i+buckle_mode*2] = 0      
##solve for critical buckling accelerations in case of no transverse acceleration
#accelerations, vectors = eig(KB, -AB)
#
#print ("Critical buckling acceleration with no side force in m/s/s:", (accelerations))
#print ("-------------------------------------")
#
##solve for stresses experienced during loading 
#left_matrix = KB+AB*ax_max
#right_vector = MYB*ay_max
#right_vector[s] = 0
#right_vector[-1] = 0
#coefficients = np.linalg.solve(left_matrix, right_vector)
#
#def buckled(x):
#    shape = 0
#    for i in range((buckle_mode)):
#        shape+= coefficients[i]*buckle_modes_sin(x,i,0)+coefficients[i+buckle_mode]*buckle_modes_cos(x,i,0)+coefficients[i+buckle_mode*2]*buckle_modes_e(x,i,0)
#    return shape
#
#plt.figure()
#buckled_shape =[]
#for m in range(1,buckle_mode+1):
#
#    modec = []
#    modes = []
#    modee = []
#    for x in x_plot:
#        modec.append(buckle_modes_cos(x,m,0))
#        modes.append(buckle_modes_sin(x,m,0))        
#        modee.append(buckle_modes_e(x,m,0))    
#    plt.plot(x_plot, modec, "blue")
#    plt.plot(x_plot, modes, "red")
#    plt.plot(x_plot, modee, "green")
#for i in x_plot:
#    buckled_shape.append(buckled(i))
#    
#
#dx = x_plot[1]-x_plot[0]
#derivatives = []
#moments = []
#stresses = []
#for p in range(len(x_plot)-2):
#    if p ==0:
#        xi = buckled_shape[p] 
#        xi1= buckled_shape[p+1]
#        xi2= buckled_shape[p+2]
#        derivatives.append((xi-2*xi1+xi2)/(dx**2))
#        moments.append(derivatives[p]*E*II(xi)/1000)
#        stresses.append(np.abs(E*derivatives[p]*dist/(10**6)))
#    
#    else:
#        xib = buckled_shape[p-1]
#        xi = buckled_shape[p]
#        xia = buckled_shape[p+1]
#        derivatives.append((xib-2*xi+xia)/(dx**2))
#        moments.append(derivatives[p]*E*II(xi)/1000)
#        stresses.append(np.abs(E*derivatives[p]*dist/(10**6)))
#    
#print ("Maximum stress experienced due to launch loads [MPa]:", np.max(stresses))
#plt.figure()
#plt.title("Shape under loading (blue) and its second derivative (green)")
#plt.plot(x_plot, buckled_shape, "blue")
##plt.plot(x_plot[:-2], derivatives, "green")
#
#plt.figure()
#plt.title("Moments [kNm] (blue) and corresponding stresses [MPa] (green)")
#plt.plot(x_plot[:-2], moments, "blue")
#plt.plot(x_plot[:-2], stresses, "green")

























# =============================================================================
# #
# ##define set of equations to solve: 5 mode weights and axial acceleration
# #def equations():
# #    le1 =  KB[0,0]*a1+KB[0,1]*a2+KB[0,2]*a3+KB[0,3]*a4+KB[0,4]*a5-CB[0,0]*a1*ax-CB[0,1]*a2*ax-CB[0,2]*a3*ax-CB[0,3]*a4*ax-CB[0,4]*a5*ax
# #    re1 = MXB[0,0]*ax+MXB[0,1]*ax+MXB[0,2]*ax+MXB[0,3]*ax+MXB[0,4]*ax+MYB[0,0]*ay_max+MYB[0,1]*ay_max+MYB[0,2]*ay_max+MYB[0,3]*ay_max+MYB[0,4]*ay_max
# #    
# #    le2 =  KB[1,0]*a1+KB[1,1]*a2+KB[1,2]*a3+KB[1,3]*a4+KB[1,4]*a5-CB[1,0]*a1*ax-CB[1,1]*a2*ax-CB[1,2]*a3*ax-CB[1,3]*a4*ax-CB[1,4]*a5*ax
# #    re2 = MXB[1,0]*ax+MXB[1,1]*ax+MXB[1,2]*ax+MXB[1,3]*ax+MXB[1,4]*ax+MYB[1,0]*ay_max+MYB[1,1]*ay_max+MYB[1,2]*ay_max+MYB[1,3]*ay_max+MYB[1,4]*ay_max
# #
# #    le3 =  KB[2,0]*a1+KB[2,1]*a2+KB[2,2]*a3+KB[2,3]*a4+KB[2,4]*a5-CB[2,0]*a1*ax-CB[2,1]*a2*ax-CB[2,2]*a3*ax-CB[2,3]*a4*ax-CB[2,4]*a5*ax
# #    re3 = MXB[2,0]*ax+MXB[2,1]*ax+MXB[2,2]*ax+MXB[2,3]*ax+MXB[2,4]*ax+MYB[2,0]*ay_max+MYB[2,1]*ay_max+MYB[2,2]*ay_max+MYB[2,3]*ay_max+MYB[2,4]*ay_max
# #
# #    le4 =  KB[3,0]*a1+KB[3,1]*a2+KB[3,2]*a3+KB[3,3]*a4+KB[3,4]*a5-CB[3,0]*a1*ax-CB[3,1]*a2*ax-CB[3,2]*a3*ax-CB[3,3]*a4*ax-CB[3,4]*a5*ax
# #    re4 = MXB[3,0]*ax+MXB[3,1]*ax+MXB[3,2]*ax+MXB[3,3]*ax+MXB[3,4]*ax+MYB[3,0]*ay_max+MYB[3,1]*ay_max+MYB[3,2]*ay_max+MYB[3,3]*ay_max+MYB[3,4]*ay_max
# #
# #    le5 =  KB[4,0]*a1+KB[4,1]*a2+KB[4,2]*a3+KB[4,3]*a4+KB[4,4]*a5-CB[4,0]*a1*ax-CB[4,1]*a2*ax-CB[4,2]*a3*ax-CB[4,3]*a4*ax-CB[4,4]*a5*ax
# #    re5 = MXB[4,0]*ax+MXB[4,1]*ax+MXB[4,2]*ax+MXB[4,3]*ax+MXB[4,4]*ax+MYB[4,0]*ay_max+MYB[4,1]*ay_max+MYB[4,2]*ay_max+MYB[4,3]*ay_max+MYB[4,4]*ay_max
# #
# #    le6 = ax
# #    re6 = ax_max
# #    
# #    return [sy.Eq(le1 -re1), sy.Eq(le2- re2), sy.Eq(le3-re3), sy.Eq(le4-re4), sy.Eq(le5-re5), sy.Eq(le6-re6)]
# #
# #a1, a2, a3, a4, a5, ax  = sy.symbols('a1 a2 a3 a4 a5 ax')
# #coef = sy.solve(equations())
# #coefficients = list(coef[0].values())
# 
# =============================================================================


