Coding with :code:`Theory` Objects
==================================

:py:meth:`AaronTools.theory.Theory` is used to designate computational options when building input files for different QM packages.
It is designed to keep much of the code for writing quantum chemistry input files similar across different software packages
to avoid having to dig into the nuances of the corresponding input file formats or worry 
about specific names for DFT functionals (e.g. PBE0 vs PBE1PBE or M06-2X vs M062X) or
basis sets (def2-TZVP vs def2tzvp) in different packages.

Here, we will cover the basics of creating and using a :code:`Theory` object to write
input files for popular QM packages.

To have a functional :code:`Theory` object, at a minimum you  need to define the :code:`method`, :code:`basis`
(unless using a semi-empirical method), and :code:`job_type`.

Optionally, you can also specify:

* charge - overall charge
* multiplicity - multiplicity
* processors - allocated cores
* memory - allocated RAM
* empirical_dispersion - Grimme D2, D3, etc.
* grid - integration grid

When writing an input file, additional keywords can be passed to
:py:meth:`AaronTools.geometry.Geometry.write` that specify any other options (often program-specific).
These keywords are described in :doc:`../api/theory_parameters`.
See `Additional Keywords`_.

For :code:`method`, :code:`basis`, :code:`job_type`, :code:`empirical_dispersion`, and :code:`grid`
you can either explicitly construct the corresponding object or provide a keyword and let :code:`Theory`
automatically construct the required object.

The latter approach is much simpler, but the former provides more control.
This control is most often needed for :code:`basis` (e.g. when using mixed basis sets or ECPs, etc).


Building Basic Input Files
--------------------------

As a first example, the following will build a Gaussian input file called :code:`benzene.com` that
does a B3LYP/def2-SVP optimization of the coordinates in :code:`benzene.xyz`
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

Note that the resulting Gaussian input file will use :code:`def2svp` for the basis set, even though we specified :code:`def2-SVP`.

Equivalently, we could have done the following, where we explicitly build :code:`Method` and :code:`BasisSet` objects:

.. code-block:: python

    from AaronTools.geometry import Geometry
    from AaronTools.theory import *
    
    geom = Geometry('benzene.xyz')
    
    method = Theory(
        method=Method("B3LYP"),
        basis=BasisSet("def2-SVP"), 
        job_type=[OptimizationJob(), FrequencyJob()]
    )
    outfile = "benzene.com"
    geom.write(outfile=outfile, theory=method)

If a molecule has a charge and multiplicity other than 0 and 1, we need to pass that to :code:`Theory`:

.. code-block:: python

    method = Theory(
        method="B3LYP", 
        charge=1,
        multiplicity=2,
        basis="def2-SVP", 
        job_type=[OptimizationJob(), FrequencyJob()]
    )

Similarly, if we want to use B3LYP-D3, instead of B3LYP, we can specify :code:`empirical_dispersion="D3"`

.. code-block:: python

    method = Theory(
        method="B3LYP", 
        charge=1,
        multiplicity=2,
        empirical_dispersion="D3",
        basis="def2-SVP", 
        job_type=[OptimizationJob(), FrequencyJob()]
    )

By changing the extension of the file being written, the corresponding format
and keyword changes (def2-svp vs def2svp, etc) are automatically handled.

For example, the example below will write (essentially) equivalent
input files for Gaussian, ORCA, and Psi4.

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


Job Types
^^^^^^^^^

There are six job types in the theory package:

* :py:meth:`AaronTools.theory.job_types.OptimizationJob`
* :py:meth:`AaronTools.theory.job_types.FrequencyJob`
* :py:meth:`AaronTools.theory.job_types.SinglePointJob`
* :py:meth:`AaronTools.theory.job_types.ForceJob`
* :py:meth:`AaronTools.theory.job_types.ConformerSearchJob`
* :py:meth:`AaronTools.theory.job_types.TDDFTJob`

A single :code:`JobType` can be given to a :code:`Theory`.
If multiple :code:`JobType` instances are given as list,
the job-related information will appear in the order it appears
in the list.
For example, above we used :code:`job_type=[OptimizationJob(), FrequencyJob()]`
to specify a geometry optimization followed by vibrational frequencies.

However, if we instead did

.. code-block:: python

    job_type = [FrequencyJob(), OptimizationJob()]

