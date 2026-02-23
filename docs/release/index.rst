Release
=======

CI Workflows
------------

- ``python-ci.yml``: test matrix and package smoke checks
- ``release-artifacts.yml``: builds and uploads ``sdist`` and ``wheel``, then publishes to PyPI on ``v*`` tags

Local Release Validation
------------------------

.. code-block:: shell

   source venv/bin/activate
   ./scripts/package_smoke_test.sh
   PYTHONPATH=src python -m pytest
   ./venv/bin/pip install build twine
   ./venv/bin/python -m build
   ./venv/bin/python -m twine check dist/*

PyPI Publish (ClipKIT-style)
----------------------------

You can use a very similar flow to ClipKIT.

.. code-block:: shell

   source venv/bin/activate
   ./venv/bin/pip install -U build twine
   rm -rf dist build *.egg-info
   ./venv/bin/python setup.py sdist bdist_wheel
   ./venv/bin/python -m twine check dist/*
   ./venv/bin/python -m twine upload dist/* -r pypi

Notes:

- Do **not** use ``--universal`` here because this package is Python 3.11+ only.
- A helper script is available at ``scripts/publish_pypi.sh``.

Automated PyPI Publish (Tags)
-----------------------------

On tag pushes matching ``v*``, GitHub Actions now publishes to PyPI automatically
after tests/build complete in ``release-artifacts.yml``.

One-time setup in PyPI:

1. Create the project (or first release) on PyPI if it does not exist yet.
2. In PyPI project settings, add a Trusted Publisher with:

   - Owner: ``JLSteenwyk``
   - Repository: ``gh-skyline-python``
   - Workflow: ``release-artifacts.yml``
   - Environment: *(leave empty unless you later enforce one)*

3. Push a version tag, for example ``v0.1.0``.

See detailed process in ``docs/RELEASE_CHECKLIST.md``.
