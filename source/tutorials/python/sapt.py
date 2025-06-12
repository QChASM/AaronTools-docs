from AaronTools.component import Component
from AaronTools.geometry import Geometry
from AaronTools.theory import *

# make Geometry object from XYZ file containing dimer
dimer = Geometry("dimer.xyz")

# for SAPT, the monomers need to be in the geometry's components attribute
dimer.components = []
for mon in dimer.get_monomers():
    dimer.components.append(Component(mon))

# Modified Theory object for SAPT computations
theory = Theory(
    charge=[0, 0, 0],
    multiplicity=[1, 1, 1],
    method=SAPTMethod("sapt0"),
    basis="jun-cc-pvdz",
    processors=4,
    memory=8,
    job_type="energy",
)

dimer.write(outfile='dimer.in', theory=theory)
