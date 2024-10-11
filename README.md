# AaronTools Documentation 

This is the documentation for <a href="https://github.com/QChASM/AaronTools.py">AaronTools</a>.
Documentation is built using Sphinx.

Note that this documentation is using the latest version of AaronTools from GitHub!
The version of AaronTools installed via pip may be slightly behind.

## Usage

These pages can be found at <a href="https://aarontools.readthedocs.io">readthedocs</a>.

## Building Docs

Requirements (available via pip):

* sphinx
* autodoc
* furo (the theme)
* sphinx-copybutton

To update docs:
* Modify/add files in the source directory
* Modify docstrings in your local copy of AaronTools
* rebuild HTML by running the following in the main AaronTools-docs directory
```sh
make html
```
Once changes are pushed to the AaronTools-docs repository on GitHub, readthedocs should automatically copy over the contents of the build directory.
That is, RTD is no longer set up to rebuild the HTML.

