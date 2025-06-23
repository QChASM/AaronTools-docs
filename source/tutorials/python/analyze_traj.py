#!/usr/bin/env python3
# print a table of selected distances and angles from an XYZ trajectory

from AaronTools.geometry import Geometry
from AaronTools.fileIO import FileReader
import numpy as np

fr = FileReader('traj.xyz', get_all=True)

# print header
print("  Step     R(1,2)   A(2,1,3)")

# loop over all XYZ files
for step,struc in enumerate(fr.all_geom):
    geom = Geometry(struc["atoms"])
    # get atoms 1, 2, 3
    a1, a2, a3 = geom.find(['1','2','3'])
    # get distance and angle
    dist = a1.dist(a2)
    angle = np.degrees(geom.angle(a2, a1, a3))
    # print data
    print(f"{step:5} {dist:10.3f} {angle:10.2f}")

