# -*- coding: utf-8 -*-
"""
FEM modal solution container and normalisation utility.

@author: Vincent Mahé
"""

import numpy as np
from typing import TYPE_CHECKING


class FEMSolution:
    r"""
    Modal solution of the beam FEM model.

    Parameters
    ----------
    frequencies : numpy.ndarray
        Natural frequencies [Hz], shape ``(n_modes,)``, sorted in ascending
        order.
    omegas : numpy.ndarray
        Angular natural frequencies [rad/s], shape ``(n_modes,)``.
    Phi : numpy.ndarray
        Normalised mode shapes, shape ``(n_nodes, n_modes)``. Each column is
        a mode shape evaluated at the beam nodes. Normalisation: the
        component with the largest absolute value is 1, and the first
        non-negligible component is positive.
    x_nodes : numpy.ndarray
        Nodal positions along the beam [m], shape ``(n_nodes,)``.
    """

    if TYPE_CHECKING:
        frequencies : "np.ndarray"
        omegas      : "np.ndarray"
        Phi         : "np.ndarray"
        x_nodes     : "np.ndarray"

    def __init__(self, frequencies, omegas, Phi, x_nodes):
        self.frequencies = frequencies
        self.omegas      = omegas
        self.Phi         = Phi
        self.x_nodes     = x_nodes


def _normalise(phi: np.ndarray) -> np.ndarray:
    r"""
    Normalise a mode shape vector.

    The component with the largest absolute value is set to 1.
    If the first non-negligible component is negative, the vector is flipped.

    Parameters
    ----------
    phi : numpy.ndarray
        Raw eigenvector.

    Returns
    -------
    phi_norm : numpy.ndarray
        Normalised mode shape.
    """
    phi = phi / np.max(np.abs(phi))

    threshold = 1e-6
    for val in phi:
        if np.abs(val) > threshold:
            if val < 0:
                phi = -phi
            break

    return phi
