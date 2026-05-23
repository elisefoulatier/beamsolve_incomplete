# -*- coding: utf-8 -*-
"""
Beam definition and cross-section helper functions.

@author: Vincent Mahé
"""

import numpy as np
from typing import Literal, TYPE_CHECKING

# Valid boundary condition types
BC = Literal["clamped", "free", "pinned"]


def rectangular_section(b: float, h: float) -> tuple:
    r"""
    Compute the cross-sectional area and second moment of area of a
    rectangular section.

    Parameters
    ----------
    b : float
        Section width [m].
    h : float
        Section height [m].

    Returns
    -------
    A : float
        Cross-sectional area [m²].
    I : float
        Second moment of area about the neutral axis [m⁴].

    Examples
    --------
    >>> from beamsolve.beam import rectangular_section
    >>> A, I = rectangular_section(b=0.02, h=0.005)
    """
    A = b * h
    I = b * h**3 / 12
    return A, I


def circular_section(d: float) -> tuple:
    r"""
    Compute the cross-sectional area and second moment of area of a
    circular section.

    Parameters
    ----------
    d : float
        Section diameter [m].

    Returns
    -------
    A : float
        Cross-sectional area [m²].
    I : float
        Second moment of area [m⁴].

    Examples
    --------
    >>> from beamsolve.beam import circular_section
    >>> A, I = circular_section(d=0.01)
    """
    A = np.pi * d**2 / 4
    I = np.pi * d**4 / 64
    return A, I


class Beam:
    r"""
    An Euler-Bernoulli beam.

    The beam is characterised by its geometry, material properties, and
    boundary conditions at both ends.

    Parameters
    ----------
    L : float
        Beam length [m].
    E : float
        Young's modulus [Pa].
    rho : float
        Material density [kg/m³].
    A : float
        Cross-sectional area [m²].
    I : float
        Second moment of area [m⁴].
    bc_left : {"clamped", "free", "pinned"}
        Boundary condition at the left end (:math:`x = 0`).
    bc_right : {"clamped", "free", "pinned"}
        Boundary condition at the right end (:math:`x = L`).

    Examples
    --------
    Clamped-free beam with a rectangular cross-section:

    >>> from beamsolve.beam import Beam, rectangular_section
    >>> A, I = rectangular_section(b=0.02, h=0.005)
    >>> beam = Beam(L=1.0, E=210e9, rho=7800, A=A, I=I,
    ...             bc_left="clamped", bc_right="free")

    Simply supported beam with a circular cross-section:

    >>> from beamsolve.beam import Beam, circular_section
    >>> A, I = circular_section(d=0.01)
    >>> beam = Beam(L=1.0, E=70e9, rho=2700, A=A, I=I,
    ...             bc_left="pinned", bc_right="pinned")
    """

    if TYPE_CHECKING:
        L        : float
        E        : float
        rho      : float
        A        : float
        I        : float
        bc_left  : str
        bc_right : str

    _VALID_BCS = {"clamped", "free", "pinned"}

    def __init__(
        self,
        L        : float,
        E        : float,
        rho      : float,
        A        : float,
        I        : float,
        bc_left  : BC = "clamped",
        bc_right : BC = "free",
    ):
        
        # Check the validity of the boundary conditions provided
        for name, bc in [("bc_left", bc_left), ("bc_right", bc_right)]:
            if bc not in self._VALID_BCS:
                raise ValueError(
                    f"{name}='{bc}' is not valid. "
                    f"Choose from {self._VALID_BCS}."
                )

        # Store the system parameters
        self.L        = L
        self.E        = E
        self.rho      = rho
        self.A        = A
        self.I        = I
        self.bc_left  = bc_left
        self.bc_right = bc_right
