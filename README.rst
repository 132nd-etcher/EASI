**********************************
Etcher's Automated Stuff Installer
**********************************

.. image:: https://circleci.com/gh/132nd-etcher/int_test.svg?style=svg
    :target: https://circleci.com/gh/132nd-etcher/int_test

.. image:: https://codeclimate.com/github/132nd-etcher/int_test/badges/gpa.svg
    :target: https://codeclimate.com/github/132nd-etcher/int_test
    :alt: Code Climate

.. image:: https://codecov.io/gh/132nd-etcher/int_test/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/132nd-etcher/int_test

.. image:: https://readthedocs.org/projects/int-test/badge/?version=latest
    :target: http://int-test.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Git checkout
------------

This project uses the `Git LFS <http://https://git-lfs.github.com/>`_ extension to manage its resource files.

You'll need to install it before checking out the repository manually.

Building
--------

After adding all requirements, you'll still need to:

- build PyQt5 "\*.ui" files

   .. code-block:: python

      from PyQt5 import uic
      uic.compileUiDir(<qt_skeleton_dir>, from_imports=True, import_from='src.ui.resources')

- build PyQt5 resource files

   .. code-block:: rconsole

      pyrcc5.exe qt_resource.qrc -o qt_resource_rc.py

- provide a 'vault.secret.py' file like this one:

   .. code-block:: python

      class sentry:
         DSN = '<your sentry DSN>'

   .. note::

        Set the DSN to 'None' if you are not using Sentry