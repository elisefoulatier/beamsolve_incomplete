Simply-supported beam
-----------------

Modal analysis of a simply-supported aluminium beam: FEM vs analytical solution.

System description
^^^^^^^^^^^^^^^^^^

The beam is supported at :math:`x = 0` (displacement zero) and supported at
:math:`x = L` (displacement y zero). It has length :math:`L`, Young's modulus :math:`E`, density :math:`\rho`,
and a circular cross-section of diameter :math:`d`.

The analytical characteristic equation for a simply-supported beam is

.. math::
   1 + \cosh(\beta L)\cos(\beta L) = 0.

Code description
^^^^^^^^^^^^^^^^

The script below

- Constructs the beam using :func:`beamsolve.beam.beam.circular_section` and :class:`beamsolve.beam.beam.Beam`.
- Solves the eigenvalue problem using :class:`beamsolve.FEM.fem_model.FEMModel` and :meth:`beamsolve.FEM.fem_model.FEMModel.solve_modes`.
- Computes the exact solution using :class:`beamsolve.Analytical.analytical_model.AnalyticalModel`.
- Compares FEM and analytical natural frequencies.
- Plots both sets of mode shapes.

.. literalinclude:: ../../../examples/simply-supported.py
   :language: python
