.. image:: _static/logo.png
   :width: 200px
   :align: center

OpenFEM-Comparison
==================

Welcome to **OpenFEM-Comparison**, a collection of benchmark problems used to
compare different open-source Finite Element (FEM) software. The same
problem (geometry, mesh, material properties and boundary conditions) is
solved independently with each FEM code, and the results are then compared
against each other.


Introduction
------------
Many open-source FEM codes exist, each with its own modeling approach,
input format and solver technology. This repository provides a common set
of benchmark problems that are solved with several of these codes, so that
their results (displacements, reaction forces, stresses, energies, ...) can
be verified and compared side by side.

Currently, the following FEM software are included in the comparison:

- `CalculiX <http://www.calculix.de/>`_: an open-source FEM solver driven by
  a text input deck (``.inp`` files), similar to Abaqus.
- `FEniCSx <https://fenicsproject.org/>`_: an open-source FEM framework for
  solving partial differential equations with Python, used here together
  with the `phasefieldx <https://phasefieldx.readthedocs.io>`_ package.

Additional FEM software can be added following the same structure described
below.


Repository Organization
------------------------
Each benchmark problem lives in its own folder under `examples/
<examples>`_. A typical example folder is organized as follows:

.. code-block::

   examples/<example_name>/
   ├── README.rst            # Describes the example: geometry, boundary
   │                         # conditions, material properties, ...
   ├── mesh/                 # Mesh shared by every FEM code (e.g. built
   │                         # with Gmsh), so all solvers use an identical
   │                         # discretization.
   ├── calculix/             # CalculiX input/output files (.inp, .frd,
   │                         # .dat, ...).
   ├── fenicsx/              # FEniCSx output files (logs, results,
   │                         # ParaView files, ...).
   ├── plot_calculix.py      # Describes/runs the CalculiX model and
   │                         # plots its results.
   ├── plot_fenicsx.py       # Sets up and runs the model with FEniCSx and
   │                         # plots its results.
   └── plot_compare.py       # Loads the results from every FEM code and
                              # compares them.

The naming convention is:

- ``README.rst``: explains the example (problem statement, geometry,
  material properties and boundary conditions). It is common to every FEM
  code used for that example.
- ``plot_<tool>.py``: one script per FEM software (for example
  ``plot_calculix.py`` for CalculiX, ``plot_fenicsx.py`` for FEniCSx). Every
  ``plot_<tool>.py`` script solves the *same* problem described in the
  example's ``README.rst``, using the same mesh, material and boundary
  conditions, so that the results are directly comparable.
- ``plot_compare.py``: gathers the results produced by every
  ``plot_<tool>.py`` script and compares them (e.g. displacement fields,
  reaction forces, energies).

To add a new benchmark problem, create a new folder under `examples/
<examples>`_ with a ``README.rst`` describing it, add one ``plot_<tool>.py``
script per FEM software to be compared, and a ``plot_compare.py`` script to
collect and compare the results.


Examples
--------
Available benchmark problems:

- `Linear_Elasticity_Displacement
  <examples/Linear_Elasticity_Displacement/README.rst>`_: linear elastic
  square plate with a fully fixed bottom edge and a prescribed vertical
  displacement on the top edge.


Contributions and Feedback
---------------------------
Contributions are welcome, whether adding new benchmark problems, adding
support for a new FEM software, or improving the existing examples. Feel
free to open an issue or a pull request.

.. footbibliography::

.. toctree::
   
   FEM_software/index
   auto_examples/index
   extras/index
