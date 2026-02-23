Release
=======

CI Workflows
------------

- ``python-ci.yml``: test matrix and package smoke checks
- ``release-artifacts.yml``: builds and uploads ``sdist`` and ``wheel``

Local Release Validation
------------------------

.. code-block:: shell

   source venv/bin/activate
   ./scripts/package_smoke_test.sh
   PYTHONPATH=src python -m pytest
   ./venv/bin/pip install build twine
   ./venv/bin/python -m build
   ./venv/bin/python -m twine check dist/*

See detailed process in ``docs/RELEASE_CHECKLIST.md``.
