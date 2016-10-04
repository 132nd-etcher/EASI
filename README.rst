*********************************
Etcher's Automated Skin Installer
*********************************

Develop:

.. image:: https://ci.appveyor.com/api/projects/status/ej728cibs8q13qw2/branch/develop?svg=true&passingText=develop%20-%20OK
    :target: https://ci.appveyor.com/project/132nd-etcher/easi

.. image:: https://api.codacy.com/project/badge/Grade/3a1f938dbe5545ad9cfa29b8df61e6ac
    :target: https://www.codacy.com/app/132nd-etcher/EASI/dashboard

.. image:: https://api.codacy.com/project/badge/Coverage/3a1f938dbe5545ad9cfa29b8df61e6ac
    :target: https://www.codacy.com/app/132nd-etcher/EASI/dashboard

.. image:: https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/quality-score.png?b=develop
    :target: https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=develop

.. image:: https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/coverage.png?b=develop
    :target: https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=develop

.. image:: https://scrutinizer-ci.com/g/132nd-etcher/EASI/badges/build.png?b=develop
    :target: https://scrutinizer-ci.com/g/132nd-etcher/EASI/?branch=develop

.. image:: https://codeclimate.com/github/132nd-etcher/EASI/badges/gpa.svg
   :target: https://codeclimate.com/github/132nd-etcher/EASI

.. image:: https://codeclimate.com/github/132nd-etcher/EASI/badges/issue_count.svg
   :target: https://codeclimate.com/github/132nd-etcher/EASI


Master: no build yet

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

- if you're using Sentry, provide a 'vault.secret.py' file like this one:

   .. code-block:: python

        class Secret:
            sentry_dsn = None