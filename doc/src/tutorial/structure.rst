.. _tutorial-project-structure:

Step 2: Project Structure
=========================

The ``demo/projects`` directory contains all the demo projects with
their ``*.py``, ``*.coffee`` and ``*.js`` files. First of all create
the `monte_carlo_pi` directory in ``demo/projects/``. Add ``__init__.py``
to indicate that it is a Python package and ``monte_carlo_pi.py`` which
will contain the project code. The ``js`` sub-directory contains the
client-side of the project: ``monte_carlo_pi.coffee`` and ``alea.js``
library (`download alea.js <../_static/alea.js>`_).
Kaylee utilizes recursive make techniques to automate Kaylee projects
and demo building process. For this a ``Makefile`` file is required.

The structure of the project directory should look as following::

  demo/projects/monte_carlo_pi/
  |
  |--js/
  |  |
  |  --monte_carlo_pi.coffee
  |  --alea.js
  |
  |--__init__.py
  |--monte_carlo_pi.py
  |
  |--Makefile


Continue with :ref:`tutorial-client-side`.
