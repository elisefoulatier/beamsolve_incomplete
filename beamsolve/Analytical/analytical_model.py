# -*- coding: utf-8 -*-
"""
Analytical modal analysis of the Euler-Bernoulli beam.

@author: [Author name]
"""

import numpy as np
from scipy.optimize import brentq
from typing import TYPE_CHECKING

from ..beam.beam import Beam


class AnalyticalSolution:
    r"""
    Analytical modal solution of the beam.

    Parameters
    ----------
    frequencies : numpy.ndarray
        Natural frequencies [Hz], shape ``(n_modes,)``, sorted in ascending
        order.
    omegas : numpy.ndarray
        Angular natural frequencies [rad/s], shape ``(n_modes,)``.
    betas : numpy.ndarray
        Wavenumbers :math:`\beta` [1/m], shape ``(n_modes,)``.
    Phi : numpy.ndarray
        Normalised mode shapes, shape ``(n_points, n_modes)``. Each column is
        a mode shape evaluated on the spatial grid ``x``. Normalisation: the
        component with the largest absolute value is 1, and the first
        non-negligible component is positive.
    x : numpy.ndarray
        Spatial grid [m], shape ``(n_points,)``.
    """

    if TYPE_CHECKING:
        frequencies : "np.ndarray"
        omegas      : "np.ndarray"
        betas       : "np.ndarray"
        Phi         : "np.ndarray"
        x           : "np.ndarray"

    def __init__(self, frequencies, omegas, betas, Phi, x):
        self.frequencies = frequencies
        self.omegas      = omegas
        self.betas       = betas
        self.Phi         = Phi
        self.x           = x


