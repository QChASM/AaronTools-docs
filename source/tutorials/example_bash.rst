Example BASH Scripts for Common Tasks
=====================================

AaronTools command line scripts (CLSs) make it simple to write BASH scripts to automate many routine tasks.
A few examples are provided here to get you started!
More examples will be added over time to make this a sort of 'cookbook' of AaronTools BASH scripts.

Optimization and Frequencies
----------------------------

Perhaps the most common task in routine quantum chemistry applications is optimizing geometries for a set of molecules and computing vibrational frequencies.
This can be done simply using AaronTools CLSs using any quantum chemistry software package.
Here we use Gaussian as an example, but trivial changes to the scripts below would instead use Q-Chem, ORCA, or Psi4.

For instance, suppose we have a set of XYZ files containing initial geomtries that we would like to optimize.
The following script will run wB97XD/def2TZVP optimizations and frequencies on all XYZ files in the current directory:

.. code-block:: bash

    #!/bin/bash
    # Perform wB97XD/def2TZVP optimizations/frequencies on all XYZ files

    for XYZ in `/bin/ls *.xyz`; do
      name=`basename $XYZ .xyz`
      makeInput.py $XYZ -m wB97XD -b "def2tzvp" -opt -freq -o $name.com
      jobSubmit.py $name.com -p 8 -m 12
    done

If initial XYZ files are not available, we can instead build all molecules from a list of IUPAC names and perform optimization + frequency computations.
For instance, suppose we have a file :code:`molecules` that contains a list of IUPAC names:

.. code-block:: bash

    #!/bin/bash
    # Perform wB97XD/def2TZVP optimizations/frequencies on all molecules listed in 'molecules'

    for mol in `cat molecules`; do
      fetchMolecule.py -i "$mol" | makeInput.py -m wB97XD -b "def2tzvp" -opt -freq -o "$mol.com"
      jobSubmit.py $mol.com -p 8 -m 12
    done

(Note that the above could be a little problematic if the IUPAC names include spaces, so it would be prudent to modify this to replace spaces in :code:`$mol` with "_", for example.)
   
Checking and Rerunning Jobs
---------------------------

After running the above optimizaitons, it is necessary to check two things:


#. Did the computations all finish correctly?
#. Are all optimized structures energy minima (no imaginary frequencies)

The following script will check these.
For jobs that did not generate an output file, the script just resubmits the original input file.
For jobs that ran but did not finish, a new job is submitted using the last geometry from the previous attempt using the same level of theory used in the corresponding output file.
For optimizations that ended with one or more imaginary vibrational frequencies, we displace along the vibrational mode using :code:`follow.py` and re-optimize.
We'll assume that we are working with a set of XYZ files, as in the first example above.
The modifications to instead use a list of IUPAC names should be obvious.
Changing the level of theory and/or quantum chemistry package should also be straightforward.

.. code-block:: bash

        #!/bin/bash
        # check all jobs and resubmit if needed, following imaginary frequency if present
        method="wb97xd"
        basis="def2tzvp"
        
        for XYZ in `/bin/ls *.xyz`; do
          name=`basename $XYZ .xyz`
        
          # Check if output file exists
          if [ ! -e $name.log ]; then
            echo $name did not run! Trying again.
            jobSubmit.py $name.com -p 8 -m 12
          else
        
            # check if job finished
            if [ `printInfo.py -i FINISHED $name.log | grep -c True` == 1 ]; then
             # check if geometry optimized to a minimum
              if [ `printFreq.py -t neg $name.log | wc -l` == 1 ]; then
                echo $name finished!
              else
                echo $name optimized to a saddle point--following imaginary mode
                follow.py $name.log | makeInput.py -m $method -b "$basis" -opt -freq -o $name.com
                jobSubmit.py $name.com -p 8 -m 12
              fi
            else
              echo $name not finished! Restarting
              makeInput.py $name.log -m $method -b "$basis" -opt -freq -o $name.com
              jobSubmit.py $name.com -p 8 -m 12
            fi
          fi
        done


