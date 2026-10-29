.. _ref_examples_elasticity:

Linear Elasticity: SENT
-----------------------
This benchmark simulates a linear elastic problem under displacement-controlled loading on a Single Edge Notch Tension (SENT) specimen. A unit vertical displacement is prescribed along the top edge of a square plate, while the bottom edge is fully constrained. The analysis is performed under plane strain conditions.

Model Overview
^^^^^^^^^^^^^^
The boundary conditions are defined as follows:

* Bottom edge: both displacement components are constrained, $u_x = u_y = 0$.
* Top edge: a unit vertical displacement, $u_y = 1$, is prescribed, while the horizontal displacement remains unconstrained.
* Lateral edges: no displacement constraints or external tractions are applied.

The geometry, boundary conditions, and mesh configuration are illustrated schematically below. The plate is discretized using quadrilateral finite elements. Note that the mesh includes an initial, single-edge notch; however, since this is a linear elastic analysis, no crack propagation is considered in this model.

.. code-block::

   #           u/\/\/\/\/\/\       
   #            ||||||||||||  
   #            *----------*  
   #            |          | 
   #            |          |
   #             ----      |
   #            |          |
   #            |          | 
   #            *----------*
   #            /_\/_\/_\/_\       
   #     |Y    /////////////
   #     |
   #      ---X
   #  Z /


Material Properties
^^^^^^^^^^^^^^^^^^^
The material properties are summarized in the table below:

+----+---------+--------+
|    | VALUE   | UNITS  |
+====+=========+========+
| E  | 210     | kN/mm2 |
+----+---------+--------+
| nu | 0.3     | [-]    |
+----+---------+--------+

The mesh used to obtain the results is provided in the corresponding input files for each solver, so every solver works on an identical discretization.

Comparison Metrics
^^^^^^^^^^^^^^^^^^
The following quantities are compared between solvers:

* Displacement field, $\mathbf{u}$.
* Reaction forces along the bottom (fixed) edge.
* Total strain energy, $\int_\Omega \psi(\boldsymbol{\varepsilon(\mathbf{u})}) \, d\Omega$.
