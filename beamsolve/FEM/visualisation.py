# -*- coding: utf-8 -*-
"""
Visualisation utilities for FEM modal solutions.

@author: Vincent Mahé
"""

import numpy as np
import matplotlib.pyplot as plt

from .solver import FEMSolution


def plot_mode_shapes(sol: FEMSolution, fig: plt.Figure = None, modes: list = None, save_path: str = None):
    r"""
    Plot the transverse mode shapes of the beam.

    Parameters
    ----------
    sol : FEMSolution
        The modal solution.
    fig: Figure
        The figure where to plot the mode shapes.
    modes : list of int, optional
        Indices of the modes to plot (0-indexed). If None, all modes are
        plotted.
    save_path : str, optional
        If provided, the figure is saved at this path instead of displayed.

    Examples
    --------
    >>> from beamsolve.beam import Beam, rectangular_section
    >>> from beamsolve.FEM import FEMModel, solve_modes, visualisation
    >>> A, I = rectangular_section(b=0.02, h=0.005)
    >>> beam  = Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
    ...              bc_left="clamped", bc_right="free")
    >>> fem_model = FEMModel(beam=beam, ne=20)
    >>> sol_fem   = fem_model.solve_modes(n_modes=3)
    >>> visualisation.plot_mode_shapes(sol_fem)
    """
    if modes is None:
        modes = list(range(sol.Phi.shape[1]))

    n_plots = len(modes)
    
    if fig is None:
        fig, axes = plt.subplots(1, n_plots, figsize=(4 * n_plots, 4), sharey=False)
        if n_plots == 1:
            axes = [axes]

        for ax, k in zip(axes, modes):
            ax.plot(sol.x_nodes, sol.Phi[:, k], color="tab:cyan", linewidth=2)
            ax.set_xlabel("$x$ [m]")
            ax.set_ylabel("Normalised displacement")
            ax.set_title(
                f"Mode {k+1}\n$f_{k+1}$ = {sol.frequencies[k]:.2f} Hz"
            )
            ax.grid(True, linestyle=":", alpha=0.6)

        fig.tight_layout()

    else:
        axes = fig.get_axes()
        for ax, k in zip(axes, modes):
            ax.get_lines()[-1].set_label("Analytical")
            ax.plot(sol.x_nodes, sol.Phi[:, k], color="tab:cyan", linewidth=2, label="FEM")
            ax.legend()

    if save_path is not None:
        fig.savefig(save_path)
        print(f"Figure saved to {save_path}")
    else:
        plt.show()

    return fig, axes
