r"""
.. _ref_linear_elasticity_displacement_compare:

Comparison
^^^^^^^^^^

"""

import os
import numpy as np
import pandas as pd
import pyvista as pv

###############################################################################
# Compare reaction forces and strain energy
# --------------------------------------------
# Each solver script (``plot_fenicsx.py`` and ``plot_calculix.py``) saves its
# reaction forces (Rx, Ry) and total strain energy (E) to a
# ``result_for_comparison.txt`` file: the first row holds the quantity
# names and the second row their values. These files are read here and
# combined into a single comparison table.
fenicsx_results = pd.read_csv(
    os.path.join("fenicsx", "result_for_comparison.txt"), sep="\t")
calculix_results = pd.read_csv(
    os.path.join("calculix", "result_for_comparison.txt"), sep="\t")

comparison = pd.concat([fenicsx_results, calculix_results], ignore_index=True)
comparison.insert(0, "solver", ["FEniCSx", "CalculiX"])
comparison = comparison.set_index("solver")

print("Comparison between solvers:")
print(comparison.to_string())

# %%
# Relative difference between FEniCSx and CalculiX, taking CalculiX as the
# reference value, expressed as a percentage.
relative_difference = (
    (comparison.loc["FEniCSx"] - comparison.loc["CalculiX"])
    / comparison.loc["CalculiX"]
) * 100

print("\nRelative difference FEniCSx vs. CalculiX [%]:")
print(relative_difference.to_string())


###############################################################################
# Compare the displacement field
# ---------------------------------
# Read solutions
file_vtu_fenicsx = pv.read(os.path.join(
    "fenicsx", "paraview-solutions_vtu", "phasefieldx_p0_000000.vtu"))
file_vtu_fenicsx.plot(scalars='u', cpos='xy', show_scalar_bar=True, show_edges=False)

file_vtu_calculix = pv.read(os.path.join(
    "calculix", "calculix.vtu"))
file_vtu_calculix.plot(scalars='U', cpos='xy', show_scalar_bar=True, show_edges=False)

# Deform both meshes using their displacement fields
deformed_fenicsx = file_vtu_fenicsx.warp_by_vector("u", factor=0.5)
deformed_calculix = file_vtu_calculix.warp_by_vector("U", factor=0.5)

# Plot both deformed configurations
plotter = pv.Plotter()
plotter.add_mesh(
    deformed_fenicsx,
    color="blue",
    opacity=0.5,
    show_edges=False,
    label="FEniCSx (scale = 0.5)",)

plotter.add_mesh(
    deformed_calculix,
    color="red",
    opacity=1.0,
    show_edges=False,
    label="CalculiX (scale = 0.5)",)

plotter.add_legend()
plotter.view_xy()
plotter.show()
