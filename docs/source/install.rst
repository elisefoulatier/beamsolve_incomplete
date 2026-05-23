Installation guide
==================

Install possibilities
---------------------

Install from PyPI (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To install the stable version from `PyPI <https://pypi.org/project/beamsolve/>`_, use::

    pip install beamsolve

Then, simply import the package in a Python environment using::

    import beamsolve

Install from a GitHub release
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To install from a GitHub release tagged as version ``vX.Y.Z``, run::

    pip install https://github.com/YOUR_USERNAME/beamsolve/archive/refs/tags/vX.Y.Z.tar.gz

Install from the repository (latest version)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To install the latest version directly from the GitHub repository, run::

    git clone https://github.com/YOUR_USERNAME/beamsolve.git
    cd beamsolve
    pip install .

Dependencies
------------

- **Python 3.8 or higher** is required.
- ``numpy >= 1.24``
- ``matplotlib >= 3.7``
- ``scipy >= 1.10``

For development or building documentation, install additional dependencies::

    pip install -r requirements-dev.txt
    pip install -r docs/requirements.txt

Optional: use a virtual environment (recommended)
--------------------------------------------------
To avoid conflicts with other packages, create and activate a virtual environment::

    python -m venv venv             # Create the virtual environment
    .\venv\Scripts\activate         # Windows
    source venv/bin/activate        # Linux / macOS

Test the install
----------------

1. Open a Python environment.
2. Run one of the examples in the :doc:`Application examples <examples>` section.
3. You should see the beam modal frequencies and mode shapes.
