# -*- coding: utf-8 -*-
"""
Finite element model for an Euler-Bernoulli beam.

@author: Vincent Mahé
"""

import numpy as np
from typing import TYPE_CHECKING

from ..beam.beam import Beam


class FEMModel:
    r"""
    Finite element model of an Euler-Bernoulli beam.

    The beam is discretised into ``ne`` elements of equal length.
    Each node has two degrees of freedom: transverse displacement :math:`v` and rotation :math:`\theta`. The global stiffness matrix :math:`\mathrm{K}` and mass matrix :math:`\mathrm{M}` are assembled using the standard Hermite shape functions.

    Parameters
    ----------
    beam : Beam
        The beam to model.
    ne : int
        Number of finite elements.

    Examples
    --------
    >>> from beamsolve.beam import Beam, rectangular_section
    >>> from beamsolve.FEM import FEMModel
    >>> A, I = rectangular_section(b=0.02, h=0.005)
    >>> beam = Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
    ...             bc_left="clamped", bc_right="free")
    >>> model = FEMModel(beam=beam, ne=20)
    """

    if TYPE_CHECKING:
        beam       : Beam
        ne         : int
        n_nodes    : int
        n_dof      : int
        Le         : float
        K          : "np.ndarray"
        M          : "np.ndarray"

    def __init__(self, beam: Beam, ne: int = 20):
        self.beam       = beam
        self.ne         = ne
        self.n_nodes    = ne + 1
        self.n_dof      = 2 * self.n_nodes
        self.Le         = beam.L / ne

        # Elementary matrices
        self.Ke = self.element_stiffness()
        self.Me = self.element_mass()

        # Reduced assembled matrices
        self.K, self.M = self.reduced_matrices()


    

    def assemble_global_matrix(self, Me) -> np.ndarray:
        r"""
        Assemble the global finite element (mass or stiffness) matrix.

        Parameters
        ----------
        Me: np.ndarray
            The elementary matrix to be assembled.
        """
        
        # Initialisation
        M = np.zeros((self.n_dof, self.n_dof))

        # Build the global matrix
        for e in range(self.ne):
            dofs = [2*e, 2*e+1, 2*e+2, 2*e+3]
            for i, di in enumerate(dofs):
                for j, dj in enumerate(dofs):
                    M[di, dj] += Me[i, j]

        return M

    def get_constrained_dofs(self) -> list:
        r"""
        Return the list of constrained degrees of freedom based on the beam
        boundary conditions.

        Returns
        -------
        constrained : list of int
            Indices of the constrained DOFs.
        """

        # Build a constraints mapping
        constrained = []
        bc_map = {
            "clamped" : [True, True],   # v=0, theta=0
            "pinned"  : [True, False],  # v=0, theta free
            "free"    : [False, False], # unconstrained
        }

        # Left end: node 0 → DOFs 0, 1
        fix_v, fix_t = bc_map[self.beam.bc_left]
        if fix_v: constrained.append(0)
        if fix_t: constrained.append(1)

        # Right end: node n_nodes-1 → DOFs 2*(n_nodes-1), 2*(n_nodes-1)+1
        last = 2 * (self.n_nodes - 1)
        fix_v, fix_t = bc_map[self.beam.bc_right]
        if fix_v: constrained.append(last)
        if fix_t: constrained.append(last + 1)

        return constrained

    def get_free_dofs(self):
        r"""
        Get the unconstrained dof
        """

        constrained = self.get_constrained_dofs()
        free_dofs   = [d for d in range(self.n_dof) if d not in constrained]

        return free_dofs

    def reduced_matrices(self):
        r"""
        Build the reduced stiffness and mass matrices from the global ones and the constraints.
        """

        # Get the unconstraint dof
        free_dofs = self.get_free_dofs()

        # Global matrices
        Kg = self.assemble_global_matrix(self.Ke)
        Mg = self.assemble_global_matrix(self.Me)

        # Build the reduced matrices
        Kr = Kg[np.ix_(free_dofs, free_dofs)]
        Mr = Mg[np.ix_(free_dofs, free_dofs)]

        return Kr, Mr
    
    def solve_modes(self, n_modes: int = 5) :
        r"""
        Solve the generalised eigenvalue problem and return the modal solution.

        The following problem is solved on the reduced (free DOF) matrices:

        .. math::
            \mathrm{K} \, \boldsymbol{\phi} =
            \omega^2 \, \mathrm{M} \, \boldsymbol{\phi}.

        Parameters
        ----------
        n_modes : int, optional
            Number of modes to compute. Default is 5.

        Returns
        -------
        sol : FEMSolution
            The modal solution.

        Examples
        --------
        >>> from beamsolve.beam import Beam, rectangular_section
        >>> from beamsolve.FEM import FEMModel
        >>> A, I = rectangular_section(b=0.02, h=0.005)
        >>> beam  = Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
        ...              bc_left="clamped", bc_right="free")
        >>> fem_model = FEMModel(beam=beam, ne=20)
        >>> sol_fem   = fem_model.solve_modes(n_modes=3)
        """
        import scipy.linalg as slg
        from .solver import FEMSolution, _normalise

        # Solve generalised eigenvalue problem
        eigvals, eigvecs = slg.eigh(self.K, b=self.M)

        # Sort by ascending frequency
        sort_idx = np.argsort(eigvals)
        eigvals  = eigvals[sort_idx]
        eigvecs  = eigvecs[:, sort_idx]

        # Keep only the requested number of modes
        eigvals = eigvals[:n_modes]
        eigvecs = eigvecs[:, :n_modes]

        omegas      = np.sqrt(eigvals)
        frequencies = omegas / (2 * np.pi)

        # Expand eigenvectors back to full DOF space (zeros at constrained DOFs)
        free_dofs = self.get_free_dofs()
        Phi       = np.zeros((self.n_nodes, n_modes))

        for k in range(n_modes):
            phi_full = np.zeros(self.n_dof)
            for i, d in enumerate(free_dofs):
                phi_full[d] = eigvecs[i, k]
            phi_v    = phi_full[0::2]   # displacement DOFs only
            Phi[:, k] = _normalise(phi_v)

        x_nodes = np.linspace(0, self.beam.L, self.n_nodes)

        return FEMSolution(
            frequencies = frequencies,
            omegas      = omegas,
            Phi         = Phi,
            x_nodes     = x_nodes,
        )


    def element_stiffness(self) :
        r"""
        Compute elementary stiffness matrix.

        Parameters
        ----------
        self :
            Description of the problem

        Returns
        -------
        Ke : ndarray
            The elementary stiffness matrix.
        """
        E = self.beam.E
        I = self.beam.I
        Le = self.Le

        # Build elementary 4 x 4 matrix
        Ke = E*I/Le**3*np.array([[12, 6*Le, -12, 6*Le], [6*Le, 4*Le**2, -6*Le, 2*Le**2], [-12, -6*Le, 12, -6*Le], [6*Le, 2*Le**2, -6*Le, 4*Le**2]])

        return Ke
    
    def element_mass(self) :
        r"""
        Compute elementary mass matrix.

        Parameters
        ----------
        self :
            Description of the problem

        Returns
        -------
        Me : ndarray
            The elementary mass matrix.
        """
        A = self.beam.A
        rho = self.beam.rho
        Le = self.Le

        # Build elementary 4 x 4 matrix
        Me = rho*A*Le/420*np.array([[156, 22*Le, 54, -13*Le], [22*Le, 4*Le**2, 13*Le, -3*Le**2], [54, 13*Le, 156, -22*Le], [-13*Le, -3*Le**2, -22*Le, 4*Le**2]])
        
        return Me