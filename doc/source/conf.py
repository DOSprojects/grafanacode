# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory, add these directories to sys.path here.
# If the directory is relative to the documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(os.path.abspath("./_ext"))

# -- Project information -----------------------------------------------------
project = 'grafanacode'
copyright = '2022, DOSprojects'
author = 'DOSprojects'
release = '0.5.1'

# -- General configuration ---------------------------------------------------
# Sphinx extensions. Can be extensions coming with Sphinx (named 'sphinx.ext.*') or custom ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
#    'sphinx_toolbox.more_autodoc.typehints',
    'autoattrs',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Extension settings
napoleon_google_docstring = True

napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False
napoleon_use_keyword = True
napoleon_custom_sections = None

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

# List of patterns, relative to source directory, that match files and directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

#
keep_warnings = False

# -- Options for HTML output -------------------------------------------------
# Theme to use for HTML and HTML Help pages.  See the documentation for a list of builtin themes.
#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- custom config -------------------------------------------------
'''
def skip_tofromdict(app, what, name, obj, skip, options):
    if what!='module':
        print ("TTTTT", what, "RRRR", name, obj, skip, options)
        print ("UUUU")
    if name=='Dashboard':
        print ("TTTTT", what, "RRRR", name, obj, skip, options)
        print ("UUUU")
    return True
    #skip_nested = str(obj).find("sage.misc.misc") != -1 and name.find("MainClass.NestedClass") != -1
    #return skip or skip_nested

def setup(app):
    app.connect('autodoc-skip-member', skip_tofromdict)
    
'''