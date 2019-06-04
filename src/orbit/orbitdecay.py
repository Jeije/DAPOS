import numpy as np
from src.atmos.nrlmsise00 import nlrmsise00_dens

x = nlrmsise00_dens(200)


class Decay(object):

    def __init__(self, alt: int=200000):
        self.__data = None
        self.__height = alt


    def return_data(self):
        return self.__data

    def constgen(self):
        m_earth = 5.972 * (10 ** 24)
        G = 6.67 * (10 ** -11)
        m_sat = 150
        Cd = 2.4

    # def orbitcalc(self):
    #     while self.__height >= 0:
    #         fD = 0.5 * dens *



    # while orbit >= minimum:
    #
    #     fD = 0.5 * density * (velocity ** 2) * dragCoefficient * surfaceArea
    #     distance = (instantTime / P) * 3.14 * radius * 2
    #     workdone = fD * distance
    #     totalEnergy = totalEnergy - workdone
    #     radius = ((-0.5) * gvConstant * m1 * m2 / totalEnergy)
    #     velocity = ((gvConstant * m1) / radius) ** 0.5
    #     orbit = radius - earthRadius
    #     t += instantTime
    #     orbitList.append(orbit / 1000)
    #     timeList.append(t / 31536000)
    #     if orbit >= minimum:
    #         density = calDensity(orbit)
    #     else:
    #         break
    # years = float(t / 31536000)
    # print("years taken: %s" % (years))