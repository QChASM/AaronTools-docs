# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'AaronTools'
copyright = '2023, V. M. Ingman, A. J. Schaefer, L. R. Andreola, and S. E. Wheeler'
author = 'V. M. Ingman, A. J. Schaefer, L. R. Andreola, and S. E. Wheeler'

# The full version, including alpha/beta/rc tags
release = '1.0b19'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    'sphinx_copybutton',
    'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# prefix for shell things that are copyable
copybutton_prompt_text = ">>> "

# raw html files
html_extra_path = [
    "googleeb034417e9c5a468.html",
]

# for multiline things
copybutton_line_continuation_character = "\\"

autodoc_default_options = {
    'exclude-members': 'get_matching_atoms',
    'member-order': 'bysource',
}

inheritance_node_attrs = {
    "fontsize": 12,
    "color": 'purple4',
    "fillcolor": "lightslateblue",
    "style": 'filled',
}

inheritance_edge_attrs = {
    "arrowsize": 1.5,
    "color": "royalblue",
    "penwidth": 1.5,
}