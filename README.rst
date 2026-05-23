beamsolve
=========

A minimal Python package for **modal analysis of Euler-Bernoulli beams** using the Finite Element Method (FEM) and analytical solutions.

This package was designed as a workshop example illustrating how to structure, document, version, and publish a Python package for research.

Overview
--------

The package is organised as follows::

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

Installation
------------

.. code-block:: bash

   pip install beamsolve

License
-------

Apache 2.0.
