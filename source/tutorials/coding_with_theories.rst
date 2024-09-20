Coding with :code:`Theory` Objects
==================================

:py:meth:`AaronTools.theory.Theory` keeps much of the code for
writing quantum chemistry input files similar across different software packages.
Here, we will cover the basics of creating and using a Theory.

Building a Basic Input File
---------------------------
The following will build a Gaussian input file called `benzene.com` that
does a B3LYP/def2-SVP optimization of the coordinates in `benzene.xyz`
followed by the computation of vibrational frequencies

.. code-block:: python

    from AaronTools.geometry import Geometry
    from AaronTools.theory import *
    
    geom = Geometry('benzene.xyz')
    
    method = Theory(
        method="B3LYP", 
        basis="def2-SVP", 
        job_type=[OptimizationJob(), FrequencyJob()]
    )
    outfile = "benzene.com"
    geom.write(outfile=outfile, theory=method)


By changing the extension of the file being written, the corresponding format
and keyword changes are automatically handled.

For example, the example below will write (essentially) equivalent input files
for Gaussian, ORCA, and Psi4.

.. code-block:: python

    from AaronTools.geometry import Geometry
    from AaronTools.theory import *
    
    geom = Geometry('benzene.xyz')
    
    method = Theory(
        method="B3LYP", 
        basis="def2-SVP", 
        job_type=[OptimizationJob(), FrequencyJob()]
    )
    for outfile in ["gaussian.com", "ORCA.inp", "psi4.in"]:
        geom.write(outfile=outfile, theory=method)

Below, we discuss more detail about working with Theory objects.

Creation
--------

Several objects or variables must be passed to Theory to make it usable.
Each of the necessary objects are found in the AaronTools.theory package.
We'll briefly cover each of these.

Method Class
------------

:py:meth:`AaronTools.theory.Method` is used to keep method keywords
the same across different formats.
As an example:

.. code-block:: python

    from AaronTools.theory import Method
    
    pbe0 = Method("PBE0")

When used with a Gaussian input file, this :code:`Method` will use the
Gaussian keyword for PBE0 (PBE1PBE).

Method also takes a :code:`is_semiempirical` argument:

.. code-block:: python

    rm1 = Method("RM1", is_semiempirical=True)

For Gaussian and ORCA input files, using a semi-empirical method
will cause basis set information to be omitted.

SAPTMethod
**********

:py:meth:`AaronTools.theory.SAPTMethod` is a subclass of :code:`Method` 
that is specific for SAPT jobs. When used to make a Psi4 input file,
the molecule will be split into monomers, which are specified by the
components attribute of the Geometry instance.

.. code-block:: python

    sapt0 = SAPTMethod("sapt0")

Basis Sets

The :py:meth:`AaronTools.theory.BasisSet` object is a collection of
:py:meth:`AaronTools.theory.Basis` and :py:meth:`AaronTools.theory.ECP` objects.

.. code-block:: python

    from AaronTools.theory import Basis, ECP, BasisSet
    from AaronTools.finders import AnyTransitionMetal, AnyNonTransitionMetal
    
    basis = BasisSet(
        [
            Basis("cc-pVTZ", AnyNonTransitionMetal()), 
            Basis("cc-pVTZ", AnyNonTransitionMetal(), aux_type='C'), 
            Basis("cc-pVTZ-PP", AnyTransitionMetal()),
            Basis("cc-pVTZ-PP", AnyTransitionMetal(), aux_type='C')
        ], 
        [ECP("SK-MCDHF-RSC")]
    )

The second argument given to each :code:`Basis` determines which
elements that basis applies to. By default, a Basis applies to all elements.
An :code:`ECP` applies to any transition metal.
These elements will be overridden if another argument is supplied when
creating an :code:`ECP` or :code:`Basis` (`i.e.` list of elements or
:py:meth:`AaronTools.finders.Finders`).

The :code:`aux_type` keyword is used for ORCA and Psi4 input files to specify
auxiliary basis sets.
A list of elements or an appropriate :code:`Finder` that use that basis set can
be given to a :code:`Basis` or :code:`ECP`.

Empirical Dispersion
--------------------

:py:meth:`AaronTools.theory.emp_dispersion.EmpiricalDispersion` keeps specifying dispersion
corrections consistent across different formats.

.. code-block:: python

    from AaronTools.theory import EmpiricalDispersion
    
    disp = EmpiricalDispersion("Grimme D2")
    
    The following are equivalent:
    
    disp = EmpiricalDispersion("Grimme D2")
    disp = EmpiricalDispersion("GD2")
    disp = EmpiricalDispersion("D2")
    disp = EmpiricalDispersion("-D2")

