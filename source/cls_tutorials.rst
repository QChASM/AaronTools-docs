Command Line Script Tutorials
=============================

Overview
--------
Here, you will find tutorials and generalizations for AaronTools' various command line scripts.
For many of the scripts covered here, some options might not be described.
To see the full list of options for a script, run it with just the --help flag (e.g. substitute.py --help).


File Input/Output
-----------------

Reading a file
^^^^^^^^^^^^^^

To get a command line script to read a file, it can be as simple as passing the path to the file to the script: 

.. code-block:: bash

    printXYZ.py benzene.log
    
If the file can an unconventional extension, you can pass the format to the :code:`-if` flag: 

.. code-block:: bash

    printXYZ.py benzene.gout -if log

Many of our scripts also support reading the structure from standard input (e.g. pipes (:code:`|`), here documents (:code:`<<`)).
The input is assumed to be in XYZ format, but :code:`-if` can be used to specify other formats.
This can be used to avoid writing intermediate files. 

.. code-block:: bash

    substitute.py benzene.xyz -s H=F | bond.py xyz -c 6 7 0.3

Writing Geometry to a File
^^^^^^^^^^^^^^^^^^^^^^^^^^

Many of our scripts accept the :code:`-o` flag to specify the destination of the output.
If no :code:`-o` flag is specified, the script's normal output will be printed to the standard output. 


The :code:`printXYZ.py` command can be used to convert any AaronTools-readable file (.xyz, Gaussian .log file, Gaussian .com file, ORCA .out file) into an XYZ file:

.. code-block:: bash

    printXYZ.py benzene.log

:: 

    12
    
    C     -4.20339   -0.06691   -0.00131
    C     -4.19394   -1.46592   -0.00065
    C     -2.99654    0.64078   -0.00092
    C     -1.78023   -0.05054    0.00013
    C     -1.77078   -1.44955    0.00079
    C     -2.97763   -2.15724    0.00040
    H     -2.97032   -3.23955    0.00091
    H     -0.82981   -1.98437    0.00161
    H     -5.12759   -2.01341   -0.00096
    H     -5.14436    0.46792   -0.00213
    H     -0.84658    0.49695    0.00044
    H     -3.00385    1.72310   -0.00143


Finding Atoms
-------------

Atoms can be specified by index (1-indexed) or by element.
For example, to turn a benzene molecule into perfluorobenzene, we can substitute all hydrogens with fluorines: 

::
    
    substitute.py benzene.xyz -s H=F
    
The :code:`findAtoms.py` script can be helpful for locating atoms using a variety of descriptions.
These descriptions include the element, how many bonds the atom has, and what atoms are bonded to a specific atom.


Structure Modification
----------------------

Changing Substituents
^^^^^^^^^^^^^^^^^^^^^

In this example, we will be building 2,4,6-trinitrotoluene (TNT) from benzene and the substituents in the AaronTools Library.
Here is the benzene structure we are starting with:

.. code-block:: 

    12
    
    C         -4.20339       -0.06691       -0.00131
    C         -4.19394       -1.46592       -0.00065
    C         -2.99654        0.64078       -0.00092
    C         -1.78023       -0.05054        0.00013
    C         -1.77078       -1.44955        0.00079
    C         -2.97763       -2.15724        0.00040
    H         -2.97032       -3.23955        0.00091
    H         -0.82981       -1.98437        0.00161
    H         -5.12759       -2.01341       -0.00096
    H         -5.14436        0.46792       -0.00213
    H         -0.84658        0.49695        0.00044
    H         -3.00385        1.72310       -0.00143

For reference, here is how the atoms are ordered: 

.. image images/benzene_numbers.png

We can get to by running AaronTools' :code:`substitute.py` script twice.
First, let's turn our benzene into toluene by changing atom 7 into a methyl group: 

::

    substitute.py benzene.xyz -s 7=Me -o toluene.xyz

