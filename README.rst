buildbot-washer |license| |pyver| |version| |tests| |coverage|
==============================================================

A library of primitives to achieve *inversion of control*, *pipelines as
code* and other useful patterns on top of **buildbot**.

.. figure:: https://raw.githubusercontent.com/BBVA/buildbot-washer/develop/logo.png
   :align: right
   :alt: buildbot-washer logo


Features & Goals
----------------

* Simplify User Contributions
* Containerized Plugins
* Inversion of Control
* Fabric-Style Tasks
* Pipelines as Code
* DSL Development

`buildbot-washer` supports Python >= 3.4.


Installation
------------

Depending on what you want to do `washer` should be installed on the master,
the worker, or both. Either way it can be installed with pip (or pipenv, of
course):

.. code-block:: bash

   $ pip install buildbot-washer


Documentation
-------------

A wider documentation is available on `Read the Docs`_, that should not be an
excuse for avoid reading the code ;)


How to Contribute
-----------------

#. Check the open issues or open a new one to start a discussion about a
   feature or a bug.
#. Fork `the repository`_ on GitHub and make your changes to the **develop**
   branch (or branch of it).
#. Write one or more tests showing that the bug was fixed or that the feature
   works as expected.
#. Send your pull request!


.. |license| image:: https://img.shields.io/pypi/l/buildbot-washer.svg
   :target: https://github.com/BBVA/buildbot-washer/blob/develop/LICENSE

.. |pyver| image:: https://img.shields.io/pypi/pyversions/buildbot-washer.svg
   :target: https://pypi.org/project/buildbot-washer/

.. |version| image:: https://img.shields.io/pypi/v/buildbot-washer.svg
   :target: https://pypi.org/project/buildbot-washer/

.. |tests| image:: https://img.shields.io/travis/BBVA/buildbot-washer.svg
   :target: https://travis-ci.org/BBVA/buildbot-washer

.. |coverage| image:: https://img.shields.io/codecov/c/gh/BBVA/buildbot-washer.svg
   :target: https://codecov.io/gh/BBVA/buildbot-washer

.. _Read the Docs: https://readthedocs.org
.. _the repository: https://github.com/BBVA/buildbot-washer
