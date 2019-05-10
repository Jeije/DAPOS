from math import *
import numpy as np

def cam_res(alt, res):
    theta = np.arctan(res/2/alt)
    vleo = [100000, 110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000, 200000, 210000, 220000, 230000, 240000, 250000]
    vleores = [2*x*np.tan(theta) for x in vleo]

    return vleores

print(cam_res(3000000, 1))