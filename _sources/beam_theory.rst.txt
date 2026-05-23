Euler-Bernoulli beam theory
===========================

The **Euler-Bernoulli beam** model relates the transverse displacement :math:`v(x, t)`
to the applied loads through

.. math::
   EI \frac{\partial^4 v}{\partial x^4} + \rho A \frac{\partial^2 v}{\partial t^2} = q(x, t),

where :math:`E` is the Young's modulus [Pa], :math:`I` the second moment of area [m :math:`^4`],
:math:`\rho` the density [kg/m :math:`^3`], :math:`A` the cross-sectional area [m :math:`^2`],
and :math:`q` a distributed transverse load [N/m].

Modal analysis
--------------

Seeking free-vibration solutions of the form :math:`v(x,t) = V(x)\,q(t)` leads to the
spatial equation

.. math::
   EI \frac{\mathrm{d}^4 V}{\mathrm{d}x^4} - \rho A \omega^2 V = 0,

whose general solution is

.. math::
   V(x) = C_1 \cos(\beta x) + C_2 \sin(\beta x)
         + C_3 \cosh(\beta x) + C_4 \sinh(\beta x),

with the wavenumber :math:`\beta` defined by

.. math::
   \beta^4 = \frac{\rho A \omega^2}{EI}.

The natural frequencies are found by enforcing the boundary conditions, which leads to
the characteristic equation :math:`\det Z(\beta) = 0` (see :doc:`modules`).

FEM discretisation
------------------

The beam is discretised into :math:`n_e` elements of equal length :math:`\ell_e = L / n_e`.
Each node has two degrees of freedom: transverse displacement :math:`v(x,t)` and rotation
:math:`\theta(x,t) = \partial{d}v/\partial{d}x`.

The element stiffness matrix is

.. math::
   \mathrm{K}_e = \frac{EI}{\ell_e^3}
   \begin{bmatrix}
    12      &  6\ell_e    & -12      &  6\ell_e    \\
    6\ell_e &  4\ell_e^2  & -6\ell_e &  2\ell_e^2  \\
   -12      & -6\ell_e    &  12      & -6\ell_e    \\
    6\ell_e &  2\ell_e^2  & -6\ell_e &  4\ell_e^2
   \end{bmatrix},

and the element mass matrix is

.. math::
   \mathrm{M}_e = \frac{\rho A \ell_e}{420}
   \begin{bmatrix}
   156     &  22\ell_e   &  54      & -13\ell_e   \\
    22\ell_e &  4\ell_e^2  &  13\ell_e & -3\ell_e^2  \\
    54      &  13\ell_e   & 156      & -22\ell_e   \\
   -13\ell_e & -3\ell_e^2  & -22\ell_e &  4\ell_e^2
   \end{bmatrix}.

After assembly and application of boundary conditions, the natural frequencies and mode
shapes are found by solving the generalised eigenvalue problem

.. math::
   \mathrm{K}\,\boldsymbol{\phi} = \omega^2\,\mathrm{M}\,\boldsymbol{\phi}.
