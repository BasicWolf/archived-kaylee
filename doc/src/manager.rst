.. _manager:

Kaylee Manager
==============

*Kaylee Manager* is a set of various scripts which help to start, implement
and deploy Kaylee applications.

kaylee-admin.py
---------------

``kaylee-admin.py`` is the base admin scripts. The supported commands are:

* ``startenv name [-h]`` - the command creates a directory ``name`` with
  a skeleton of Kaylee development environment.


klmanage.py
-----------

``klmanage.py`` is the Kaylee development environment management script.
The supported commands are:

* ``startproject [-h] [-m {manual,auto}] [-t {js,coffee}] name``
  - the command creates a directory ``name`` with a skeleton of a Kaylee project.

  Options:

  + ``-m, --mode`` - defines the :ref:`Project mode <projects_modes>`.
  + ``-t, --template`` - defines the project's client-side programming
    language.

* ``build [-h] [-s SETTINGS_FILE] [-b BUILD_DIR]`` - builds the projects
  found in :config:`settings.PROJECTS_DIR <PROJECTS_DIR>` and copies all
  the necessary files (as well as the built projects) required to run
  the environment into the ``BUILD_DIR``.

  Options:

  + ``-s, --settings-file`` - path to the settings file
    (default: ``settings.py``).
  + ``-b, --build-dir`` - path to the build directory
    (default: ``_build``).

* ``run [-h] [--debug] [-s SETTINGS_FILE] [-b BUILD_DIR] [-p PORT]``
  - starts the built-in web server and runs the previously built Kaylee 
    development environment. The server currently listens on 
    ``127.0.0.1`` only.

  Options:

  + ``--debug`` - sets the logging level to DEBUG (default: ``False``)
  + ``-s, --settings-file`` - path to the settings file
    (default: ``settings.py``).
  + ``-b, --build-dir`` - path to the build directory
    (default: ``_build``).
  + ``-p, --port`` - defines the port which the debug web server
    should be listening to.
