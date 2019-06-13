import numpy as np
import matplotlib.pyplot as plt

def trapezoid(area, side_angle):
    x = np.sqrt((4 * area * np.tan(np.deg2rad(side_angle)))/96)
    L1 = 11 * x
    L2 = (2 * area)/(16 * x)
    L3 = 5 * x
    vertices = np.array([[-L1 / 2, L1 / 2, L3 / 2, -L3 / 2, -L1 / 2], [0, 0, -L2, -L2, 0]])
    return vertices

def centroid(vertices, thickness):
    x = vertices[0]
    y = vertices[1]

    cx = 0.
    cy = 0.
    area = 0.

    for i in range(len(vertices[0])-1):
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]
        length = np.sqrt(dx * dx + dy * dy)

        xavg = (x[i] + x[i+1]) / 2
        yavg = (y[i] + y[i+1]) / 2

        cx += length * thickness * xavg
        cy += length * thickness * yavg
        area += length * thickness

    cx = cx/area
    cy = cy/area

    return cx, cy

def moi(vertices, thickness):
    cx, cy = centroid(vertices, thickness)
    x = vertices[0] - cx
    y = vertices[1] - cy

    Ixx = 0.
    Iyy = 0.

    for i in range(len(vertices[0])-1):
        dx = x[i+1] - x[i]
        dy = y[i+1] - y[i]

        xavg = (x[i] + x[i+1]) / 2
        yavg = (y[i] + y[i+1]) / 2

        beta = np.arctan(abs(dy) / abs(dx))
        length = np.sqrt(dx * dx + dy * dy)
        Ixx += thickness * length**3 * np.sin(beta) * np.sin(beta) / 12
        Ixx += thickness * length * xavg * xavg
        Iyy += thickness * length**3 * np.cos(beta) * np.cos(beta) / 12
        Iyy += thickness * length * yavg * yavg

    return Ixx, Iyy


area = 0.4
thickness = 0.001
#
#launcher = plt.Circle((0,0),0.6,color='k')
#feedline = plt.Circle((0,0),0.05,color='w')
#plt.gcf().gca().add_artist(launcher)
#plt.gcf().gca().add_artist(feedline)

verts = trapezoid(area, 30)
cx, cy = centroid(verts, 0.001)
verts[0] = verts[0] - cx
verts[1] = verts[1] - cy

print(moi(verts, thickness))

#plt.axis('equal')
#plt.xlim(-0.75, 0.75)
#plt.ylim(-0.75, 0.75)
#
#plt.plot(verts[0], verts[1])
#plt.show()