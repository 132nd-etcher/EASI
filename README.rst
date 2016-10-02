*********************************
Etcher's Automated Skin Installer
*********************************

.. image:: https://api.codacy.com/project/badge/Grade/3a1f938dbe5545ad9cfa29b8df61e6ac
    :target: https://www.codacy.com/app/132nd-etcher/EASI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=132nd-etcher/EASI&amp;utm_campaign=Badge_Grade

.. image:: https://api.codacy.com/project/badge/Coverage/3a1f938dbe5545ad9cfa29b8df61e6ac
    :target: https://www.codacy.com/app/132nd-etcher/EASI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=132nd-etcher/EASI&amp;utm_campaign=Badge_Coverage

.. image:: https://ci.appveyor.com/api/projects/status/ej728cibs8q13qw2/branch/master?svg=true&passingText=master%20-%20OK
    :target: https://github.com/132nd-etcher/EASI
    :alt: Master build status

.. image:: https://ci.appveyor.com/api/projects/status/ej728cibs8q13qw2/branch/develop?svg=true&passingText=develop%20-%20OK
    :target: https://github.com/132nd-etcher/EASI
    :alt: Develop build status

.. image:: https://codeclimate.com/github/132nd-etcher/EASI/badges/gpa.svg
   :target: https://codeclimate.com/github/132nd-etcher/EASI
   :alt: Code Climate

.. image:: https://codeclimate.com/github/132nd-etcher/EASI/badges/issue_count.svg
   :target: https://codeclimate.com/github/132nd-etcher/EASI
   :alt: Issue Count

.. image:: https://codecov.io/gh/132nd-etcher/EASI/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/132nd-etcher/EASI

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

        class Secret:
            sentry_dsn = None

   .. note::

        Set the DSN to 'None' if you are not using Sentry