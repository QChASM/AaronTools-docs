``FileReader`` class
======================================

Any data parsed from by a ``FileReader`` can be accessed much like a dictiory (*i.e.* ``some_filereader["energy"]``).
A nearly complete list of keys for various file types is at the bottom of this page.

.. autoclass:: AaronTools.fileIO.FileReader
    :special-members: __init__
    :members:



``FileReader`` keys for various output files
*********************************************

CREST output
--------------

.. csv-table::
    :file: crest-filereader.csv
    :delim: ;
    :header: "key", "description"
    

Gaussian Output
---------------

.. csv-table::
    :file: gaussian-filereader.csv
    :delim: ;
    :header: "key", "description"
    

Gaussian Formatted Checkpoint File
------------------------------------
The keys for .fchk files are mostly the same as the labels in the .fchk file.
No string entries are parsed from .fchk files.
There is also an ``orbitals`` key with an ``Orbitals`` object. 


NBO Output
----------

.. csv-table::
    :file: nbo-filereader.csv
    :delim: ;
    :header: "key", "description"
    
    
ORCA Output
------------

.. csv-table::
    :file: orca-filereader.csv
    :delim: ;
    :header: "key", "description"
    
    
Psi4 Output
------------

.. csv-table::
    :file: psi4-filereader.csv
    :delim: ;
    :header: "key", "description"
    
    
Q-Chem Output
-------------

.. csv-table::
    :file: qchem-filereader.csv
    :delim: ;
    :header: "key", "description"
    
    
SQM Output
----------

.. csv-table::
    :file: sqm-filereader.csv
    :delim: ;
    :header: "key", "description"
    
    
xTB Output
----------

.. csv-table::
    :file: xtb-filereader.csv
    :delim: ;
    :header: "key", "description"
    
    