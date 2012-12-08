.. _tutorial-compiling:

Step 6: Compiling the Application
=================================

Makefile
--------

The ``monte_carlo_pi.coffee`` file can be compiled by the CoffeeScript
as follows::

  	coffee --bare -c monte_carlo_pi.coffee

But then, the script has to be added and executed in a website which has
Kaylee client engine up and running. One way is to create a website of your
own, another - use the existing Kaylee demo web application.

Kaylee demo includes convenient build scripts which build the demo application
and the project and then copy all the files to a directory which can be used
by the front-end's (or web server's) static content dispatcher.

The Makefile builds ``monte_carlo_pi.js`` locally and (if built by the
master demo Makefile) copies the fields to to the demo's ``build`` directory:

.. code-block:: makefile

  PROJECT_NAME = monte_carlo_pi
  LIB = $(PROJECT_NAME).js
  # location of coffee file and to-be-compiled js files.
  LIBDIR = js

  # js target
  TARGETS = $(LIBDIR)/$(LIB)
  CLEAN_TARGETS =

  # if make has been called recursively, add remote targets
  ifeq ($(origin PJ_RES_DIR), environment)
  PJ_JS_DIR = $(PJ_RES_DIR)/$(PROJECT_NAME)/js
  TARGETS += remote
  CLEAN_TARGETS += clean_remote
  endif

  all: $(TARGETS)

  $(LIBDIR)/$(LIB): $(LIBDIR)/$(PROJECT_NAME).coffee
      coffee --bare -c $(LIBDIR)/$(PROJECT_NAME).coffee

  remote:
      mkdir -p  $(PJ_RES_DIR)/$(PROJECT_NAME)
      cp $(LIBDIR)/*.js $(PJ_RES_DIR)/$(PROJECT_NAME)

  clean: $(CLEAN_TARGETS)
      rm -f $(LIBDIR)/$(PROJECT_NAME).js

  clean_remote:
      rm -rf $(PJ_RES_DIR)/$(PROJECT_NAME)


Do **NOT** copy-paste the code above. Makefiles syntax is based
on tab characters which are replaced by spaces here.
`Download <../_static/Makefile>`_ the Makefile and save it to
``monte_carlo_pi/Makefile``.

It is also necessary to modify the master demo Makefile in order for the
build process find the project:

.. code-block:: makefile

  # demo/Makefile

  PROJECTS = monte_carlo_pi # you can comment out the rest of the projects.


Run ``make`` in demo directory to build the projects and collect the files
to the ``build`` directory.


Continue with  :ref:`tutorial-running`.
