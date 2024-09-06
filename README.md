# AaronTools Documentation 

This is the documentation for <a href="https://github.com/QChASM/AaronTools.py">AaronTools</a>.
Documentation is built using Sphinx.

## Usage

These pages can be found at <a href="https://aarontools.readthedocs.io">readthedocs</a>.

## Building Docs

Requirements (available via pip):

* sphinx
* autodoc
* furo (the theme)
* sphinx-copybutton

You make also need to run `sphinx-quickstart` to create the `make` script.
Ensure you separate source from build during the quickstart.

Modify/add files in the source directory and then rebuild the HTML with:
```sh
make html
```
Once changes are pushed to GitHub, readthedocs should automatically build the new docs!

## Documenting Things
Read a sphinx tutorial. Basically, the files people modify are all in the source directory. Autodoc automatically adds docstrings if you ask it to. 
