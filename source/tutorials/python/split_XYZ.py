#!/usr/bin/env python3
# split a multistructure XYZ file (e.g. from Crest) into individual XYZ files

from AaronTools.geometry import Geometry
from AaronTools.fileIO import FileReader

fr = FileReader('crest_conformers.xyz', get_all=True)

# loop over conformers
for confnum, conf in enumerate(fr.all_geom):
    geom = Geometry(conf["atoms"])
    outfile = f"conf{confnum}.xyz"
    geom.write(outfile=outfile)

