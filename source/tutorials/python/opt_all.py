# build ORCA input files for optimization + frequency calculation on all XYZ files in current directory
from AaronTools.geometry import Geometry
from AaronTools.theory import *
from AaronTools.job_control import SubmitProcess
import glob

# build theory object
method = Theory(
    method="wb97xd",
    basis="def2-tzvp",
    job_type=[OptimizationJob(), FrequencyJob()]
)

# loop over XYZ files in current directory
for XYZ in glob.glob("*.xyz"):
    name = XYZ.split('.')[0]  # grab name without .xyz ending
    geom = Geometry(XYZ)      # build AaronTools geometry
    outfile = name + "." + "inp" # build filename with .inp extension for ORCA
    geom.write(outfile=outfile, theory=method) # make input file

    # create SubmitProcess object
    submit_process = SubmitProcess(outfile, 12, 8, 12)

    # submit job
    try:
        submit_process.submit()
    except Exception as e:
        warn("failed to submit %s: %s" % (outfile, str(e)))
