Coding with :code:`FileReader` objects
======================================

Here, you will find tutorials and explanations for using AaronTools'
functions, classes, and subroutines pertaining to our object for reading
files: :py:meth:`AaronTools.fileIO.FileReader`.


Creation
--------

A :code:`FileReader` object can be created by passing the path
to a file. To begin, let's import :code:`FileReader`:

.. code-block:: python

    from AaronTools.fileIO import FileReader
    
    fr = FileReader("benzene.log")

The file "benzene.log" will be read as a Gaussian output file
because of the .log extension.
Creating a :code:`Geometry` from this :code:`FileReader` is as
simple as passing it to Geometry:

.. code-block:: python

    from AaronTools.geometry import Geometry
    
    geom = Geometry(fr)

If the file has an unexpected extension, we should specify the format
for AaronTools:

.. code-block:: python

    fr = FileReader(("benzene.gout", "log", None))

Here, we've replaced the filename with a tuple containing

#. the path to the file
#. the format AaronTools should read the file as
#. the file content

Because we haven't read anything from the file yet,
we specify None in our tuple.
The content can also be a string containing the contents of a
file of the specified format or a file-like object (e.g. :code:`sys.stdin`).

Below is a table containing AaronTools' expectations for file extensions:

.. list-table:: Expected File Extensions
    :header-rows: 1

    * - file type
      - extension
    * - Gaussian input
      - com or gjf
    * - Gaussian output
      - log
    * - ORCA output
      - out
    * - XYZ
      - xyz
    * - structure data file
      - sd or mol
    * - Psi4 output
      - dat or out


Getting More Information
------------------------

:code:`FileReader` initialization accepts two keywords:
:code:`get_all` and :code:`just_geom`.
Let's look at what those do.

Multiple Structures
*******************

The :code:`get_all` keyword tells :code:`FileReader` to
store all the structures it finds while reading the
file (e.g. all steps in an optimization or an XYZ trajectory).
These structures are stored in the FileReader's all_geom attribute.
This will be a list of dictionaries, with one of the keys being atoms
and the other being either comment or data, depending on the file format.
The data key is used for QM output files, and stores whatever data has
been parsed at the time the corresponding structure was read.
The comment key is used for files that do not have computed data
to parse (e.g., XYZ or Mol files). With :code:`get_all=False`,
the :code:`FileReader`'s only structure will be the last one in the file.

Below is sample code for turning each structure in a
:code:`FileReader` into a :code:`Geometry`:

.. code-block:: python

    from AaronTools.atoms import Atom
    from AaronTools.geometry import Geometry
    from AaronTools.fileIO import FileReader
    
    fr = FileReader('benzene.log', get_all=True)
    
    geom_list = []
    for struc in fr.all_geom:
        geom_list.append(Geometry(struc["atoms"]))
    
Below is similar code for reading an XYZ file with multiple structures
that will also copy over the comment information from the original XYZ entry

.. code-block:: python

    from AaronTools.atoms import Atom
    from AaronTools.geometry import Geometry
    from AaronTools.fileIO import FileReader
    
    fr = FileReader('molecules.xyz', get_all=True)
    
    geom_list = []
    for struc in fr.all_geom:
        geom_list.append(Geometry(struc["atoms"], comment=struc["comment"]))
    

Calculation Information

The :code:`just_geom` keyword controls whether the
:code:`FileReader` grabs more than the file's structure.
Additional information will be stored as a dictionary in the
:code:`FileReader`'s other attribute.
This data can also be accessed by using the :code:`FileReader`
as if it was a dictionary (`i.e.` :code:`fr["energy"]` instead
of :code:`fr.other["energy"]`).
A list of dictionary keys, what they are, and which of our
file parsers can grab them can be found on the
`this page <../api/filereader.html#filereader-keys-for-various-output-files>`_.
