INI Files
=========
AaronTools provides INI configuration file parsing with ``AaronTools.config.Config("/path/to/config.ini")`` allowing one to cleanly pass information AaronTools needs.
This functionality is also used by `AaronJr <https://github.com/QChASM/AaronJr>`__.
Note that AaronJr development is not complete.

Built-in configuration defaults are provided in ``$QCHASM/AaronTools/config.ini`` and user-defined defaults can be put in ``$AARONLIB/config.ini`` to stream-line job-specific configuration files.

INI configuration format overview
---------------------------------

.. code-block:: 

	global_option = value
	
	[Section]
	foo = bar
	multiword option = multiword value
	
	[Other Section]
	hello = world

`See here for more info <https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`__


AaronJr also supports prefixing any option with a number corresponding to a step in the workflow. By doing so, that option will only be applied to a particular step. Eg:

.. code-block:: 
	
	[Section]
	option = value_default
	1 option = value_1

will use ``option = value_1`` for the first step of the workflow and use ``option=value_default`` for all other steps.
This is especially helpful when the workflow includes higher-level single points or when relaxing substituted components using a lower-level of theory prior to optimization.

Configuration sections and their options
----------------------------------------
[DEFAULT]
^^^^^^^^^
This is the global section, and option/value pairs are available in all sections.
The ``[DEFAULT]`` section header is optional as long as the global option/value pairs come at the top of the file.

Option descriptions:

* local_only - set to true to disable any features that utilize web APIs (e.g. fetching molecular structures from IUPAC names)
* name - a name for AaronTools to use for the structure/job; will default to the filename of the configuration file used without the ".ini" extension
* project - this can be set to help tag multiple config files as part of a single project; it doesn't really do anything concrete (like affecting file name conventions), but can be helpful for organization or when searching for groups of jobs.

[Geometry]
^^^^^^^^^^
This is the section used to import molecular structures.

Option descriptions:

* structure - loads the value as a :py:meth:`~AaronTools.geometry.Geometry()` object; the value can be a file name, a smiles string, or a subdirectory (using a subdirectory will import all structures in that location)
* constraints - comma-separated list of atom-index tuples; applied only for constrained optimizations (see :ref:`Job Types <Job Types>`)

This will constrain the 1-2 bond length, the 3-4-5 bond angle, and the 6-7-8-9 dihedral

.. code-block::
	
	constraints = (1, 2), (3, 4, 5), (6, 7, 8, 9)


Special options:

