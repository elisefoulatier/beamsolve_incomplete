# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-11
### Added
- Initial release.
- `Beam` class with `rectangular_section` and `circular_section` helper functions.
- `FEMModel` class assembling global stiffness and mass matrices using Hermite shape functions.
- `FEMSolution` class storing FEM modal results.
- `FEMModel.solve_modes()` solving the generalised eigenvalue problem.
- `AnalyticalModel` class computing natural frequencies via the characteristic equation `det(Z(β)) = 0`.
- `AnalyticalSolution` class storing analytical modal results.
- `AnalyticalModel.solve_modes()` returning mode shapes evaluated on a spatial grid.
- Visualisation utilities for FEM and analytical mode shapes, with overlay support.
- Clamped-free and simply-supported beam examples.
- Sphinx documentation with online deployment via GitHub Actions and gh-pages.
