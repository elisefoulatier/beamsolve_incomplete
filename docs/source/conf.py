# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# Project information
project   = 'beamsolve'
copyright = '2025, Your Name'
author    = 'Your Name'
release   = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'myst_parser',
]

# Template configuration
templates_path   = ['_templates']
exclude_patterns = []

# Generate autosummary
autosummary_generate         = True
autosummary_imported_members = True

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy':  ('https://numpy.org/doc/stable/', None),
}

# Enable math support in MyST
myst_enable_extensions = [
    "amsmath",
    "dollarmath",
]

# Options for HTML output
html_theme        = "sphinx_rtd_theme"
html_static_path  = ['_static']
html_theme_options = {
    'navigation_depth': 6,
}

# Types
autodoc_typehints = "none"
