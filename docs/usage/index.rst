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

Example Output (ASCII)
----------------------

Example terminal output from a generated skyline:

.. code-block:: text

    ╽╽╽       ╽╽╽       ╽╽╽       ╽╽╽       ╽╽╽       ╽
   ╽▓▓▓╽╻╻┃┃┃╽▓▓▓╽╻╻┃┃┃╽▓▓▓╽╻╻┃┃┃╽▓▓▓╽╻╻┃┃┃╽▓▓▓╽╻╻┃┃┃╽▓
   ▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒
   ▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒
   ▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒▒▒▓▓▓▓░░▒▒
   ░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░
   ░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░░▒▒▒▓▓▓▓░░

                           mona
                           2024

The same sample is tracked in the parity fixture:
``testdata/parity/ascii/mona-2024.txt``.

Output Naming
-------------

Default output pattern:

- ``{username}-{year|year-range}-github-skyline.stl``

If ``--output`` omits ``.stl``, the extension is added automatically.
