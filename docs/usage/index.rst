Usage
=====

Single Year
-----------

.. code-block:: shell

   PYTHONPATH=src python -m gh_skyline --year 2024 --user JLSteenwyk --output my-skyline

Multiple Years
--------------

.. code-block:: shell

   PYTHONPATH=src python -m gh_skyline --year 2019-2024 --user JLSteenwyk --output my-skyline

Full History
------------

.. code-block:: shell

   PYTHONPATH=src python -m gh_skyline --full --user JLSteenwyk --output my-skyline

ASCII Preview Only
------------------

.. code-block:: shell

   PYTHONPATH=src python -m gh_skyline --year 2024 --user JLSteenwyk --art-only

Output Naming
-------------

Default output pattern:

- ``{username}-{year|year-range}-github-skyline.stl``

If ``--output`` omits ``.stl``, the extension is added automatically.
