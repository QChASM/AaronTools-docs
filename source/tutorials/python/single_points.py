# build Gaussian input files for Single Point calculations on all LOG files in 
# current directory 
# use LANL2DZ basis and ECP on any transition metal and 6-311+G(d,p) on everything else

from AaronTools.geometry import Geometry
from AaronTools.theory import *
from AaronTools.job_control import SubmitProcess
import glob

# build basis object
basis = BasisSet(
    [
        Basis("6-311+G(d,p)", AnyNonTransitionMetal()),
        Basis("LANL2DZ", AnyTransitionMetal()),
    ],
    [ECP("LANL2DZ")]
)

# build theory object
method = Theory(
    method="b3lyp",
    empirical_dispersion="D3",
    basis=basis,
    job_type=SinglePointJob()
    processors=8,
    memory=12,
)

# loop over LOG files in current directory
for LOG in glob.glob("*.xyz"):
    name = LOG.split('.')[0]   # grab name without .log ending
    geom = Geometry(LOG)       # build AaronTools geometry
    outfile = f"{name}.sp.com" # build filename with .com extension for Gaussian
    geom.write(outfile=outfile, theory=method) # make input file

    # create SubmitProcess object
    submit_process = SubmitProcess(outfile, 12, 8, 12)

    # submit job
    try:
        submit_process.submit()
    except Exception as e:
        warn("failed to submit %s: %s" % (outfile, str(e)))
