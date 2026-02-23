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

.. code-block:: shell

   python3 -m venv venv
   source venv/bin/activate
   pip install -U pip
   pip install -e .[dev]

Authentication
--------------

If ``gh`` is unavailable, set a token:

.. code-block:: shell

   export GITHUB_TOKEN=YOUR_TOKEN

Optional GHES host override:

.. code-block:: shell

   export GH_HOST=github.example.com
