Example Python Scripts for Common Tasks
=======================================

Many routine tasks can be handled using BASH scripts based on the AaronTools command line scripts (CLSs).
See :doc:`example_bash`.
However, for more complex tasks you'll need to use the AaronTools Python API.
A few examples are provided here to get you started (you can also peruse the `CLSs <https://github.com/QChASM/AaronTools.py/tree/master/bin>`_, although some are overly complicated for generality).
More examples will be added over time to make this a sort of 'cookbook' of AaronTools Python scripts

Note that these scripts assume you have correctly installed AaronTools (see :doc:`install`) and configured the :doc:`../other_docs/job_templates` to allow for job submission to a local queue.

Optimization and Frequencies
----------------------------

Although the task of submitting optimization + frequency jobs can be readily handled using a BASH script (see :doc:`example_bash`), we include a Python version here for completeness.
Here we use ORCA as an example, but the script below would instead use Psi4 or Gaussian by simply changing the filename extension to :code:`.in` or :code:`.com`, respectfully!

The following script will submit wB97XD/def2-TZVP optimization and frequency jobs (requesting 8 cores/processors, a 12 hour walltime, and 12 GB of memory) on all XYZ files in the current directory:

.. literalinclude:: python/opt_all.py
   :language: python

This could be easily modified to use IUPAC names or SMILES.

.. _python_SAPT_calculations:

SAPT Calculations
-----------------
In :ref:`bash_SAPT_calculations` we built a script to run SAPT calculations on the parallel stacked benzene dimer as a function of horizontal and vertical displacements.
In that case, because we were using :code:`makeInput.py`, we had to rely on Psi4 automatically partitioning the dimer into fragments.
If more control is required over how the supermolecule is fragmented for SAPT computations, we need to build a Psi4 input file explicitly separating the molecule into componets.

This requires some small changes to how we build the geometry and theory objects.
First, we need to define the :code:`components` of :code:`Geometry` to be a list of the individual monomers.
Second, in the :code:`theory` object we need to use :code:`SAPTMethod` instead of :code:`Method`.
Finally, the :code:`charge` and :code:`multiplicity` need to be lists consisting of the charge/multiplicity for the whole system and each monomer.

For instance, the following will submit a Psi4 job to calcualte the SAPT0/jun-cc-pVDZ energy on a dimer (read from :code:`dimer.xyz`) but use the AaronTools function :py:meth:`AaronTools.geometry.Geometry.get_monomers` to separate the monomers:

.. literalinclude:: python/sapt.py
   :language: python
