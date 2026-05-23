Package architecture
====================

The following diagram illustrates the class structure of the :py:mod:`beamsolve.FEM` module:

.. image:: /_static/architecture/classes_beamsolve.svg
   :alt: FEM Module Class Diagram
   :width: 100%
   :align: center

.. note::
   The data types shown in this diagram may not be fully accurate.
   For the correct data types, please refer to the :doc:`modules` section of the documentation.

Generating the diagram
----------------------

The diagram above was generated using `pyreverse <https://pylint.readthedocs.io/en/stable/pyreverse.html>`_ (included in the ``pylint`` package) and `Graphviz <https://graphviz.org/>`_.

To regenerate it, go to ``docs/source/architecture/`` and run::

    pyreverse -o dot -p beamsolve ../../../beamsolve

This produces ``classes_beamsolve.dot``. Then edit the colours and layout using the ``edit_dot.py`` script::

    python edit_dot.py

Finally, convert the edited ``.dot`` file to SVG::

    dot -Tsvg classes_beamsolve_edited.dot -o ../_static/architecture/classes_beamsolve.svg
