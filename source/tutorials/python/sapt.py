from AaronTools.component import Component
from AaronTools.geometry import Geometry
from AaronTools.theory import *
from AaronTools.job_control import SubmitProcess

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

outfile='dimer.in'

# write Psi4 input then submit job
dimer.write(outfile=outfile, theory=theory)
submit_process = SubmitProcess(outfile, 12, 4, 8)
try:
    submit_process.submit()
except Exception as e:
    warn("failed to submit %s: %s" % (outfile, str(e)))

