# Configuration file for Sphinx documentation builder.

from __future__ import annotations

import os
import sys

project = "gh-skyline-python"
copyright = "2026 Jacob L. Steenwyk"
author = "Jacob L. Steenwyk"

extensions = ["sphinx.ext.githubpages"]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = None

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "body_max_width": "960px",
    "logo_only": True,
}
html_logo = "_static/img/logo.png"
html_show_sourcelink = False
html_static_path = ["_static"]

html_sidebars = {
    "**": [
        "navigation.html",
        "relations.html",
        "searchbox.html",
    ]
}


def setup(app):
    app.add_css_file("custom.css")