Some dispersion methods are not available in all QM software programs.
Check the :code:`get_gaussian`, :code:`get_orca`, etc. methods of the
:code:`EmpiricalDispersion` class (or the respective manuals) for
acceptable dispersion methods.

Integration Grid
----------------

As with other objects in the :code:`AaronTools.theory` package, the
:py:meth:`AaronTools.theory.IntegrationGrid` object is a way to
specify grids in a similar manner across different file formats.

It's important to note that different programs use different types of grids.
This, combined with varied grid pruning algorithms, mean that grids will
usually have to be approximated if you use a keyword from one program
to make an input file for a different program.

.. code-block:: python

    from AaronTools.theory import IntegrationGrid
    
    grid = IntegrationGrid("SuperFineGrid")

Gaussian, ORCA, and Psi4 all have different ways of specifying integration grids.
Gaussian and ORCA have grid keywords.
When using an ORCA grid keyword to write a Gaussian input file,
:code:`IntegrationGrid` will try to approximate the ORCA grid's density.
Psi4 specifies grid density by supplying a number of radial and angular points.
Gaussian allows a similar specification.
These can be specified as a string of the format :code:`"(radial, angular)"`.
As an example,

.. code-block::

    grid = IntegrationGrid("(99, 590)")

This grid can be used with Gaussian and Psi4, and should give similar results
(down to grid pruning and other algorithmic differences).
If you're going to write and ORCA input file with this grid,
the number of radial points is set indirectly with the :code:`IntAcc` option.
:code:`IntAcc` will be set for the number of radial points in the 2nd row
of the periodic table.

Job Types
---------

There are six job types in the theory package:

* :py:meth:`AaronTools.theory.job_types.OptimizationJob`
* :py:meth:`AaronTools.theory.job_types.FrequencyJob`
* :py:meth:`AaronTools.theory.job_types.SinglePointJob`
* :py:meth:`AaronTools.theory.job_types.ForceJob`
* :py:meth:`AaronTools.theory.job_types.ConformerSearchJob`
* :py:meth:`AaronTools.theory.job_types.TDDFTJob`

A single :code:`JobType` can be given to a Theory.
If multiple :code:`JobType` instances are given as list,
the job-related information will appear in the order it appears
in the list. For example:

.. code-block:: python

    jobs = [FrequencyJob(), OptimizationJob()]

A Psi4 input file that uses this list will specify frequency before optimize,
but many programs are not sensitive to the order these jobs
will appear in the input file. 

Other Options
-------------

* charge - overall charge
* multiplicity - multiplicity
* processors - allocated cores
* memory - allocated RAM

When writing an input file, additional keywords can be passed to
:py:meth:`AaronTools.geometry.Geometry.write` that specify any other options.
The keywords for the dictionary are listed in :doc:`../api/theory_parameters`.

Examples
--------

Below are examples of writing roughly equivalent input files for Gaussian, ORCA, and Psi4.

.. code-block:: python

    from AaronTools.geometry import Geometry
    from AaronTools.theory import *
    
    geom = Geometry('tnt.xyz')
    
    fun = Method("B3LYP")
    basis_set = BasisSet([Basis("def2-SVP")])
    int_grid = IntegrationGrid("(99, 590)")
    disp = EmpiricalDispersion("D2")
    
    jobs = [OptimizationJob(), FrequencyJob()]
    
    b3lyp_def2svp = Theory(
        method=fun, 
        basis=basis_set, 
        grid=int_grid, 
        empirical_dispersion=disp, 
        job_type=jobs, 
    )
    
    geom.write(
        outfile="tnt_freq.com", 
        theory=b3lyp_def2svp, 
        GAUSSIAN_ROUTE={'freq':['HPModes', 'NoRaman']}
    )
    
    geom.write(
        outfile="tnt_freq.inp", 
        theory=b3lyp_def2svp
    )
    
    geom.write(
        outfile="tnt_freq.in", 
        theory=b3lyp_def2svp
    )

Note that :code:`Method`, :code:`BasisSet`, :code:`IntegrationGrid`,
and :code:`EmpiricalDispersion` objects can be created automatically
when creating a :code:`Theory` object just by passing strings:

.. code-block:: python

    b3lyp_def2svp = Theory(
        method="B3LYP", 
        basis="def2-SVP", 
        grid="(99, 590)", 
        empirical_dispersion="D2", 
        job_type=jobs, 
    )
