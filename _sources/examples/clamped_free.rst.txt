Clamped-free beam
-----------------

Modal analysis of a clamped-free steel beam: FEM vs analytical solution.

System description
^^^^^^^^^^^^^^^^^^

The beam is clamped at :math:`x = 0` (displacement and rotation both zero) and free at
:math:`x = L`. It has length :math:`L`, Young's modulus :math:`E`, density :math:`\rho`,
and a rectangular cross-section of width :math:`b` and height :math:`h`.

The analytical characteristic equation for a clamped-free beam is

.. math::
   1 + \cosh(\beta L)\cos(\beta L) = 0.

Code description
^^^^^^^^^^^^^^^^

The script below

- Constructs the beam using :func:`beamsolve.beam.beam.rectangular_section` and :class:`beamsolve.beam.beam.Beam`.
- Solves the eigenvalue problem using :class:`beamsolve.FEM.fem_model.FEMModel` and :meth:`beamsolve.FEM.fem_model.FEMModel.solve_modes`.
- Computes the exact solution using :class:`beamsolve.Analytical.analytical_model.AnalyticalModel`.
- Compares FEM and analytical natural frequencies.
- Plots both sets of mode shapes.

.. literalinclude:: ../../../examples/clamped_free.py
   :language: python
