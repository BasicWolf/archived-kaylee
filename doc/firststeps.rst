First steps
===========

This section briefly describes the concepts, interfaces and best practices
used in Kaylee.

.. module:: kaylee

Server and Nodes
----------------

Kaylee is divided in two parts: the server-side Python brains which controls
the tasks distribution and results collection and client-side
(browser-side) JavaScript Nodes which do the dirty computation work.

The server performs the following routines:

  * Registers the nodes.
  * Subscribes the nodes to applications.
  * Dispatches the tasks to the nodes.
  * Collects the results from the odes.

There are multiple simple and complex sub-routines among this large ones,
but we will talk about them later.

Kaylee Nodes exploit the new HTML5 Web Workers [1]_ in order to avoid
interfering with browser's main JavaScript event loop.
After registering and subscribing to Kaylee application, a Node has a single
job to do: solve given tasks and report the results.


Projects and Tasks
------------------

Kaylee tries to free users of routines related to distributed computation
as much as possible. Still a user needs to write the server-side Python code
which will generate data for computation and receive and validate the results
and the client-side code which will compute and solve the tasks
provided by the server.
In Kaylee's terms the server and client-side code is written in the scope
of a single *Project*.
A :py:class:`Project` is an iterator-like object (it is initialized
for iteration only once) which returns :py:class:`Task` objects on every
`next(project)` call. Every task **must** have a unique ID which can be
used to generate the same task if required. This means that the following
code::

  t = next(project)
  t2 = project[t.id]

should generate `t` and `t2` with identical data, so that the computation
results of `t` and `t2` are also the same.

The client-side of the project contains the code which actually solves the
given tasks (see :ref:`clientapi`). To keep things simple all communication is
done via JSON.

Global Settings and Kaylee objects
----------------------------------

Kaylee lets you to store all settings in a single `.py` file and make them
accessible through any part of your code. The settings loader looks for
an environmental variable (see :py:const:`loader.SETTINGS_ENV_VAR`) which
contains the absolute path to the settings module to be loaded::

  from kaylee.loader import SETTINGS_ENV_VAR
  os.environ[SETTINGS_ENV_VAR] = os.path.join('/path/to/kaylee/settings.py')

The settings are wrapped by a :py:class:`LazyObject` proxy object, that's why
the corresponding environmental variable must be defined **before** loading
or running any parts of the code which access the global `settings` object::

  from kaylee import settings
  print(settings.SOME_ATTRIBUTE)

The global instance of :py:class:`Kaylee` is automatically created based on
settings provided by the user. You can access it as follows::

  from kaylee import kl

At this point Kaylee should be ready for further processing.


Controllers
-----------

A controller is an object which stands between the outer Kaylee interface
and a project. Controller keeps the track of the nodes, decides what kind
of task every node will recieve and how the results are collected.

.. [1] http://www.w3schools.com/html5/html5_webworkers.asp

