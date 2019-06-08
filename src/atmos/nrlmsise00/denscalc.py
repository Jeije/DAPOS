from src.atmos.nrlmsise00.model.nrlmsise_00 import *
import time
import numpy as np
from src.atmos.nrlmsise00.misc_func import monthtodoy

def nlrmsise00(year:int=1994, month:int=1, day:int=10, sec:float=0, h:float=190, lat:float=-70, lon:float=100, indices:np.array=np.array([60,60,0,0,0,0,0,0,0])):
    output = [nrlmsise_output() for _ in range(2)]
    Input = [nrlmsise_input() for _ in range(2)]
    flags = nrlmsise_flags()
    aph = ap_array()

    for i in range(24):
        flags.switches[i]=1
    flags.switches[0] = 1
    flags.switches[9] = 1

    for i in range(7):
        aph.a[i] = indices[2:8]

    doy = monthtodoy(year, month, day)

    Input[1].doy = doy
    Input[1].year = year  # /* without effect */
    Input[1].sec = sec
    Input[1].alt = h
    Input[1].g_lat = lat
    Input[1].g_long = lon
    Input[1].f107 = indices[0]
    Input[1].f107A = indices[1]
    Input[1].ap_a = aph
    #Input[1].ap = 0

    gtd7(Input[1], flags, output[1])

    return output[1]

if __name__ == '__main__':
    start = time.clock()
    a = nlrmsise00()
    print(a.d[5])
    print(time.clock() - start)