# build Gaussian input files for optimization + frequency calculation
# on all XYZ files in current directory 
# use LANL2DZ basis and ECP on any transition metal and 6-31G(d) on everything else

from AaronTools.geometry import Geometry
from AaronTools.theory import *
from AaronTools.job_control import SubmitProcess
import glob

# build basis object
basis = BasisSet(
    [
        Basis("6-31G(d)", AnyNonTransitionMetal()),
        Basis("LANL2DZ", AnyTransitionMetal()),
    ],
    [ECP("LANL2DZ")]
)

# build theory object
method = Theory(
    method="b3lyp",
    empirical_dispersion="D3",
    basis=basis,
    job_type=[OptimizationJob(), FrequencyJob()]
    processors=8,
    memory=12,
)

# loop over XYZ files in current directory
for XYZ in glob.glob("*.xyz"):
    name = XYZ.split('.')[0]  # grab name without .xyz ending
    geom = Geometry(XYZ)      # build AaronTools geometry
    outfile = f"{name}.com"   # filename with .com extension for Gaussian
    geom.write(outfile=outfile, theory=method) # make input file

    # create SubmitProcess object
    submit_process = SubmitProcess(outfile, 12, 8, 12)

    # submit job
    try:
        submit_process.submit()
    except Exception as e:
        warn("failed to submit %s: %s" % (outfile, str(e)))
