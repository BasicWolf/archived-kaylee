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

This will create a directory with a project skeleton:

.. code-block:: none

  montecarlopi/
  |
  |--client/
  |  |
  |  --montecarlopi.js
  |
  |--__init__.py
  |--montecarlopi.py

Finally, :download:`download alea.js <alea.js>` into the ``client`` directory,
so that the project client files structure would look as follows:

.. code-block:: none

  |--client/
  |  |
  |  --alea.js
  |  --montecarlopi.js

Continue with :ref:`tutorial-client-side`.