class AnalyticalModel:
    r"""
    Analytical modal analysis of an Euler-Bernoulli beam.

    Parameters
    ----------
    beam : Beam
        The beam to analyse.
    n_modes : int
        Number of modes to compute.

    Notes
    -----
    The natural frequencies and mode shapes are computed from the analytical
    solution of the Euler-Bernoulli beam equation

    .. math::
        EI \frac{\partial^4 V}{\partial x^4} - \rho A \omega^2 V = 0.

    The general solution for the mode shape :math:`V(x)` is

    .. math::
        V(x) = C_1 \cos(\beta x) + C_2 \sin(\beta x)
              + C_3 \cosh(\beta x) + C_4 \sinh(\beta x),

    where the wavenumber :math:`\beta` is related to the angular frequency by

    .. math::
        \beta^4 = \frac{\rho A \omega^2}{EI}.

    The boundary conditions at both ends are gathered in a :math:`4 \times 4`
    matrix :math:`\mathrm{Z}(\beta)` such that :math:`\mathrm{Z}(\beta)\,\mathbf{C} = \mathbf{0}`.
    Natural frequencies correspond to values of :math:`\beta` for which
    :math:`\det \mathrm{Z}(\beta) = 0`. The associated mode shape coefficients
    :math:`\mathbf{C}` are obtained as the null vector of :math:`\mathrm{Z}(\beta)` via SVD.

    The rows of :math:`\mathrm{Z}(\beta)` encode the following conditions:

    - **Clamped** end: :math:`V = 0` and :math:`V' = 0`
    - **Pinned** end: :math:`V = 0` and :math:`V'' = 0`
    - **Free** end: :math:`V'' = 0` and :math:`V''' = 0`

    Examples
    --------
    >>> from beamsolve.beam import Beam, rectangular_section
    >>> from beamsolve.Analytical import AnalyticalModel
    >>> A, I = rectangular_section(b=0.02, h=0.005)
    >>> beam  = Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
    ...              bc_left="clamped", bc_right="free")
    >>> analytical_model = AnalyticalModel(beam=beam, n_modes=3)
    >>> sol   = analytical_model.solve_modes()
    >>> sol.frequencies
    array([...])
    """

    if TYPE_CHECKING:
        beam    : Beam
        n_modes : int

    def __init__(self, beam: Beam, n_modes: int = 5):
        self.beam    = beam
        self.n_modes = n_modes

    # ── BC matrix ─────────────────────────────────────────────────────────────

    def bc_rows(self, bc: str, x: float, beta: float) -> np.ndarray:
        r"""
        Return the two rows of :math:`\mathrm{Z}(\beta)` corresponding to boundary
        condition ``bc`` applied at position ``x``.

        Parameters
        ----------
        bc : str
            Boundary condition type (``"clamped"``, ``"pinned"``, ``"free"``).
        x : float
            Position [m] where the BC is applied.
        beta : float
            Wavenumber [1/m].

        Notes
        -----
        The mode shape :math:`V(x) = C_1\cos(\beta x) + C_2\sin(\beta x) + C_3\cosh(\beta x) + C_4\sinh(\beta x)`
        and its derivatives evaluated at ``x`` give the following rows:

        .. math::
            V    &: [\cos(\beta x),\ \sin(\beta x),\ \cosh(\beta x),\ \sinh(\beta x)] \\
            V'   &: \beta\,[-\sin(\beta x),\ \cos(\beta x),\ \sinh(\beta x),\ \cosh(\beta x)] \\
            V''  &: \beta^2\,[-\cos(\beta x),\ -\sin(\beta x),\ \cosh(\beta x),\ \sinh(\beta x)] \\
            V''' &: \beta^3\,[\sin(\beta x),\ -\cos(\beta x),\ \sinh(\beta x),\ \cosh(\beta x)]

        Returns
        -------
        rows : numpy.ndarray, shape (2, 4)
            Two rows of the BC matrix.
        """
        bx        = beta * x
        co, si    = np.cos(bx),  np.sin(bx)
        ch, sh    = np.cosh(bx), np.sinh(bx)
        b, b2, b3 = beta, beta**2, beta**3

        row_V   = np.array([ co,     si,     ch,    sh   ])
        row_dV  = np.array([-b*si,   b*co,   b*sh,  b*ch ])
        row_d2V = np.array([-b2*co, -b2*si,  b2*ch, b2*sh])
        row_d3V = np.array([ b3*si, -b3*co,  b3*sh, b3*ch])

        if bc == "clamped":
            return np.array([row_V,   row_dV ])   # V=0,   V'=0
        elif bc == "pinned":
            return np.array([row_V,   row_d2V])   # V=0,   V''=0
        elif bc == "free":
            return np.array([row_d2V, row_d3V])   # V''=0, V'''=0

    def build_Z(self, beta: float) -> np.ndarray:
        r"""
        Assemble the :math:`4 \times 4` boundary condition matrix
        :math:`\mathrm{Z}(\beta)`.

        Parameters
        ----------
        beta : float
            Wavenumber [1/m].

        Returns
        -------
        Z : numpy.ndarray, shape (4, 4)
        """
        rows_left  = self.bc_rows(self.beam.bc_left,  0,           beta)
        rows_right = self.bc_rows(self.beam.bc_right, self.beam.L, beta)
        return np.vstack([rows_left, rows_right])

    def characteristic_equation(self, beta: float) -> float:
        r"""
        Evaluate the characteristic equation :math:`\det \mathrm{Z}(\beta)`.

        To avoid numerical overflow from the hyperbolic functions at large
        :math:`\beta L`, the determinant is normalised by the Frobenius norm
        of :math:`\mathrm{Z}`:

        .. math::
            f(\beta) = \frac{\det \mathrm{Z}(\beta)}{\| \mathrm{Z}(\beta) \|_F^4}

        Parameters
        ----------
        beta : float
            Wavenumber [1/m].

        Returns
        -------
        float
            Value of the normalised characteristic equation.
        """
        Z    = self.build_Z(beta)
        norm = np.linalg.norm(Z, ord='fro')
        if norm == 0:
            return 0.0
        return np.linalg.det(Z) / norm**4

    # ── Root finding ──────────────────────────────────────────────────────────

    def find_betas(self) -> np.ndarray:
        r"""
        Find the first ``n_modes`` roots of :math:`\det \mathrm{Z}(\beta) = 0` by
        scanning for sign changes and refining with Brent's method.

        Returns
        -------
        betas : numpy.ndarray
            Array of wavenumbers :math:`\beta` [1/m], shape ``(n_modes,)``.
        """
        n_scan    = 10000
        betaL_max = (self.n_modes + 2) * np.pi
        beta_arr  = np.linspace(0.01, betaL_max / self.beam.L, n_scan)

        f_arr = np.array([self.characteristic_equation(b) for b in beta_arr])
        roots = []

        for i in range(len(f_arr) - 1):
            if f_arr[i] * f_arr[i + 1] < 0:
                try:
                    root = brentq(
                        self.characteristic_equation,
                        beta_arr[i], beta_arr[i + 1],
                        xtol=1e-12,
                    )
                    roots.append(root)
                except ValueError:
                    pass
            if len(roots) == self.n_modes:
                break

        if len(roots) < self.n_modes:
            raise RuntimeError(
                f"Only {len(roots)} roots found out of {self.n_modes} requested. "
                "Try increasing the scan range."
            )

        return np.array(roots[:self.n_modes])

    # ── Mode shapes ───────────────────────────────────────────────────────────

    def mode_coefficients(self, beta: float) -> np.ndarray:
        r"""
        Compute the mode shape coefficients :math:`\mathbf{C} = [C_1, C_2, C_3, C_4]`
        for a given wavenumber via SVD of :math:`\mathrm{Z}(\beta)`.

        At a root :math:`\beta_i`, :math:`\mathrm{Z}(\beta_i)` has rank 3 and its
        smallest singular value is (numerically) zero. The associated right
        singular vector — the last row of :math:`\mathrm{V}^T` in the decomposition
        :math:`\mathrm{Z} = \mathrm{U} \mathrm{\Sigma} \mathrm{V}^T` — spans the null space and gives
        :math:`\mathbf{C}`.

        Parameters
        ----------
        beta : float
            Wavenumber [1/m].

        Returns
        -------
        C : numpy.ndarray, shape (4,)
            Mode shape coefficients :math:`[C_1, C_2, C_3, C_4]`.
        """
        Z        = self.build_Z(beta)
        _, _, Vt = np.linalg.svd(Z)
        return Vt[-1]

    def phi(self, x: np.ndarray, beta: float) -> np.ndarray:
        r"""
        Evaluate the mode shape at positions ``x``.

        Parameters
        ----------
        x : numpy.ndarray
            Positions along the beam [m].
        beta : float
            Wavenumber [1/m].

        Returns
        -------
        phi : numpy.ndarray
            Mode shape values at positions ``x``.
        """
        C1, C2, C3, C4 = self.mode_coefficients(beta)
        return (
              C1 * np.cos (beta * x)
            + C2 * np.sin (beta * x)
            + C3 * np.cosh(beta * x)
            + C4 * np.sinh(beta * x)
        )

    def normalise(self, phi: np.ndarray) -> np.ndarray:
        r"""
        Normalise a mode shape vector.

        The component with the largest absolute value is set to 1. If the
        first non-negligible component is negative, the vector is flipped.

        Parameters
        ----------
        phi : numpy.ndarray
            Raw mode shape values.

        Returns
        -------
        phi_norm : numpy.ndarray
            Normalised mode shape.
        """
        phi = phi / np.max(np.abs(phi))
        for val in phi:
            if np.abs(val) > 1e-6:
                if val < 0:
                    phi = -phi
                break
        return phi

    # ── Solver ────────────────────────────────────────────────────────────────

    def solve_modes(self, x: np.ndarray = None) -> AnalyticalSolution:
        r"""
        Compute natural frequencies and mode shapes and return the analytical
        solution.

        Parameters
        ----------
        x : numpy.ndarray, optional
            Spatial grid [m] on which the mode shapes are evaluated, shape
            ``(n_points,)``. Defaults to ``numpy.linspace(0, L, 300)``.

        Returns
        -------
        sol : AnalyticalSolution
            The analytical modal solution.

        Examples
        --------
        >>> import numpy as np
        >>> from beamsolve.beam import Beam, rectangular_section
        >>> from beamsolve.Analytical import AnalyticalModel
        >>> A, I = rectangular_section(b=0.02, h=0.005)
        >>> beam  = Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
        ...              bc_left="clamped", bc_right="free")
        >>> analytical_model = AnalyticalModel(beam=beam, n_modes=3)
        >>> sol   = analytical_model.solve_modes()
        >>> sol.Phi.shape
        (300, 3)
        """
        if x is None:
            x = np.linspace(0, self.beam.L, 300)

        betas       = self.find_betas()
        omegas      = betas**2 * np.sqrt(self.beam.E * self.beam.I / (self.beam.rho * self.beam.A))
        frequencies = omegas / (2 * np.pi)

        Phi = np.zeros((len(x), self.n_modes))
        for k, beta in enumerate(betas):
            Phi[:, k] = self.normalise(self.phi(x, beta))

        return AnalyticalSolution(
            frequencies = frequencies,
            omegas      = omegas,
            betas       = betas,
            Phi         = Phi,
            x           = x,
        )