&call
"""""
This is used to apply :py:meth:`~AaronTools.geometry.Geometry()` methods to the imported structure(s).
Take care to use the same syntax you would if calling the method within a Python script when providing the arguments for the function call, eg: using quotes around atom indices since they should be passed as strings, capitalizing boolean values, etc.
This will set the 1-2-3-4 dihedral to 60-degrees and change atom 2 to Si.

.. code-block:: 
	
	structure = ethane.xyz
	&call:
	    structure.change_dihedral("1", "2", "3", "4", 60)
	    structure.change_element("2", "Si")

&for {name} in {iterator}
"""""""""""""""""""""""""
This is used to generate starting structures using a for loop; use a suffix on the `structure` key to distinguish the generated structures from one another.
The following will create structures corresponding to a H-C-C-H dihedral scan in 10-degree increments.
Note that we are changing the dihedral for ``structure.0`` to 0-degrees (just in case the dihedral for the structure in ``ethane.xyz`` is not equal to 0), so we iterate starting at 0 degrees.
Additionally, note that ``range(a, b, step)`` follows Python's builtin implementation of the ``range`` function, specifically it will iterate from ``a`` up to *but not including* ``b`` in increments of ``step``.
Finally, most Geometry() methods are implemented as in-place changes to the structure, so it will often be necessary to call ``copy()`` to get a separate structure to alter.

.. code-block:: 

	[Geometry]
	structure.0 = ethane.xyz
	&for i in range(0, 370, 10):
	    structure.i = structure.0.copy()
	    structure.i.change_dihedral("3", "1", "2", "6", i)


The following will create several structures, in which atom 4 (a carbon) will be changed to various other elements:

.. code-block:: 

	[Geometry]
	structure.C = hydrocarbon.xyz
	&for element in ['O', 'N', 'Si', 'P', 'S']:
	    structure.element = structure.C.copy()
	    structure.element.change_element("4", element, adjust_bonds=True, adjust_hydrogens=True)


[Theory]
^^^^^^^^
This section is used to specify options that will be used to define the level of theory requested in the input files built for computational software.

Option descriptions:

* charge - the charge of the structure
* multiplicity - the multiplicity of the structure
* method - the name of the DFT or ab initio method requested
* basis - basis set info - see :ref:`Basis Options <Basis Options>`
* ecp - ECP info - see :ref:`Basis Options <Basis Options>`
* temperature - the temperature in Kelvin
* solvent - the solvent name (defaults to gas)
* solvent model - the solvent model to use (unused if solvent=gas)

Other options can also be provided, depending on which computational software is to be used.
See :ref:`Software Specific Theory Options <Software Specific Theory Options>` for more info.

[Job]
^^^^^
This section is used to specify options that define the computational job, eg: what to compute, what software to use, resources to request, etc.
Not all of these options will need to be specified.
Check the template file used to build computational files.
Note that if you are using AaronJr, the ``type`` option will be defined for you if you decide to use one of our pre-built workflows.

Option descriptions:

* type - what kind of computation to run (optimization, frequencies, single-point, etc.) See :ref:`Job types <Job Types>` for more info.
* exec_type - the computational software to use ("gaussian", "orca", "psi4", "q-chem", "xtb", or "sqm")
* queue - the name of the queue to submit to
* memory - the amount of memory to request (eg: ``memory=4GB``)
* ppmem - the per-processor memory to request
* exec_memory - the amount of memory to tell the executable to use (only use if different from memory)
* procs - the number of processors to request
* ppn - the number of processes per node
* nodes - the number of nodes to request
* wall - the wall time to request

The ``procs`` and ``memory`` options also control the default memory and processors for the :doc:`/cls/makeInput` and :doc:`/cls/jobSubmit` command line scripts.

The user can add any other options they wish to be used when filling in job submission templates or execuatable templates. See :doc:`job_templates` for more information.

[HPC]
^^^^^
These options are used to define how to connect to the HPC and queuing system when submitting jobs.

Option descriptions:

* user - the user name used to login to the HPC
* host - the host name of the HPC
* transfer_host - if a different host name is used when transferring files, this option is available (defaults to the value of `host`)
* scratch_dir - the top of the user's scratch directory on the HPC
* queue_type - the type of queuing system used on the HPC (eg: PBS, SLURM, etc.)

[Substitution]
^^^^^^^^^^^^^^
This section is used to define the changes that will be made to a Geometry object when using AaronJr.
To quickly list what changes will be made to to generate the new structures, use the ``listChanges.py`` command-line script included with AaronTools.

Options:

* ``reopt = True`` to re-optimize the template structure or False to only add changed structures to the workflow (default is False)

Substitution requests are illustrated in the following examples:

Example 1: This creates two structures. One formed by replacing only the functional group at atom #1 with a methyl group, and one by replacing both functional groups at atom 1 and atom 2 with an ethyl group.

.. code-block:: 
	
	mySub1: 1 = Me
	mySub2: 1, 2 = Et


Example 2: This creates one structure, where a methyl group replaces groups at atoms 1 and 2 and an alcohol group at atom 3

.. code-block::
	
	mySub:
	    1, 2 = Me
	    3 = OH

Or equivalently (note the semicolon!):

.. code-block::
	
	mySub: 1,2=Me; 3=OH


You can also request combinations of substitutions:

.. code-block:: 

	&combinations:
	    1, 2 = H, Me, Et, iPr
	    3 = F, Cl, Br, I

The snippet above produces 16 structures: all combinations of replacing atoms 1 and 2 with H, Me, Et, or iPr groups and replacing atom 3 with F, Cl, Br, or I.
Combinations can also be used similar to a list:

.. code-block:: 

	&combinations:
	    1, 2 = H, Me, Et, iPr

is equivalent to 

.. code-block:: 
	
	H_H: 1, 2 = H
	Me_Me : 1, 2 = Me
	Et_Et: 1, 2 = Et
	iPr_iPr: 1, 2 = iPr


Allowed substituent forms:

* AARONLIB name (run ``substitute.py -ls`` at the command line to get a list of all available substituents or browse using ChimeraX with the SEQCROW plugin by navigating to "Tools > `Browse AaronTools Libraries <https://github.com/QChASM/SEQCROW/wiki/Browse-AaronTools-Libraries-Tool>`__" and clicking the "substituents" tab)
* {SMILES} with X in place of sub.end eg: ``{XOH}`` adds alcohol group, ``{X=NH}`` adds imine
* ``None`` will simply remove the fragment without adding a new substituent

[Mapping]
^^^^^^^^^
"Key atoms" are used to properly map the new ligand to the old ligand.
For transition metal centered systems, the key atoms would be the atoms of the ligand that coordinate with the metal center.
It may be helpful to look at some of the ligands provided in the AaronTools ligand library (You can browse the AARON and AaronTools libraries at with SEQCROW's `Browse AaronTools Libraries <https://github.com/QChASM/SEQCROW/wiki/Browse-AaronTools-Libraries-Tool>`__ tool) to see which atoms are defined as the key atoms for that ligand.

.. code-block:: 
	
	lig1: 1, 2 = S-BINAP

Replaces the ligand(s) with key atoms 1 and 2 with the bidentate S-BINAP ligand.
Note that the order of key atoms matters, as AaronTools will attempt to place the first key atom in the ligand template file on the first listed key atom.
Though it doesn't really matter with S-BINAP, since it it C\ :sub:`2`\-symmetric.
If the order were swapped (i.e. ``lig1: 2, 1 = S-BINAP``), the S-BINAP ligand would be mounted in the opposite orientation.
This can be more complex with higher denticity ligands.

For multiple mappings:

.. code-block:: 

	lig1:
	    1 = PPh3
	    2 = PPh3
	lig2:
	    1 = XPhos
	    2 = XPhos

Or equivalently (note the semicolon!):

.. code-block:: 

	lig1: 1=PPh3; 2=PPh3
	lig2: 1=XPhos; 2=XPhos

Replaces the ligand(s) with key atoms 1 and 2 with two monodentate PPh3 ligands (one at atom 1 and one at atom 2) to form the ``lig1`` structure. Does similarly with XPhos to form the ``lig2`` structure.

Substitutions and Mappings in the same config file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Structures are generated by combinatorially applying each substitution with each mapping. By default, the original template structure is not optimized again. Use the `reopt` option in either the [Substitution] or [Mapping] section to reoptimize the template structure.

The following will generate four structures (original, sub1 only, lig1 only, sub1+lig1):

.. code-block:: 

	[Substitution]
	reopt=True
	sub1: 1,2=Me, 3=Cl
	
	[Mapping]
	lig1: 6,7=S-BINAP


This next example will generate eight structures (sub1 only, sub2 only, lig1 only, lig2 only, sub1+lig1, sub2+lig1, sub1+lig2, sub2+lig2):

.. code-block:: 

	[Substitution]
	sub1: 1,2 = Me
	sub2: 1,2 = Et
	
	[Mapping]
	lig1: 6,7=S-BINAP
	lig2: 6,7=R-BINAP


Using functions
---------------
Complex interpolation of the configuration file is provided to simplify configuration. For example, consider one wants to always request 2GB of memory for every processor requested on the HPC. In the user's default configuration file, the memory option is defined as follows:

.. code-block:: 

	# snippet from $AARONLIB/config.ini
	[HPC]
	memory = %{ $procs * 2 }GB

Now, we simply indicate the number of processors we need for our specific jobs

.. code-block:: 

	# snippet from really_small_job.ini
	[HPC]
	procs = 1
	
	# snippet from much_bigger_job.ini
	[HPC]
	procs = 48

When using ``really_small_job.ini``, ``memory = 2GB``. When using ``much_bigger_job.ini``, ``memory = 96GB``.

To refer to values from other sections, use ``$section:key``

.. code-block:: 

	[Job]
	temperature = 298
	
	[HPC]
	exec_options = -temp %{ $Job:temperature }


Software Specific Theory Options
--------------------------------
Gaussian
^^^^^^^^
Gaussian has the following options:

* link0
* route
* end_of_file
* comments

Route keywords should be separated onto different lines.
Options for route keywords should follow the keyword, separated by commas. For example:

.. code-block:: 

	route = pop NBORead, NBO7
	        DensityFit


will add ``pop=(NBORead,NBO7) DensityFit`` to the route, with any additional ``pop`` from the job type being added. 

Link0 keywords use the same format as route options, though the "%" is removed from the Link 0 command:

.. code-block:: 
	
	link0 = Save
	        LindaWorkers hamlet:4, ophelia:4


end_of_file adds lines to the end of the file (*e.g.* for NBORead). Multiple lines can be added.

.. code-block:: 
	
	end_of_file = $nbo RESONANCE NBOSUM E2PERT=0.0 NLMO BNDIDX $end


The format for comments is identical to the format of end_of_line.

ORCA
^^^^
ORCA has the following options:

* simple
* blocks
* comments

Simple input keywords and comments should be on separate lines. For example:

.. code-block:: 

	simple = TightSCF
	         Split-RI-J


Blocks should be separated onto different lines. Options are separated by commas. The first item in each block is used as the block name, though "%" should be omitted. For example:

.. code-block:: 

	blocks = cpcm epsilon 80.0, refrac 1.0, rsolv 1.3
	         scf SOSCFStart 0.00033


will add

.. code-block:: 

	%cpcm
	    epsilon 80.0
	    refrac 1.0
	    rsolv 1.3
	end
	%scf
	    SOSCFStart 0.00033
	end


to ORCA input files.

Psi4
^^^^
Psi4 has the following options:

* settings
* before_molecule
* before_job
* after_job
* molecule
* job
* optking
* comments

Settings, job, optking, and molecule options should be on separate lines. The setting or function comes first, followed by an option or value. For job, additional options can be added by separating individual options with commas. For example:

.. code-block:: 

	settings = reference uhf
	           diag_method olsen
	           ex_level 2
	molecule = no_com
	           no_reorient
	job = frequencies return_wfn=True, dertype=energy


before_molecule, before_job, and after_job can be used to add lines in difference places in the input file. For example:

.. code-block:: 

	before_job = print("AaronTools is cool")
	             activate(auto_fragments())


comments uses the same format as before_molecule, etc., though the "#" should be omitted.

Crest and xtb
^^^^^^^^^^^^^

* gfn - The GFN version to use (default = 2)
* cmdline - A string containing any other desired command line options (e.g.: ``cmdline = --esp --opt extreme``. These will be appended to the command line options built from the [Theory] section options (temperature, solvent, charge, multiplicity, etc.), so it is possible to override automatically-generated options.

Basis Options
-------------
Basis sets and effective core potentials can be specified with the ``basis`` and ``ecp`` options, respectively.
By default, basis sets will by used for all elements, and ECP's will only apply to d-block elements. The simplest basis specification is

.. code-block:: 

	basis = def2-SVP

This will use def2-SVP for all elements, and no ECP will be used. A list of elements (space-separated) can precede a basis name. An exclamation point can be used to exclude an element from a basis. For example:

.. code-block:: 

	basis =  H cc-pvqz
	        !H aug-cc-pvqz

will use cc-pVQZ for hydrogen and aug-cc-pVQZ for all other elements. As a shortcut, "tm" and "all" can be used to specify d-block elements and all elements, respectively.

Auxiliary basis sets can be employed by adding ``aux <auxiliary type>`` before the basis name:

.. code-block:: 

	basis = aux C cc-pVTZ


ORCA auxiliary basis types are C, J, JK, CABS, and OptRI CABS. Psi4 auxiliary basis types are JK and RI.

For external basis sets, the path to the basis set file can come after the basis set name. The path cannot include spaces, and the file must be compatible with the program you are using.

.. code-block:: 

	basis = def2-SVPD /home/CoolUser/basis_sets/def2svpd.gbs


ECP's use the same format, though auxiliary type will be ignored: 

.. code-block:: 

	ecp = Ir LANL2DZ

ECP's will not be printed to Psi4 input files, as Psi4 expects ECP's to be included in the basis set definition. 

Atom Types
----------
Symbols for dummy atoms can be defined in config files.
By default, X is used for dummy atoms.

.. code-block::

    [AtomTypes]
    dummy=X Du

This sets the symbols "X" and "Du" to be considered dummy atoms.
