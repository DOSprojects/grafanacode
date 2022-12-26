****************************
Contributing to grafanacode
****************************

TODO: check the validity of this


Thank you for contributing to grafanacode.
Here are some notes to help you get your PR merged as quickly as possible and to help us remember how to review things properly.

If something comes up during a code review or on a ticket that you think should be part of these guidelines, please say so, or even file a PR to make this doc better!

Coding guidelines
=================

* Use Python 3
* Use `attrs`_
* Use Docstrings for classes, methods and functions
* Link to official Grafana docs in comments if possible

Conventions
-----------

* Classes are ``PascalCased``
* Attributes are ``camelCased``
* Methods are ``camelCased``
* Functions are ``camelCased``
* Local variables are ``lowercased``
* Use 4 spaces indentation:
* Triple single quotes `'''` for docstrings
* Single quotes `'` for string literals

Testing
-------

The major part of grafanacode are just data classes. Little testing has been written here.
However, tests are strongly encouraged for anything with non-trivial logic.
Please try to use `hypothesis`_ for your tests.

.. code-block:: console

  $ make all

Gotchas
-------

* Do **not** use mutable values as default values for attributes when defining classes.
  Mutable values include lists (e.g. ``default=[RED, GREEN]``) and other grafanacode objects (e.g. ``default=Annotations()``).
  Instead, use `attrs.Factory`_.
  e.g. ``default=attrs.Factory(Annotations)`` or ``default=attrs.Factory(lambda: [RED, GREEN])``.

Submitting a Change Request
===========================

* Change Requests are always welcome.
* Please add an entry to the `CHANGELOG`_ in your CR.
* It helps a lot if the CR description provides some context on what you are trying to do and why you think it's a good idea.
* The smaller the CR, the more quickly it might be reviewed.
* Keep in mind this is a hobby project and there can be months with little or no time to spend on this.
* Help with coding is a more valuable option - this whole module is no rocket science.

Filing a bug
============

* Please describe what you saw, what you expected to see, and how the bug can be reproduced.
* If it comes with a test case, even better!

.. _attrs: http://www.attrs.org/en/stable/
.. _attrs.Factory: http://www.attrs.org/en/stable/api.html#attr.Factory
.. _hypothesis: http://hypothesis.works/
.. _CHANGELOG: ../../CHANGELOG.rst