Our benzene structure is in benzene.xyz.
"Me" is the name of the methyl substituent in the AaronTools library.
The resulting structure will be saved to toluene.xyz. 

Now, we can change some hydrogens into nitro groups.
Because of the nature of our first substitution, all of the remaining hydrogens on the ring still have the same numbering. Therefore, our ortho and para positions are 8, 9, and 12.
We can run the substitute.py script again to turn these into nitro groups: 

::
    
    substitute.py toluene.xyz -s 8,9,12=NO2 -o tnt.xyz

We're using the toluene.xyz that we created in the previous step.
"NO2" is the name of the nitro substituent in the AaronTools library.
We are writing this to a file named tnt.xyz.


We could combine these two steps into one by simply specifying both substitution instructions: 

::
    
    substitute.py benzene.xyz -s 7=Me -s 8,9,12=NO2 -o tnt.xyz
    
Running Jobs
------------

Creating Input Files
^^^^^^^^^^^^^^^^^^^^

Now that we've modified benzene to get TNT, we ought to minimize our TNT structure before we analyze it.
:code:`makeInput.py` can help us set up the input file.
We'll be optimizing the structure and compute frequencies at the B3LYP/def2-SVP level of theory with Psi4.
To make the input file for the optimization job, run: 

.. code-block:: bash
    
    makeInput.py tnt.xyz -o tnt.in -opt -freq -m b3lyp -b def2-svp


* :code:`-opt` or :code:`--optimize` specifies an optimization job
* :code:`-freq` or :code:`--frequencies` specifies a normal vibrational mode calculation
* :code:`-m` or :code:`--method` specifies the method/DFT functional
* :code:`-b` or :code:`--basis` specifies the basis set
* :code:`-mem` or :code:`--memory` specifies the allocated memory in GB
* :code:`-p` or :code:`--processors` specifies the allocated number of CPU cores

The Psi4 input file is written to 'tnt.in'.
Because the '.in' extension was used, it's assumed that we want the file in Psi4 format.
Gaussian format is assumed when '.com' is used, and ORCA is assumed when '.inp' is used.
The contents of 'tnt.in' are:

.. code-block:: python

    set_num_threads(6)
    memory 12 GB
    basis {
        assign    def2-svp
    }
    
    molecule {
    0 1
    C     -4.20339   -0.06691   -0.00131
    C     -4.19394   -1.46592   -0.00065
    C     -2.99654    0.64078   -0.00092
    C     -1.78023   -0.05054    0.00013
    C     -1.77078   -1.44955    0.00079
    C     -2.97763   -2.15724    0.00040
    C     -2.96723   -3.69720    0.00113
    N     -0.44931   -2.20063    0.00194
    N     -5.50513   -2.23480   -0.00109
    H     -5.14436    0.46792   -0.00213
    H     -0.84658    0.49695    0.00044
    N     -3.00681    2.16075   -0.00164
    H     -2.23552   -4.07163   -0.74575
    H     -3.97618   -4.08316   -0.25664
    H     -2.68230   -4.07382    1.00630
    O      0.58497   -1.53501    0.00259
    O     -0.49200   -3.42985    0.00216
    O     -5.44583   -3.46333   -0.00240
    O     -6.54832   -1.58322   -0.00010
    O     -4.10039    2.72366   -0.00139
    O     -1.92093    2.73838   -0.00242
    }
    
    nrg = optimize('b3lyp')
    nrg = frequencies('b3lyp')


Submitting to the Queue 
^^^^^^^^^^^^^^^^^^^^^^^

If we're logged on to a computing cluster, we can submit this optimization job to the queue with jobSubmit.py.
We'll need to have a template job file that's compatible with the queuing software (e.g. SGE, PBS, Slurm).
Below is a template file for a Psi4 computation running on a PBS cluster: 

