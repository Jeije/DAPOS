from numpy import nper
import math as m

G = 6.673e-11
M = 5.972e+24

def v_orb(h:int):
    h = 6371*1000+h
    return m.sqrt(G*M/h)

def get_mflow(a:int,h:int,rho:int,eff:float):
    v = v_orb(h)
    return eff*a*v*rho*10**3

def scctoarea(sccm:float,h:int,rho:int,eff:float):
    mflow = sccm*10**-3/45.37
    v = v_orb(h)
    return mflow/(eff*v*rho*10**3)

def cd_calc(a:float):
