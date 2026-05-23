README
======

Project Home
------------
The source codes for the **beamsolve** project are hosted on `GitHub <https://github.com/YOUR_USERNAME/beamsolve>`_.

Overview
--------
The **beamsolve** package implements modal analysis of Euler-Bernoulli beams using both
the Finite Element Method and analytical solutions.
It is primarily designed as a pedagogical example for a workshop on Python package development.

The package is organised as follows:

.. code-block:: text

   beamsolve
   │   __init__.py
   │   __version__.py
   │
   ├───beam
   │       beam.py
   │       __init__.py
   │
   ├───FEM
   │       fem_model.py
   │       solver.py
   │       visualisation.py
   │       __init__.py
   │
   └───Analytical
           analytical_model.py
           visualisation.py
           __init__.py

- :py:mod:`beamsolve.beam` defines the beam geometry and material:

  - :py:func:`beamsolve.beam.beam.rectangular_section` and :py:func:`beamsolve.beam.beam.circular_section` compute cross-sectional properties,
  - :py:class:`beamsolve.beam.beam.Beam` defines the beam.

- :py:mod:`beamsolve.FEM` is the FEM solver module:

  - :py:class:`beamsolve.FEM.fem_model.FEMModel` assembles the global stiffness and mass matrices and solves the eigenvalue problem,
  - :py:mod:`beamsolve.FEM.visualisation` provides plotting utilities.

- :py:mod:`beamsolve.Analytical` is the analytical solver module:

  - :py:class:`beamsolve.Analytical.analytical_model.AnalyticalModel` computes exact natural frequencies and mode shapes,
  - :py:mod:`beamsolve.Analytical.visualisation` provides plotting utilities.

Quick start
-----------

.. code-block:: python

   from beamsolve import beam, FEM, Analytical
   import matplotlib.pyplot as plt

   A, I = beam.rectangular_section(b=0.02, h=0.005)
   beam = beam.Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
                    bc_left="clamped", bc_right="free")

   fem_model        = FEM.FEMModel(beam=beam, ne=20)
   sol_fem          = fem_model.solve_modes(n_modes=4)
   FEM.visualisation.plot_mode_shapes(sol_fem)

   analytical_model = Analytical.AnalyticalModel(beam=beam, n_modes=4)
   sol_analytical   = analytical_model.solve_modes()
   Analytical.visualisation.plot_mode_shapes(sol_analytical, fig=plt.gcf())
