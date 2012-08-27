.. _tutorial-compiling:

Step 6: Compiling the Application
=================================

Makefile
--------

The Makefile builds ``monte_carlo_pi.js`` locally and (if built by the
master demo Makefile) copies the fields to to the ``build`` directory:

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


Do **NOT** copy-paste the code above to because Makefiles syntax is based
on tab characters. `Download <../_static/Makefile>`_ the Makefile
and save it to ``monte_carlo_pi/Makefile``.

It is also necessary to modify the master demo Makefile in order for the
build process find the project:

.. code-block:: makefile

  # demo/Makefile

  PROJECTS = monte_carlo_pi # you can comment out the rest of the applications


Run ``make`` in demo directory to build the projects and collect the files
to the ``build`` directory.


Continue with  :ref:`tutorial-running`.
