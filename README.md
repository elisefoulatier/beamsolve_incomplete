# beamsolve

A minimal Python package for **modal analysis of Euler-Bernoulli beams** using the Finite Element Method (FEM) and analytical solutions.

This package was designed as a workshop example illustrating how to structure, document, version, and publish a Python package for research.

## Overview

`beamsolve` is organised as follows:

```text
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
```

- `beamsolve.beam.Beam` — defines the beam geometry, material, and boundary conditions.
- `beamsolve.beam.rectangular_section` / `circular_section` — compute cross-sectional properties.
- `beamsolve.FEM.FEMModel` — assembles the global stiffness and mass matrices.
- `beamsolve.FEM.solve_modes` — solves the generalised eigenvalue problem.
- `beamsolve.FEM.visualisation` — plots mode shapes.
- `beamsolve.Analytical.AnalyticalModel` — computes exact natural frequencies and mode shapes.
- `beamsolve.Analytical.visualisation` — plots analytical mode shapes.

## Quick start

```python
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
```

## Installation

```bash
pip install beamsolve
```

Or install from the GitHub repository:

```bash
git clone https://github.com/YOUR_USERNAME/beamsolve.git
cd beamsolve
pip install .
```

## Documentation

Full documentation is available at [https://YOUR_USERNAME.github.io/beamsolve/](https://YOUR_USERNAME.github.io/beamsolve/).

## License

Apache 2.0 — see [LICENSE](LICENSE).