then any Psi4 input file constructed using the corresponding :code:`Theory` object will
request frequencies before the optimization.
Other programs are not sensitive to the order these jobs will appear in the input file. 

Many of these job types take additional arguments (click the links above to see the options).
For example, for a transition state optimization you need to specify :code:`OptimizationJob(transition_state=True)`.

Constrained Optimizations
=========================
If we want to do a constrained optimization, we need to do a little more work.
For example, suppose we have an AaronTools :code:`Geometry` (probably not benzene) called :code:`geom` and we want to write an input file
for an optimization with a constraint on the distance between atoms 1 and 4.
Constraints are passed to :code:`OptimizationJob()` as a dictionary, with the keys corresponding to the types of constraints (bonds, angles, torsions, etc).
Each entry in the dictionary is a list of lists of :code:`AaronTools Atoms`.
In our case, we are constraining a distance ('bond') so need to supply a list of a list of two atoms, whcih are most easily built using :code:`Geometry.find()`:

.. code-block:: python

    constraints = {}
    constraints["bonds"] = [geom.find("1,4")]

Now we can pass this constraints dictionary to :code:`OptimizationJob()`:

.. code-block:: python

    method = Theory(
        method="B3LYP", 
        basis="def2-SVP", 
        job_type=OptimizationJob(constraints=constraints)
    )

An input file written using this :code:`Theory` object will include this geometric constraint, formatted properly for the correspinding QM package.

To add more constraints we simply append more pairs (or triples for an angle, quadruples for a torsion, etc) to the corresponding
entry in the constraints dictionary.
The following (silly) example will constrain distances 1-4 and 7-11, angle 2-3-5, and torsion 1-2-3-4:

.. code-block:: python

    constraints = {}
    constraints["bonds"] = [geom.find("1,4"), geom.find("7,11")]
    constraints["angles"] = [geom.find("2,3,5")]
    constraints["torsions"] = [geom.find("1,2,3,4")]

    method = Theory(
        method="B3LYP", 
        basis="def2-SVP", 
        job_type=OptimizationJob(constraints=constraints)
    )


Finer Control
-------------

If you need more control over one or more of these objects you can explicitly define various objects and pass these to :code:`Theory`.
This is most likely to occur for :code:`BasisSet`, for example, when working with mixed basis sets and/or ECPs.

The various objects that can be passed to :code:`Theory` are discussed below.

Method Class
^^^^^^^^^^^^

:py:meth:`AaronTools.theory.Method` is used to keep method keywords
the same across different formats.
As an example:

.. code-block:: python

    from AaronTools.theory import Method
    
    pbe0 = Method("PBE0")

When used to write a Gaussian input file, this :code:`Method` will use the
Gaussian keyword for PBE0 (PBE1PBE).

Method also takes a :code:`is_semiempirical` argument:

.. code-block:: python

    rm1 = Method("RM1", is_semiempirical=True)

For Gaussian and ORCA input files, using a semi-empirical method
will cause basis set information to be omitted.

SAPTMethod
^^^^^^^^^^

:py:meth:`AaronTools.theory.SAPTMethod` is a subclass of :code:`Method` 
that is specific for SAPT jobs. When used to make a Psi4 input file,
the molecule will be split into monomers, which are specified by the
components attribute of the Geometry instance.

.. code-block:: python

    sapt0 = SAPTMethod("sapt0")

See :ref:`python_SAPT_calculations` for an example.

Basis Sets
^^^^^^^^^^

The :py:meth:`AaronTools.theory.BasisSet` object is a collection of
:py:meth:`AaronTools.theory.Basis` and (optionally) :py:meth:`AaronTools.theory.ECP` objects.

The second argument given to each :code:`Basis` determines which elements that basis applies to.
By default, a :code:`Basis` applies to all elements while an :code:`ECP` applies to any transition metal.

For example, suppose we have some Pt carbonyl complex. 
To build a :code:`BasisSet` object for a calculation in which we use LANL2DZ basis set
and ECP on Pt and 6-31G(d) on C and O, we could do

.. code-block:: python

    from AaronTools.theory import Basis, ECP, BasisSet
    basis = BasisSet(
        [
            Basis("6-31G(d)", ["C", "O"]),
            Basis("LANL2DZ", "Pt")
        ],
        [ECP("LANL2DZ")]
    )

Alternatively, we can use :doc:`../api/finders` to automatically build lists of elements:

