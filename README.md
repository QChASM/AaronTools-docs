# AaronTools Documentation 

This is the documentation for <a href="https://github.com/QChASM/AaronTools.py">AaronTools</a>.
Documentation is built using Sphinx.

## Usage

These pages can be found at readthedocs (coming soon<sup>TM</sup>).

## Building Docs

Requirements (available via pip):

* sphinx
* autodoc
* furo (the theme)

You make also need to run `sphinx-quickstart` to create the `make` script.
Ensure you separate source from build during the quickstart.

```sh
make html
```

## Documenting Things
Read a sphinx tutorial. Basically, the files people modify are all in the source directory. Autodoc automatically adds docstrings if you ask it to. 
