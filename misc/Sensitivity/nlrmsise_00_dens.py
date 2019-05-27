# -*- coding: utf-8 -*-
"""
Created on Mon May 13 19:59:10 2019

@author: flori
"""

import matplotlib.pyplot as plt
from matplotlib import *
from math import *
import numpy as np
from nrlmsise_00_header import *
from nrlmsise_00_data import *
from nrlmsise_00_start import *
from nlrmsise_00_dens import *

def nlrmsise00_dens(alt):

    output = [nrlmsise_output() for _ in range(17)]
    Input = [nrlmsise_input() for _ in range(17)]
    flags = nrlmsise_flags()

    flags.switches[0] = 1
    
    for i in range(1, 24):
        flags.switches[i]=1

    Input[1].doy = 172
    Input[1].year = 0  # /* without effect */
    Input[1].sec = 29000
    Input[1].alt = alt
    Input[1].g_lat = 60
    Input[1].g_long = -70
    Input[1].lst = 16
    Input[1].f107A = 240 #max 240
    Input[1].f107 = 280 #max 280
    Input[1].ap = 4
    gtd7(Input[1], flags, output[1])

    return output[1].d[5]
