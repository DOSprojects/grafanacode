***************
Release process
***************

TODO: check the validity of this

Pre-release
-----------

* Pick a new version number (e.g. ``X.Y.Z``)
* Update `CHANGELOG.rst <https://github.com/LDossche/grafanacode/blob/main/CHANGELOG.rst>`_ with that number
* Update `pyproject.toml <https://github.com/LDossche/grafanacode/blob/main/pyproject.toml>`_ with that number

Smoke-testing
-------------

* Run

      .. code-block:: console

         $ python setup.py install --user

* Check ``~/.local/bin/generate-dashboard`` for the update version.
* Try the example on `README <https://github.com/LDossche/grafanacode/blob/main/README.rst>`_.

Releasing
---------

* Head to `<https://github.com/LDossche/grafanacode/releases/new>`_ and create the release there.
* Wait for GitHub Actions to complete the build and release.
* Confirm on `<https://pypi.org/project/grafanacode/>`_ that the release made it there.

Follow-up
---------

* Run

      .. code-block:: console

         $ pip install grafanacode -U

* Check if the upgrade worked and the test above still passes.

Pro memory: creating a python package
-------------------------------------

Credits to `Publish Your Python Code to PyPI in 5 Simple Steps <https://builtin.com/data-science/how-to-publish-python-code-pypi>`_.
From this document one can find following workflow below.

    .. code-block:: console

        grc_module
        ├── doc
        ├── grafanacode
        │   ├── examples
        │   │   ├── __init__.py (empty)
        │   │   └── example... .py
        │   ├── plugins
        │   │   ├── __init__.py (empty)
        │   │   └── ... .py
        │   ├── tests
        │   │   ├── __init__.py (empty)
        │   │   └── test... .py
        │   ├── __init__.py
        │   └── ... .py
        ├── .gitattributes
        ├── .gitignore
        ├── .pylintrc
        ├── .readthedocs.yaml
        ├── CHANGELOG.rst
        ├── LICENSE
        ├── MANIFEST.in
        ├── README.rst
        └── pyproject.toml


* Install dependencies:

    .. code-block:: console
    
        # Install wheel tool.
        # Have the latest version of the build tool.
        # Install Twine, which is a tool to help create the package.

        > pip install wheel
        > python -m pip install --upgrade build
        > pip install twine

* Get Code Files Ready:

* Prepare Supporting Files:

* Build Package Locally:

    .. code-block:: console

        > python -m build

If all your files are ok, this command produces many lines of commands and ends with no error.
 
* Upload Package to TestPyPI:

    .. code-block:: console
 
        > python -m twine upload --repository testpypi dist/*

        Results in something similar to:
            Uploading distributions to https://test.pypi.org/legacy/
            Enter your username: <username>
            Enter your password: <password>
            Uploading yourpkg_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
            100%|█████████████████████| 4.65k/4.65k [00:01<00:00, 2.88kB/s]
            Uploading yourpkg_YOUR_USERNAME_HERE-0.0.1.tar.gz
            100%|█████████████████████| 4.25k/4.25k [00:01<00:00, 3.05kB/s]
 
* Test Package on testPyPI:

    Create a new virtual environment

    Test to make sure the module works properly.

    .. code-block:: console
 
        > pip install --index-url https://test.pypi.org/simple/ grafanacode

 
* Upload Package to PyPI:

    .. code-block:: console
 
        > python -m twine upload --repository PyPI dist/*
 
        If the package was already published and this is an update:

    .. code-block:: console
 
        > python -m twine upload --skip-existing dist/*
 
* Test Package on PyPI
 
    Create a new virtual environment

    Test to make sure the module works properly.

    .. code-block:: console

        > pip install grafanacode

