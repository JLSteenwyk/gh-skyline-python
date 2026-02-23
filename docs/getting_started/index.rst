Getting Started
===============

Requirements
------------

- Python 3.11+
- Network access to GitHub GraphQL API
- Authentication via either:

  - ``gh`` CLI session (if ``gh`` is installed)
  - ``GITHUB_TOKEN`` / ``GH_TOKEN``

Installation
------------

From PyPI (recommended for users):

.. code-block:: shell

   python3 -m venv venv
   source venv/bin/activate
   pip install -U pip
   pip install gh-skyline-python

From source (recommended for contributors):

.. code-block:: shell

   python3 -m venv venv
   source venv/bin/activate
   pip install -U pip
   pip install -e .[dev]

CLI Check
---------

After installation, verify the CLI:

.. code-block:: shell

   skyline --help

Both ``skyline`` and ``gh-skyline`` are available as command names.

Authentication
--------------

If ``gh`` is unavailable, set a token:

.. code-block:: shell

   export GITHUB_TOKEN=YOUR_TOKEN

Optional GHES host override:

.. code-block:: shell

   export GH_HOST=github.example.com
