Development
===========

Run Test Suite
--------------

.. code-block:: shell

   source venv/bin/activate
   PYTHONPATH=src python -m pytest

Package Smoke Test
------------------

.. code-block:: shell

   ./scripts/package_smoke_test.sh

Parity Fixtures
---------------

Generate local parity fixtures:

.. code-block:: shell

   python tools/generate_parity_fixtures.py

Import external artifact sets (optional):

.. code-block:: shell

   python tools/import_parity_artifacts.py /path/to/artifacts

Then validate parity tests:

.. code-block:: shell

   PYTHONPATH=src python -m pytest tests/parity -q
