.. _tutorial-building-and-running:

Step 6: Building and Running
============================

You are now ready to build and run the application. This is simply done
via ``klmanage.py`` as follows:

.. code-block:: none

  $ python klmanage.py build

This builds the project and copies all the files required to run
the application into the ``_build`` directory.
If the build was successful, run the debug server as follows:

.. code-block:: none

  $ python klmanage.py run

This starts Kaylee running on a debug web server (built-in Werkzeug_ web
server) on port 5000. 


To run the MonteCarloPi, open a browser at http://127.0.0.1:5000

.. _Werkzeug: http://werkzeug.pocoo.org/
