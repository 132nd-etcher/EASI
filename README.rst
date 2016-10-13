*********************************
Etcher's Automated Skin Installer
*********************************

.. image:: http://b.repl.ca/v1/Author_skill-Script_kiddie-red.png

.. image:: https://img.shields.io/badge/Author%20skill-Script%20kiddie-red.svg?style=flat

Develop:

.. image:: https://badge.waffle.io/132nd-etcher/EASI.svg?label=ready&title=Ready&style=flat
    :target: https://waffle.io/132nd-etcher/EASI 
    :alt: 'Stories in Ready'

.. image:: https://ci.appveyor.com/api/projects/status/ej728cibs8q13qw2/branch/develop?svg=true&style=flat&passingText=develop%20-%20OK
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

.. image:: https://codeclimate.com/github/132nd-etcher/EASI/badges/gpa.svg?style=flat
    :target: https://codeclimate.com/github/132nd-etcher/EASI

.. image:: https://codeclimate.com/github/132nd-etcher/EASI/badges/issue_count.svg?style=flat
    :target: https://codeclimate.com/github/132nd-etcher/EASI

.. image:: https://www.quantifiedcode.com/api/v1/project/c20bff6d0c384ec890e23c8d020ae34a/snapshot/origin:develop:HEAD/badge.svg
    :target: https://www.quantifiedcode.com/app/project/c20bff6d0c384ec890e23c8d020ae34a

.. image:: https://coveralls.io/repos/github/132nd-etcher/EASI/badge.svg?branch=HEAD&style=flat
    :target: https://coveralls.io/github/132nd-etcher/EASI?branch=HEAD

.. image:: https://snap-ci.com/132nd-etcher/EASI/branch/develop/build_image
    :target: https://snap-ci.com/132nd-etcher/EASI/branch/develop

.. image:: https://landscape.io/github/132nd-etcher/EASI/develop/landscape.svg?style=flat
    :target: https://landscape.io/github/132nd-etcher/EASI/develop
    :alt: Code Health

.. image:: https://badges.gitter.im/easi_/Lobby.svg
    :alt: Join the chat at https://gitter.im/easi_/Lobby
    :target: https://gitter.im/easi_/Lobby

.. image:: https://www.versioneye.com/user/projects/57fcb44b886dd100411cdf7e/badge.svg?style=flat
    :target: https://www.versioneye.com/user/projects/57fcb44b886dd100411cdf7e


Master: no build yet

.. image:: https://img.shields.io/librariesio/github/132nd-etcher/easi.svg

Documentation
-------------

`Project documentation <https://132nd-etcher.github.io/EASI/>`_

Project current throughput
--------------------------

.. image:: https://graphs.waffle.io/132nd-etcher/EASI/throughput.svg 
 :target: https://waffle.io/132nd-etcher/EASI/metrics/throughput 
 :alt: 'Throughput Graph'


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
