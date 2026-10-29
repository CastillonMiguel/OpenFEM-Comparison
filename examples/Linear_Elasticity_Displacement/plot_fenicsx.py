r"""
.. _ref_linear_elasticity_displacement_fenicsx:

FenicsX/PhaseFieldX
^^^^^^^^^^^^^^^^^^^

"""

###############################################################################
# Step 1: Import the required libraries
# ---------------------------------------
# ``dolfinx``, ``mpi4py`` and ``petsc4py`` are the FEniCSx building blocks.
# ``phasefieldx`` provides ready-to-use helpers (simulation input, solver,
# boundary conditions and post-processing), so this example does not need to
# reimplement the finite element formulation.
import os
import dolfinx
import mpi4py
import pyvista as pv

from phasefieldx.Element.Elasticity.Input import Input
from phasefieldx.Element.Elasticity.solver.solver import solve
from phasefieldx.Boundary.boundary_conditions import bc_xy
from phasefieldx.PostProcessing.ReferenceResult import AllResults


###############################################################################
# Step 2: Simulation parameters
# --------------------------------
# ``Data`` stores the material properties (Young's modulus ``E`` and
# Poisson's ratio ``nu``) and the folder where the results are saved. These
# values are identical to the ones used in the CalculiX input file
# (``calculix/calculix.inp``).
Data = Input(E=210.0,
             nu=0.3,
             save_solution_xdmf=False,
             save_solution_vtu=True,
             results_folder_name="fenicsx")


###############################################################################
# Step 3: Mesh
# --------------
# Instead of building a structured mesh with dolfinx, the exact same mesh
# used by CalculiX (``mesh/mesh.msh``), generated with Gmsh, is read. This
# guarantees that both solvers work on an identical discretization.
msh_file = os.path.join("mesh", "mesh.msh")
gdim = 2                           # Geometric dimension of the mesh
gmsh_model_rank = 0                # Rank of the Gmsh model in a parallel setting
mesh_comm = mpi4py.MPI.COMM_WORLD  # MPI communicator

mesh_data = dolfinx.io.gmsh.read_from_msh(
    msh_file, mesh_comm, gmsh_model_rank, gdim)
msh = mesh_data.mesh
facet_markers = mesh_data.facet_tags
fdim = msh.topology.dim - 1  # Dimension of the mesh facets

# %%
# The physical groups "bottom" (tag 8) and "top" (tag 9), defined in the
# Gmsh ``.geo`` file used to create the mesh, are retrieved here as the
# facet indices belonging to each boundary.
bottom_facet_marker = facet_markers.find(8)
top_facet_marker = facet_markers.find(9)


###############################################################################
# Step 4: Function space
# -------------------------
# Linear (degree 1) Lagrange vector elements are used for the displacement
# field u, consistent with the linear elements used by CalculiX.
V_u = dolfinx.fem.functionspace(msh, ("Lagrange", 1, (msh.geometry.dim, )))


###############################################################################
# Step 5: Boundary conditions
# ------------------------------
# These reproduce the boundary conditions of ``calculix/calculix.inp``:
#
# - ``bottom``: fully fixed, ux = uy = 0.
# - ``top``: ux = 0, uy = 1.0 (prescribed vertical displacement).
bc_bottom = bc_xy(bottom_facet_marker, V_u, fdim, value_x=0.0, value_y=0.0)
bc_top = bc_xy(top_facet_marker, V_u, fdim, value_x=0.0, value_y=1.0)

bcs_list_u = [bc_top, bc_bottom]
bcs_list_u_names = ["top", "bottom"]

# %%
# This is a single-step, linear static analysis: the prescribed displacement
# is already set when ``bc_top`` is created above, so it does not need to
# change over time. A function is still required by the generic ``solve``
# interface used for every example; here it simply reports the (constant)
# boundary condition values that get logged to ``top.dof``.
def update_boundary_conditions(bcs, time):
    return 0, 0, 0


###############################################################################
# Step 6: Solve
# ---------------
# The problem is linear, so a single pseudo-time step (``final_time = dt =
# 1.0``) is enough to obtain the solution. The displacement field, reaction
# forces and elastic energy are written to the ``fenicsx`` results folder.
final_time = 1.0
dt = 1.0

# solve(Data,
#       msh,
#       final_time,
#       V_u,
#       bcs_list_u,
#       update_boundary_conditions,
#       dt=dt,
#       bcs_list_u_names=bcs_list_u_names)


###############################################################################
# Step 7: Load the results
# ---------------------------
# ``AllResults`` reads every result file (reaction forces, energy, degrees
# of freedom, ...) written by the solver into the results folder.
S = AllResults(Data.results_folder_name)
S.set_label('FEniCSx')
S.set_color('b')

reaction_bottom_x = S.reaction_files['bottom.reaction']['Rx'].iloc[0]
reaction_bottom_y = S.reaction_files['bottom.reaction']['Ry'].iloc[0]
total_energy = S.energy_files['total.energy']['E'].iloc[0]

print(f"Reaction force at the bottom edge (Rx): {reaction_bottom_x:.4f} kN")
print(f"Reaction force at the bottom edge (Ry): {reaction_bottom_y:.4f} kN")
print(f"Total elastic energy: {total_energy:.4f} kN·mm")


###############################################################################
# Step 8: Save the results used for comparison
# ------------------------------------------------
# The reaction forces (Rx, Ry) and the total strain energy (E) are saved to
# ``result_for_comparison.txt``: the first row holds the quantity names and
# the second row their values. This file is later read by
# ``plot_compare.py`` to compare FEniCSx against the other FEM solvers.
result_file = os.path.join(Data.results_folder_name, "result_for_comparison.txt")
with open(result_file, "w") as f:
    f.write("Rx\tRy\tE\n")
    f.write(f"{reaction_bottom_x}\t{reaction_bottom_y}\t{total_energy}\n")


###############################################################################
# Step 9: Plot the displacement field
# --------------------------------------
# The displacement field saved in the ``.vtu`` file is visualized with
# PyVista.
file_vtu_fenicsx = pv.read(os.path.join(
    Data.results_folder_name, "paraview-solutions_vtu", "phasefieldx_p0_000000.vtu"))
file_vtu_fenicsx.plot(scalars='u', cpos='xy', show_scalar_bar=True, show_edges=False)
