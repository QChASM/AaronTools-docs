Converting Z-Matrices to Cartesian Coordinates
==============================================

AaronTools works almost exclusively with Cartesian coordinates.
However, some quantum chemistry codes (e.g. CFOUR) require molecular specification in terms of Z-matrices.
While tools are available to automatically generate Z-matrices, constructing Z-matrices that honor molecular symmetry typically requires their construction by hand.
This is a somewhat tedious process, and one often needs to check the final Z-matrix to ensure that the correct structure has been constructed.
Strangely, there seem to be limited tools available that will convert a general Z-matrix (or a CFOUR-style ZMAT file) to Cartesian coordinates.

To provide such a tool, and to demonstrate the utility of AaronTools, below we describe a simple ZMAT2XYZ converter

ZMAT Format
-----------
First, below is an example ZMAT file for acetone suitable for running an optimization in CFOUR:

.. code-block::

        Geometry optimization of acetone
        C
        O 1 r1*
        C 1 r2* 2 a2*
        C 1 r2* 2 a2* 3 D180
        H 3 r3* 1 a3* 2 D0
        H 3 r4* 1 a4* 2 d4*
        H 3 r4* 1 a4* 2 nd4*
        H 4 r3* 1 a3* 2 D0
        H 4 r4* 1 a4* 2 d4*
        H 4 r4* 1 a4* 2 nd4*
        
        r1=1.216
        r2=1.516
        r3=1.093
        r4=1.093
        a2=121.9
        a3=109.9
        a4=109.9
        d4=121.0
        nd4=-121.0
        D0=0.0
        D180=180.0
        
        *ACES2(CALC=MP2,BASIS=PVDZ)


We will read the Z-matrix and variables and then construct the corresponding molecule using AaronTools functions.


Reading ZMAT file
-----------------
The Python below will read the Z-matrix (removing the stars) and variable definitions (stored as a dictionary)
from a file called ZMAT as shown above.

.. code-block:: python

        from AaronTools.geometry import Geometry
        from AaronTools.atoms import Atom
        import numpy as np

        f = open('ZMAT', 'r')
        comment = f.readline()
        
        # start with empty geometry
        geom = Geometry([])
        geom.comment = comment.strip()
        
        # read z-matrix
        zmat = ""
        line = f.readline()
        while line.strip():
            line = line.replace("*","") # remove stars from optimized vars
            zmat += line
            line = f.readline()
        
        # read variables and build dict
        vars = {}
        line = f.readline().strip()
        while line:
            line = line.replace(" ","") # strip white space
            line_items = line.split("=")
            vars[line_items[0]] = float(line_items[1])
            line = f.readline().strip()


Converting Z-Matrix to Cartesian Coordinates
--------------------------------------------
With the Z-matrix definition now saved as `zmat` and the corresponding variables as the 
dictionary `vars`, the following Python code will build a new :py:meth:`AaronTools.geometry.Geometry`
object with the corresponding coordinates:

.. code-block:: python

        # loop over lines in zmat and build molecule
        for line in zmat.splitlines():
            line_items = line.split()
        
            # place atom in random spot to avoid co-linear atoms
            geom += [Atom(element=line_items[0], coords=np.random.random_sample(3))]
            a0 = geom.atoms[-1] # new atom
            
            # set distance
            if len(line_items) > 1:
                a1 = geom.atoms[int(line_items[1]) - 1]
                dist = vars[line_items[2]]
                geom.change_distance(a0, a1, dist=dist, fix=2, as_group=False)
                
            # set angle
            if len(line_items) > 3:
                a2 = geom.atoms[int(line_items[3]) - 1]
                angle = vars[line_items[4]]
                # note that change_angle uses radians by default
                geom.change_angle(a0, a1, a2, angle, radians=False, fix=3, as_group=False)
                      
            # set dihedral
            if len(line_items) > 5:
                a3 = geom.atoms[int(line_items[5]) - 1]
                dihedral = vars[line_items[6]]
                geom.change_dihedral(a0, a1, a2, a3, dihedral, fix=4, as_group=False)
    
For a given atom, we start by placing that atom in a random position to avoid accidentally having co-linear atoms.
We then use :py:meth:`AaronTools.geometry.Geometry.change_distance`, :py:meth:`AaronTools.geometry.Geometry.change_angle`, and :py:meth:`AaronTools.geometry.Geometry.change_dihedral` to set the distance, angle, and dihedral values as specified in the Z-matrix, taking care to move only the newly added atom.
That's it!

For completeness, we can also remove any dummy atoms (X) and then center and place the molecule in a reasonable orientation, then print the resulting coordinates in XYZ format.
Putting this all together, we have a simple little ZMAT to XYZ converter:


.. code-block:: python

        from AaronTools.geometry import Geometry
        from AaronTools.atoms import Atom
        import numpy as np

        f = open('ZMAT', 'r')
        comment = f.readline()

        # start with empty geometry
        geom = Geometry([])
        geom.comment = comment.strip()
        
        # read z-matrix
        zmat = ""
        line = f.readline()
        while line.strip():
            line = line.replace("*","") # remove stars from optimized vars
            zmat += line
            line = f.readline()
        
        # read variables and build dict
        vars = {}
        line = f.readline().strip()
        while line:
            line = line.replace(" ","") # strip white space
            line_items = line.split("=")
            vars[line_items[0]] = float(line_items[1])
            line = f.readline().strip()

        # loop over lines in zmat and build molecule
        for line in zmat.splitlines():
            line_items = line.split()
        
            # place atom in random spot to avoid co-linear atoms
            geom += [Atom(element=line_items[0], coords=np.random.random_sample(3))]
            a0 = geom.atoms[-1] # new atom
            
            # set distance
            if len(line_items) > 1:
                a1 = geom.atoms[int(line_items[1]) - 1]
                dist = vars[line_items[2]]
                geom.change_distance(a0, a1, dist=dist, fix=2, as_group=False)
                
            # set angle
            if len(line_items) > 3:
                a2 = geom.atoms[int(line_items[3]) - 1]
                angle = vars[line_items[4]]
                # note that change_angle uses radians by default
                geom.change_angle(a0, a1, a2, angle, radians=False, fix=3, as_group=False)
                      
            # set dihedral
            if len(line_items) > 5:
                a3 = geom.atoms[int(line_items[5]) - 1]
                dihedral = vars[line_items[6]]
                geom.change_dihedral(a0, a1, a2, a3, dihedral, fix=4, as_group=False)

        # remove any dummy atoms
        try:
            geom -= geom.find('X')
        except:
            pass
            
        # move to COM
        geom.coord_shift(-geom.COM())
        
        # orient (close) to principle axes
        moments, axes = geom.get_principle_axes()
        geom.coords @= axes
        
        print(geom)


