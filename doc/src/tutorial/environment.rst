.. _tutorial-environment:

Step 2: Project Environment
===========================

Kaylee provides convenient projects management scripts which we are
going to learn in this part of the tutorial. In the working directory run:

.. code-block:: none

  python kaylee-admin.py startenv myenv

This will create a directory ``myenv`` with two files in it:

* ``klmanage.py`` - environment manager.
* ``settings.py`` - environment settings.

To start the *Monte-Carlo PI* tutorial project run:

.. code-block:: none

   python klmanage.py startproject MonteCarloPi

This will create

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