.. code-block:: bash
    
    #PBS -S /bin/bash
    #PBS -N {{ name }}
    #PBS -q wheeler_q
    #PBS -l epilogue=/usr/local/lab/sewlab/cleanup
    #PBS -l nodes=1:ppn={{ processors }}
    #PBS -l walltime={{ walltime }}:00:00
    #PBS -l mem={{ memory }}gb
    
    module purge
    
    # load the psi4 module, adding psi4 to our path
    module load PSI4
    # create a scratch area for this job
    SCRATCH=/scratch/$USER/$PBS_JOBID
    mkdir -p $SCRATCH
    cd $SCRATCH
    # move our input file to the scratch area and run the job
    cp $PBS_O_WORKDIR/{{ name }}.in .
    psi4 {{ name }}.in $PBS_O_WORKDIR/{{ name }}.dat
    cd $PBS_O_WORKDIR
    rm -rf $SCRATCH
    exit


the values surrounded by double curly brackets will be replaced by :code:`jobSubmit.py`:

* :code:`{{ name }}` - job name, will be determined by the name of the input file
* :code:`{{ walltime }}` - allowed wall time in hours
* :code:`{{ processors }}` - allocated cpu cores
* :code:`{{ memory }}` - allocated memory in gigabytes

If this file is placed in the Aaron_libs directory (defaults to "Aaron_libs" in your home area, but can be overwritten by setting the AARONLIB environment variable), in a file named Psi4_template.txt, it will automatically be used by jobSubmit.py. Similarly, Gaussian and ORCA default job templates can be put at Aaron_libs/Gaussian_template.txt and Aaron_libs/ORCA_template.txt, respectively.

A different default template, along with default processors, memory, and wall time may be specified in your configuration file.

To submit this job to the queue, we can run: 

::

    jobSubmit.py tnt.in -p 6 -m 12
    
where :code:`-p` and :code:`-m` are the allocated CPU cores and memory, respectively.
This will create and submit a job file named 'tnt.job':

.. code-block:: bash

    #PBS -S /bin/bash
    #PBS -N tnt
    #PBS -q wheeler_q
    #PBS -l epilogue=/usr/local/lab/sewlab/cleanup
    #PBS -l nodes=1:ppn=6
    #PBS -l walltime=12:00:00
    #PBS -l mem=12gb
    
    module purge
    
    # load the psi4 module, adding psi4 to our path
    module load PSI4
    # create a scratch area for this job
    SCRATCH=/scratch/$USER/$PBS_JOBID
    mkdir -p $SCRATCH
    cd $SCRATCH
    # move our input file to the scratch area and run the job
    cp $PBS_O_WORKDIR/tnt.in .
    psi4 tnt.in $PBS_O_WORKDIR/tnt.dat
    cd $PBS_O_WORKDIR
    rm -rf $SCRATCH
    exit

Our job should be queued::

    qstat -u $USER
    
    dispatch.ecompute:
                                                                                    Req'd       Req'd       Elap
    Job ID                  Username    Queue    Jobname          SessID  NDS   TSK   Memory      Time    S   Time
    ----------------------- ----------- -------- ---------------- ------ ----- ------ --------- --------- - ---------
    3409256.sapelo2         ajs99778    wheeler_ tnt              196715     1      6      12gb  12:00:00 Q       --


Analyzing Output
----------------

Now that we are running jobs with AaronTools, we will look at processing the output. 

Grabbing Thermochemical Corrections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

AaronTools can calculate several thermochemical corrections from the output of a frequency job: zero-point energy (or H 0K), rigid-rotor/harmonic oscillator (RRHO) enthalpy, RRHO free energy, quasi-RRHO free energy, and quasi-harmonic free energy.
AaronTools will recalculate each of these, even if they are printed in the output file, to maintain consistency with the constants that AaronTools uses.
The :code:`grabThermo.py` command line script can be used to print thermochemistry:

::

    grabThermo.py tnt.dat

At the time of writing, Psi4 does not compute IR intensities for DFT methods. 
However, if we used Gaussian, ORCA, or Q-Chem to perform this computations, we could generate an IR spectra from the output using the :code:`plotIR.py` script::

    plotIR.py tnt.log

