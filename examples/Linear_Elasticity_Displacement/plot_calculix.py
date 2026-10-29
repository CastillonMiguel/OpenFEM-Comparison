r"""
.. _ref_linear_elasticity_displacement_calculix:

CalculiX
^^^^^^^^
The simulation is run from the command line with::

    /path/to/calculix -i calculix.inp

which reads ``calculix.inp`` and produces the result files (``calculix.frd``,
``calculix.dat``, ...) used afterwards.

.. literalinclude:: ../../../../examples/Linear_Elasticity_Displacement/calculix/calculix.inp
   :language: text

   
Convert the .frd results to a ParaView-readable .vtu/.vtk file with:
   ccx2paraview calculix.frd vtu

"""

import os
import pandas as pd
import pyvista as pv

###############################################################################
# CalculiX input file
# --------------------


###############################################################################
# Read the CalculiX results file (.dat)
# ----------------------------------------
# CalculiX writes the output requested with ``*NODE PRINT`` / ``*EL PRINT``
# (see ``calculix.inp``) as plain text in ``calculix.dat``. Both the
# reaction forces on the "bottom" node set and the total strain energy are
# read directly from this file.
calculix_dat_file = os.path.join("calculix", "calculix.dat")
with open(calculix_dat_file) as f:
    dat_lines = f.readlines()

# %%
# Reaction forces
# ^^^^^^^^^^^^^^^
# The reaction force table starts two lines below the header
# ``forces (fx,fy,fz) for set BOTTOM ...`` (one blank line in between) and
# ends at the next blank line. Each row contains the node number and the
# reaction force components (Rx, Ry, Rz) at that node.
reaction_forces = []
for i, line in enumerate(dat_lines):
    if line.strip().startswith("forces") and "BOTTOM" in line:
        for row in dat_lines[i + 2:]:
            if not row.strip():
                break
            node, rx, ry, rz = row.split()
            reaction_forces.append((int(node), float(rx), float(ry), float(rz)))
        break

reaction_forces = pd.DataFrame(reaction_forces, columns=["node", "Rx", "Ry", "Rz"])
print("Reaction forces on the bottom edge:")
print(reaction_forces.to_string(index=False))

# %%
# Summing the reaction force of every node on the bottom edge gives the
# total support reaction in each direction.
Rx_total, Ry_total, Rz_total = reaction_forces[["Rx", "Ry", "Rz"]].sum()
print(f"\nSum of reaction forces: Rx = {Rx_total:.6e}, "
      f"Ry = {Ry_total:.6e}, Rz = {Rz_total:.6e}")

# %%
# Strain energy
# ^^^^^^^^^^^^^
# The total strain energy is the single value printed two lines below the
# header ``total internal energy for set SPECIMEN ...``.
for i, line in enumerate(dat_lines):
    if line.strip().startswith("total internal energy"):
        strain_energy = float(dat_lines[i + 2])
        break

print(f"\nTotal strain energy: {strain_energy:.6e} kN\u00b7mm")


###############################################################################
# Save the results used for comparison
# ----------------------------------------
# The total reaction forces (Rx, Ry) and the total strain energy (E) are
# saved to ``result_for_comparison.txt``: the first row holds the quantity
# names and the second row their values. This file is later read by
# ``plot_compare.py`` to compare CalculiX against the other FEM solvers.
result_file = os.path.join("calculix", "result_for_comparison.txt")
with open(result_file, "w") as f:
    f.write("Rx\tRy\tE\n")
    f.write(f"{Rx_total}\t{Ry_total}\t{strain_energy}\n")


###############################################################################
# Plot the displacement field
# --------------------------------------
# The displacement field saved in the ``.vtu`` file is visualized with
# PyVista.
file_vtu_calculix = pv.read(os.path.join(
    "calculix", "calculix.vtu"))
file_vtu_calculix.plot(scalars='U', cpos='xy', show_scalar_bar=True, show_edges=False)
