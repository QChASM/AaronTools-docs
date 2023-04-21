Job Submission Templates
========================

Job templates can be used when submitting a job to a queue with an AaronTools utility such as the :code:`jobSubmit.py` command line script.
Due to the uniqueness of each cluster, no job templates are included in the AaronTools installation - users must create their own.

There are several text patterns that are replaced by the corresponding resource or attribute requested by the job:

* :code:`{{ processors }}` - number of processors allocated to the job.
* :code:`{{ memory }}` - memory allocated to the job in gigabytes. Note that you might need to allocate more memory for the job than for the QM program, as QM software packages often use the specified memory only to limit their storage of large arrays (e.g. overlap integrals, wavefunction info). Other data might push their memory usage past the specified amount.
* :code:`{{ name }}` - name of the job.
* :code:`{{ walltime }}` - wall time allocated to the job in hours.

AaronTools can submit jobs to LSF, Slurm, PBS, and SGE queues.
You should specify what queuing software you are using by setting the :code:`QUEUE_TYPE` environment variable to :code:`LSF`, :code:`Slurm`, :code:`PBS`, or :code:`SGE`.

The default templates used for Gaussian, ORCA, Psi4, and Q-Chem jobs are $AARONLIB/Gaussian_template.txt, $AARONLIB/ORCA_template.txt, $AARONLIB/Psi4_template.txt, and $AARONLIB/QChem_template.txt respectively.
There is currently no default template location for other programs.

Examples
--------
Every cluster will be slightly different.
Pay close attention to where your scratch space should be, and how to make the Gaussian, Psi4, etc. executable available.
If you are uncertain of how your queuing system is set up, check whether your cluster administrators (or can help build) a submission script for these programs.
If so, we recommend using that as the starting point and modifying it with just the double curly braces outlined above.

PBS
^^^

Below is an example template for running Gaussian on a PBS queuing system.

.. code-block:: bash

    #PBS -S /bin/bash
    #PBS -N {{ name }}
    #PBS -q wheeler_q
    #PBS -l epilogue=/usr/local/lab/sewlab/cleanup
    #PBS -l nodes=1:ppn={{ processors }}
    #PBS -l walltime={{ walltime }}:00:00
    #PBS -l mem={{ memory }}gb
    
    module purge
    
    module load gaussian
    export GAUSS_SCRDIR=/scratch/$USER/$PBS_JOBID
    SCRATCH=$GAUSS_SCRDIR
    mkdir -p $SCRATCH
    cd $SCRATCH
    cp $PBS_O_WORKDIR/{{ name }}.com .
    g16 {{ name }}.com $PBS_O_WORKDIR/{{ name }}.log
    cd $PBS_O_WORKDIR
    rm -rf $SCRATCH
    exit

Slurm
^^^^^
Example of template for running ORCA on Slurm:

.. code-block:: bash

    #!/bin/bash
    #SBATCH --job-name={{ name }}
    #SBATCH --partition wheeler_p
    #SBATCH --ntasks={{ processors }}
    #SBATCH --cpus-per-task=1
    #SBATCH --time={{ walltime }}:00:00
    #SBATCH --mem={{ memory }}gb
    
    module purge
    
    module load ORCA
    export orcaroot=`which orca`
    SCRATCH=/scratch/$USER/$SLURM_JOB_ID
    mkdir -p $SCRATCH
    cd $SCRATCH
    cp $SLURM_SUBMIT_DIR/{{ name }}.inp .
    $orcaroot {{ name }}.inp > $SLURM_SUBMIT_DIR/{{ name }}.out
    if [ -e *.hess ]; then
        for hessfile in *.hess; do
            cp $hessfile $SLURM_SUBMIT_DIR
        done
    fi
    cd $SLURM_SUBMIT_DIR
    rm -rf $SCRATCH
    exit