.. _firststeps:

First steps
===========

This section briefly describes the concepts used in Kaylee with a minimum
of technical details.

.. module:: kaylee

Server and Nodes
----------------

Kaylee is divided in two parts: the server-side Python brains which controls
the tasks distribution and results collection and client-side
(browser-side) JavaScript Nodes which do the dirty computation work.

The server performs the following routines:

  * Registers the nodes. During the registration process Kaylee decides
    whether the host can be registered as a node and assigns the host
    a unique :py:class:`node id <NodeID>`. The information about the nodes
    is maintained on the server via an instance of :py:class:`NodesRegistry`.
  * Subscribes the nodes to applications. During the subscription process
    the node loads and initializes the project script(s).
  * Dispatches the tasks to the nodes. At this stage the subscribed nodes
    receive the tasks, solve them and return the results back.
  * Collects the results from the nodes. Kaylee decides whether the results
    are satisfactory and stores them to a permanent storage.

There are multiple simple and complex sub-routines and we will talk about
them later.

Kaylee Nodes utilize the new HTML5 Web Workers [1]_ standard in order to
avoid interfering with browser's main JavaScript event loop.
After registering and subscribing to Kaylee application, a Node has a single
job to do: solve given tasks and report the results.

.. _firststep_projects_and_tasks:


Projects and Tasks
------------------

Kaylee tries to free users of routines related to distributed computation
as much as possible. Still, a user needs to write the server-side Python code
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

It is important to understand that a single project can be configurable so,
that it  be instantiated. For example, a project which is used to model
some complex process can be instantiated based on various initial
conditions. Each of this instances will work as a separate Kaylee
:ref:`Application <firststep_application>`.


Settings and Kaylee proxies
---------------------------

Kaylee lets you to store all settings in a single `.py` file and make them
accessible through any part of your code.
The instance of :py:class:`Kaylee` is automatically created based on
the settings provided by the user. Both settings and Kaylee object can be
accessed through the global proxies as follows::

  from kaylee import settings, kl


Controllers
-----------
A controller is an object which stands between the outer Kaylee interface
and a project. Controller keeps the track of subscribed nodes, decides
what kind of task every node will recieve and how the results are collected.

Why do we need controllers at all? Why not communicate directly with projects?
It is simple: the world on the other side of Kaylee is not perfect. You can
never be sure whether a node with assigned task will return the results
(as it can disconnect without notifying Kaylee) or the results will be correct
at all. A controller can be designed to send the same task to multiple
nodes instead of a single one. That kind redundancy is the fee for
the results integrity and accuracy.

Implementing controllers is easy as there are only two methods to implement:
`get_task(self, node)` and `accept_result(self, node, data)` (for more
details see :py:class:`Controller`).


Auto Filters
------------
Auto-filtering is yet another feature in Kaylee which allows to write less
code. Filters are Python decorators which can be automatically applied to
implementation of Controllers' and Projects' abstract methods. For example
the :py:func:`depleted_guard` filter sets project's *depleted* flag if
`project.__next__()` raises :py:exc:`StopIteration`. TODO: filters list.


Storages
--------
As we speak of the tasks' results you may wonder, how the results are
maintained on the server? Kaylee provides abstract storage interfaces
for both temporal (see :py:class:`ControllerResultsStorage`)
and permanent (See :py:class:`ProjectResultsStorage`) storages.
This allows to use any kind of storage solutions: from simple
in-memory objects to relational or NoSQL databases.

The difference between the interfaces is that controller refers to
the results by both `node id` and `task id`. On the other hand a project
knows nothing about the nodes and thus refers to the results by `task id`
only.
It is also important to remember that :py:class:`ControllerResultsStorage`
stores a single result per node per task, while
:py:class:`ProjectResultsStorage` stores multiple results per task.

But is it necessary to use a temporal controller storage? Of course not!
If the controller does not need to keep the intermediate results it can
pass them right to the project.

.. _firststep_application:


Applications
------------
By combining controllers storages and projects users form Kaylee
`Applications`. Speaking in technical terms, an application
is a combination of project, controller and storage *objects*.
which are not shareable among the applications.

For example, consider a project which is used to find the best
flight trajectories for a space station sent from the Earth to another planet
in Solar system. So, one of the applications will use an instance of
the `SpaceTrajectoryProject` class configured to search for trajectories
to Mars, and another application will use an instance of the same class
configured to search for trajectories to Pluto.

.. [1] http://www.w3schools.com/html5/html5_webworkers.asp
