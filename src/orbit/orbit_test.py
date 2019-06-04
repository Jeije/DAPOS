# import numpy as np
# import matplotlib.pyplot as plt
# from astropy.coordinates import CartesianRepresentation, SphericalRepresentation
#
#
# from astropy import units as u
#
# from poliastro.bodies import Earth, Moon
# from poliastro.twobody import Orbit
# from poliastro.plotting import static
#
# r = [-6045, -3490, 2500] * u.km
# v = [-3.457, 6.618, 2.533] * u.km / u.s
# ss_i = Orbit.from_vectors(Earth, r, v)
# ss = static.StaticOrbitPlotter()
# a = ss_i.represent_as(SphericalRepresentation)
# print(a)
# ss_i2 = ss_i.propagate(30 * u.min)
# b = ss_i2.represent_as(SphericalRepresentation)
# print(b)


from numpy import radians
from scipy.constants import kilo
from orbital import earth, KeplerianElements, plot

from orbital import earth, KeplerianElements, Maneuver, plot, plot3d
# Create molniya orbit from period and eccentricity
from orbital import earth_sidereal_day
molniya = KeplerianElements.with_period(
    earth_sidereal_day / 2, e=0.741, i=radians(63.4), arg_pe=radians(270),
    body=earth)

# Simple circular orbit
orbit = KeplerianElements.with_altitude(1000 * kilo, body=earth)

plot3d(molniya)

orbit4 = KeplerianElements.with_apside_radii(7000 * kilo, 8400 * kilo, body=earth)
plot(orbit4, title='Orbit 4')
