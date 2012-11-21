.. _firststeps:

First Steps
===========

This section briefly describes the concepts used in Kaylee with a minimum
of technical details.

.. module:: kaylee

Server and Nodes
----------------

Kaylee is divided in two parts: the server-side Python brains which control
the tasks distribution, the results (solutions) collection and the
client-side Nodes communication processes.

The server performs the following routines:

  * Registers the nodes. During the registration process Kaylee decides
    whether the host can be registered as a node and assigns the host
    a unique :py:class:`node id <NodeID>`. The information about the nodes
    is maintained on the server via an instance of :py:class:`NodesRegistry`.
  * Subscribes the nodes to applications. During the subscription process
    the node loads and initializes the project script(s).
  * Dispatches the tasks to the nodes. At this stage the subscribed nodes
    receive the tasks, solve them and send the solution back to the server.
  * Collects the results from the nodes. Kaylee decides whether the results
    are satisfactory and stores them to a permanent storage.

Kaylee Nodes utilize the new HTML5 Web Workers [1]_ standard in order to
avoid interfering with browser's main JavaScript event loop.

.. _firststep_projects_and_tasks:


Projects and Tasks
------------------

Kaylee tries to free users of routines related to distributed computation
as much as possible. Still, a user needs to write the server-side Python code
which yields the data for computation, the code to receive and validate the
results and the client-side code which will compute and solve the tasks
provided by the server.
In Kaylee's terms the server and client-side code is written in the scope
of a single *Project*.
A :py:class:`Project` is an iterator-like object (it is initialized
for iteration only once) which returns :py:class:`Task` objects on every
``next(project)`` call. Every task **must** have a unique ID which can be
used to generate the same task if required. This means that the following
code::

  t = next(project)
  t2 = project[t.id]

should generate ``t`` and ``t2`` with identical data, so that in cases where
the computation algorithm is not based on a random factor(s), the solution of
``t`` and ``t2`` agree.

The client-side of a project contains the code which actually solves the
given tasks (see :ref:`clientapi`). To keep things simple the communication
between client and server is carried out via JSON.

An important matter to remember: a single project can be instantiated into
multiple *applications* that differ by project's configuration.
For example, a project which is used to model a complex weather process can
be instantiated based on various initial wind, humidity, temperature etc.
conditions. Each of this instances will work as a separate Kaylee
:ref:`Application <firststep_application>`.


Controllers
-----------
A controller is an object which stands between the outer Kaylee interface
and a project. A controller keeps the track of subscribed nodes, decides
what kind of task every node will recieve and how the results are collected.

Why do we need controllers at all? Why not communicate directly with projects?
It is simple: the world on the other side of Kaylee is not perfect. You can
never be sure whether a node with assigned task will return the results
(as it can disconnect without notifying Kaylee) or the results will be correct
at all. A controller can be designed to send the same task to multiple
nodes instead of a single one. That kind of redundancy is the fee for the
results' integrity and accuracy.

Implementing controllers is easy as there are only two methods to implement:
``get_task(self, node)`` and ``accept_result(self, node, data)`` (for more
details see :py:class:`Controller API <Controller>`).


Auto Filters
------------
Auto-filtering is yet another feature of Kaylee's "write less do more"
principle. Filters are Python decorators which can be automatically
applied to Controllers' and Projects' methods. They take care of
the ``Client <-> Server <-> Controller <-> Project`` interface specifics
and let the user to concentrate on the actual code.

Storages
--------
As we speak of the tasks' solutions you may wonder, how these results are
maintained on the server? Kaylee provides abstract storage interfaces
for both :py:class:`temporal <TemporalStorage>` and
:py:class:`permanent <PermanentStorage>`) storages.
This allows using any kind of storage solutions: from simple
in-memory objects to relational or NoSQL databases.

The difference between the interfaces is that controllers refer to
the results by both ``node id`` and ``task id``. On the other hand a project
knows nothing about the nodes and thus refers to the results by ``task id``
only.
It is also important to remember that :py:class:`TemporalStorage`
stores a single result per node per task which may be discarded, while
:py:class:`PermanentStorage` permanently stores one or multiple results
per task.

Is it necessary to use a temporal controller storage? Of course not!
If the controller does not need to keep the intermediate results it can
pass them right to the project.

.. _firststep_application:


Applications
------------
By combining controllers storages and projects users form Kaylee
`Applications`. Speaking in technical terms, an application
is an instance of :class:`Controller` class with bound :class:`Project`,
:class:`TemporalStorage` and :class:`PermanentStorage` objects.


Continue with :ref:`tutorial`.

.. [1] http://www.w3schools.com/html5/html5_webworkers.asp
