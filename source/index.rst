.. AaronTools documentation master file, created by
   sphinx-quickstart on Fri Mar 24 14:26:16 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the AaronTools Documentation!
========================================

AaronTools is a Python module for facilitating many tasks in computational quantum chemistry workflows


.. toctree::
    :maxdepth: 1
    :caption: Pages:
    
    tutorials/install
    tutorials/tut_list
    cls/list
    other_docs/configuration
    api/api
    advanced/advanced

Note that this documentation corresponds to the version of AaronTools on GitHub.
The version available via :code:`pip` is usually slightly behind.

Citation
========
If you use the Python AaronTools, please cite:

    V. M. Ingman, A. J. Schaefer, L. R. Andreola, and S. E. Wheeler
    "QChASM: Quantum Chemistry Automation and Structure Manipulation"
    |wires|_


Overview of Features
====================

These are some of the more popular features in AaronTools, with links to the
relevant command line scripts or Python API.

Data can be processed from several popular quantum chemsitry software packages including
Gaussian, ORCA, Psi4, and xTB.

Steric Parameters
-----------------

Sterimol parameters
*******************

* :doc:`cls/substituentSterimol`
* :doc:`cls/ligandSterimol`
* :py:meth:`AaronTools.substituent.Substituent.sterimol`
* :py:meth:`AaronTools.component.Component.sterimol`
* :py:meth:`AaronTools.geometry.Geometry.sterimol`

Buried Volume
*************

* :doc:`cls/percentVolumeBuried`
* :py:meth:`AaronTools.geometry.Geometry.percent_buried_volume`

Steric Maps
***********

* :doc:`cls/stericMap`
* :py:meth:`AaronTools.geometry.Geometry.steric_map`

Ligand Solid Angles
*******************

* :doc:`cls/solidAngle`
* :py:meth:`AaronTools.component.Component.solid_angle`


Ligand Cone Angles
*******************

* :doc:`cls/coneAngle`
* :py:meth:`AaronTools.component.Component.cone_angle`

Structure Operations
--------------------

Add/Modify Substituents
***********************

* :doc:`cls/substitute`
* :doc:`cls/multiSubstitute`
* :py:meth:`AaronTools.geometry.Geometry.substitute`

Swap Ligands
************

* :doc:`cls/mapLigand`
* :py:meth:`AaronTools.geometry.Geometry.map_ligand`

Fetch by Name/SMILES
********************

* :doc:`cls/fetchMolecule`
* :py:meth:`AaronTools.geometry.Geometry.from_string`

Generate Coordination Complexes
*******************************

* :doc:`cls/getCoordinationComplexes`
* :py:meth:`AaronTools.geometry.Geometry.get_coordination_complexes`

Quantum Chemistry Setup and Processing
--------------------------------------

Making Input Files
******************

* :doc:`cls/makeInput`
* :doc:`cls/makeCrestInput`
* :py:meth:`AaronTools.geometry.Geometry.write`
* :py:meth:`AaronTools.theory.Theory`

Parsing Data
************

* :doc:`cls/printInfo`
* :py:meth:`AaronTools.fileIO.FileReader`

Free Energy (RRHO, Quasi-RRHO, Quasi-Harmonic)
**********************************************

* :doc:`cls/grabThermo`
* :py:meth:`AaronTools.comp_output.CompOutput`

Vibrational Frequency Analysis
******************************

* :doc:`cls/plotIR`
* :doc:`cls/plotAverageIR`
* :doc:`cls/follow`
* :doc:`cls/printFreq`
* :py:meth:`AaronTools.spectra.Frequency`

Valence Excitations
*******************

* :doc:`cls/plotUVVis`
* :doc:`cls/plotAverageUVVis`
* :py:meth:`AaronTools.spectra.ValenceExcitations`

Orbital Data
************

* :doc:`cls/printCube`
* :py:meth:`AaronTools.orbitals.Orbitals`


ChimeraX Plugin
===============

The majority of these features are also available with a graphical interface
in the `SEQCROW plugin <https://cxtoolshed.rbvi.ucsf.edu/apps/seqcrow>`_ for
`ChimeraX <https://www.cgl.ucsf.edu/chimerax/>`_.

Perl
======
A Perl implementation of AaronTools is also available `here <https://github.com/QChASM/AaronTools>`_.
However, users are strongly urged to use the Python version since it
has far more powerful features and, unlike the Perl version, will continue
to be developed and supported.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _wires: http://dx.doi.org/10.1002/wcms.1510
.. |wires| replace:: *WIREs Comp. Mol. Sci.* **11**, e1510 (2021)
