.. _tutorial-project-structure:

Step 1: Project Structure
=========================

Kaylee utilizes recursive Makefile techniques to automate Kaylee client,
projects and demo building process. The `src/projects` directory contains
all the user projects with all necessary `*.py` and `*.coffee` and/or `*.js`
files. So, first of all let's create `monte_carlo_pi` directory in
`src/projects/`.
It will also serve as a Python package thus, we'll need the `__init__.py`
in it. Another good idea is to leave the `__init__.py` with few lines of
code as possible and to write the code in a separate `monte_carlo_pi.py`
file.
Finally we will need a place to store the client-side code of the project,
e.g. `js` sub-directory. It will contain the `monte_carlo_pi.coffee` and
possibly 3d-party libraries required for the project.
The structure of the project directory should now look as following::

  monte_carlo_pi/
  |
  |--js/
  |  |
  |  --monte_carlo_pi.coffee
  |  --(3d-party js libraries)
  |
  |--__init__.py
  |--monte_carlo_pi.py
  |
  |--Makefile


Let's continue with writing the :ref:`client-side code <tutorial-client-side>`.