.. code-block:: python

    from AaronTools.theory import Basis, ECP, BasisSet
    from AaronTools.finders import AnyTransitionMetal, AnyNonTransitionMetal
    
    basis = BasisSet(
        [
            Basis("6-31G(d)", AnyNonTransitionMetal()), 
            Basis("LANL2DZ", AnyTransitionMetal()),
        ], 
        [ECP("LANL2DZ")]
    )

Finally, the :code:`aux_type` keyword is used for ORCA and Psi4 input files to specify
auxiliary basis sets.


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

Any of these :code:`BasiSet` objects can then be passed to a :code:`Theory` object.
For example, the following will write a Gaussian input file :code:`TM_complex.com` for an optimization + frequency
job at the M06-2X/6-31G(d)/LANL2DZ level of theory for any transition metal complex in :code:`TM_complex.xyz`: 

.. code-block:: python

    from AaronTools.geometry import Geometry
    from AaronTools.theory import *
    from AaronTools.finders import AnyTransitionMetal, AnyNonTransitionMetal
    
    geom = Geometry('TM_complex.xyz')

    basis = BasisSet(
        [
            Basis("6-31G(d)", AnyNonTransitionMetal()), 
            Basis("LANL2DZ", AnyTransitionMetal()),
        ], 
        [ECP("LANL2DZ")]
    
    method = Theory(
        method="M062X", 
        basis=basis,
        job_type=[OptimizationJob(), FrequencyJob()]
    )
    outfile = "TM_complex.com"
    geom.write(outfile=outfile, theory=method)



Empirical Dispersion
--------------------

:py:meth:`AaronTools.theory.emp_dispersion.EmpiricalDispersion` keeps specifying dispersion
corrections consistent across different input file formats.

.. code-block:: python

    from AaronTools.theory import EmpiricalDispersion
    
    disp = EmpiricalDispersion("Grimme D2")
    
    # The following are equivalent:
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
This, combined with varied grid pruning algorithms, mean that getting exactly 
equivalent grids in two QM programs is nearly impossible.
If you use a keyword from one program to make an input file for a different program,
:code:`IntegrationGrid` will at least try to specify an equivalent grid.

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
If you're going to write an ORCA input file with this grid,
the number of radial points is set indirectly with the :code:`IntAcc` option.
:code:`IntAcc` will be set for the number of radial points in the 2nd row
of the periodic table.


Additional Keywords
-------------------
Additional program options are often program-specific and are passed to :py:meth:`AaronTools.geometry.Geometry.write` differently depending on the QM package and the location where the additional options are required.
These keywords are described in :doc:`../api/theory_parameters`.

For example, in `Constrained Optimizations`_ we added constraints using the :code:`constraints` option in :code:`OptimizationJob()`.
Alternatively, we can directly write data to the constraints section of a Gaussian input file using :code:`GAUSSIAN_CONSTRAINTS`.
For instance, we can write the constraints from `Constrained Optimizations`_ by modifying the :code:`geom.write` line:

.. code-block:: python

    geom.write(outfile=outfile, theory=method, GAUSSIAN_CONSTRAINTS = "B 1 4 F\nB 7 11 F\nA 1 2 3 F\nD 1 2 3 4 F")

The advantage of building a :code:`constraints` dictionary and passing that to :code:`OptimizationJob()` is that you can more easily switch to a different QM package.

Some of these additional keywords take a dictionary.
:code:`GAUSSIAN_ROUTE` provides a nice example.
As noted above, you can requiest a TS optimization by passing :code:`transition_state=True` to :code:`OptimizationJob()`.
However, what if you also want to include :code:`noeigen` as an option to :code:`opt`?
In other words, by using :code:`transition_state=True` the route section will include :code:`opt=(ts,CalcFC`), but we want to add :code:`noeigen` to the list of :code:`opt` options.
We can do this by defining a dictionary with key :code:`opt` and value :code:`noeigen` and :code:`noeigen` will automatically be added to the list of options under :code:`opt`:

.. code-block:: python

    route = {"opt": "noeigen"}
    geom.write(outfile=outfile, theory=method, GAUSSIAN_ROUTE=route)

For route entries with no options (e.g. :code:`nosym`) you simply provide the key but an empty value:

.. code-block:: python

    route = {"nosym": ""}
    geom.write(outfile=outfile, theory=method, GAUSSIAN_ROUTE=route)

