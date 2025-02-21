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
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
sys.setrecursionlimit(1500)

###########################
# For a full list of toc directives:
# https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
#
# For badges and buttons:
# https://sphinx-design.readthedocs.io/en/sbt-theme/badges_buttons.html
###########################

# -- Project information -----------------------------------------------------

project = 'rickle'
copyright = '2025, Zipfian Science'
author = 'Zipfian Science'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.napoleon',
              # 'sphinx.ext.todo',
              # 'sphinx.ext.githubpages',
              'sphinx.ext.autosectionlabel',
              "myst_parser",
              "sphinx_design",
              'sphinx_copybutton'
              ]

myst_enable_extensions = ["colon_fence"]

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
# html_theme = 'sphinx_rtd_theme'
html_theme = 'sphinx_book_theme'
# html_theme ='alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'figure_align': 'htpb',
}

# The master toctree document.
master_doc = 'index'
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# html_sidebars = {'**': ['localtoc.html', 'sourcelink.html', 'searchbox.html']}

html_title = "rickle documentation"

html_theme_options = {
    "show_toc_level": 1,
    "repository_url": "https://github.com/Zipfian-Science/rickled",
    "use_repository_button": True,
    "external_links": [
        {"name": "PyPI", "url": "https://pypi.org/project/rickled/"},
    ],
    "icon_links": [
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/rickled/",
            "icon": "fa-custom fa-pypi",
            "type": "fontawesome",
        },
    ],
}

###########
##### Read here: https://sphinx-book-theme.readthedocs.io/en/latest/index.html
#########
