# -*- coding: utf-8 -*-

#%% Imports
import numpy as np
from beamsolve import beam, FEM, Analytical
import matplotlib.pyplot as plt

# %matplotlib tkAgg # Magic IPython command to display Figures in a pop up Window

#%% Define the beam
# Clamped-free steel beam, rectangular cross-section
A, I = beam.rectangular_section(b=0.02, h=0.005)
beam = beam.Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
            bc_left="clamped", bc_right="free")

#%% FEM modal analysis
fem_model = FEM.FEMModel(beam=beam, ne=20)
sol_fem   = fem_model.solve_modes(n_modes=4)

print("FEM natural frequencies [Hz]:")
for k, f in enumerate(sol_fem.frequencies):
    print(f"  Mode {k+1}: {f:.3f} Hz")

#%% Analytical modal analysis
analytical_model = Analytical.AnalyticalModel(beam=beam, n_modes=4)
sol_analytical   = analytical_model.solve_modes()

print("\nAnalytical natural frequencies [Hz]:")
for k, f in enumerate(sol_analytical.frequencies):
    print(f"  Mode {k+1}: {f:.3f} Hz")

#%% Compare FEM vs analytical frequencies
print("\nRelative error FEM vs analytical [%]:")
for k in range(4):
    err = abs(sol_fem.frequencies[k] - sol_analytical.frequencies[k]) / sol_analytical.frequencies[k] * 100
    print(f"  Mode {k+1}: {err:.4f} %")

#%% Plot mode shapes
FEM.visualisation.plot_mode_shapes(sol_fem)
Analytical.visualisation.plot_mode_shapes(sol_analytical, fig=plt.gcf())

# %%
