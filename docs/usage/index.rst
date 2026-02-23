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

ASCII Key
---------

- ``╽`` high activity at column top
- ``┃`` medium activity at column top
- ``╻`` low activity at column top
- ``▓`` high activity in middle/base blocks
- ``▒`` medium activity in middle/base blocks
- ``░`` low activity in middle/base blocks
- ``.`` future dates (not yet reached)
- ``<space>`` zero contributions

Output Naming
-------------

Default output pattern:

- ``{username}-{year|year-range}-github-skyline.stl``

If ``--output`` omits ``.stl``, the extension is added automatically.

3D Printing
-----------

The generated ``.stl`` file is ready for standard 3D-print workflows.

1. Import the STL into a slicer (``PrusaSlicer``, ``Cura``, ``Bambu Studio``, etc.).
2. Orient the model flat on the build plate.
3. Slice to ``gcode`` and print.

Starter slicer settings:

- Layer height: ``0.20 mm``
- Walls/perimeters: ``2-3``
- Top/bottom layers: ``4-5``
- Infill: ``10-15%`` (grid or gyroid)
- Supports: ``Off`` (usually not needed)
- Build plate adhesion: ``Brim`` if corners lift
