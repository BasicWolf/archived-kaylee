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
    the node loads and initializes the project client-side Scripture's(s).
  * Dispatches the tasks to the nodes. At this stage the subscribed nodes
    receive the tasks, solve them and send the results back to the server.
  * Collects the results from the nodes. Kaylee decides whether the results
    are satisfactory and stores them to a permanent storage.

.. _firststep_projects_and_tasks:


Projects, Tasks and Solutions
-----------------------------

Kaylee tries to free its users of routines related to the distributed
computation as much as possible. Still, a user needs to write the
server-side Python code which yields the data for computation, receives
and validates the results and the client-side code which will
compute and solve the tasks provided by the server.
In Kaylee's terms the server and client-side code is written in the scope
of a single *Project*.
A :py:class:`Project` yields tasks via a simple call::

    task = project.next_task()

A **task** is Python json-serializable dict with an obligatory ``id`` field,
e.g.::

    task = {
        'id' : 'a10',
        'speed' : 50,
        'distance' : 200,
    }


The ``id`` field is used to generate the same task if required. This means
that the following code::

  t1 = project.next_task()
  t2 = project[t1['id']]
  t1 == t2

should always be true, so that in cases where the computation algorithm is
not based on a random factor(s), the solution of ``t1`` and ``t2`` agree
as well.

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
results' integrity and accuracy. For more details see
:py:class:`Controller API <Controller>`).


Auto Filters
------------
Auto-filtering is yet another feature of Kaylee's "write less do more"
principle. Filters are Python decorators which can be automatically
applied to Controllers' and Projects' methods. They help to automate
lots of data integrity checks and conversions in any part of the
the ``Client <-> Server <-> Controller <-> Project`` inter-communication.
For example, the
:py:func:`normalize_result <kaylee.filters.normalize_result>` filter
takes care of calling result normalization and validation routines before
passing it do the decorated function. And all the methods implementing
:py:meth:`Contoller.accept_result` are usually decorated automatically,
so that a user gets already validated and normalized result.


Storages
--------
As we speak of the tasks' solutions you may wonder, how these results are
maintained on the server? Kaylee provides abstract storage interfaces
for both :py:class:`temporal <TemporalStorage>` and
:py:class:`permanent <PermanentStorage>`) storages.
This allows using any kind of storage solutions: from simple
in-memory objects to relational or NoSQL databases.

The difference between these interfaces is that controllers temporally refer
to the results by both ``node id`` and ``task id``. On the other hand there
is no need to keep the node ID information when the result has been confirmed.
It is also important to remember that :py:class:`TemporalStorage`
stores a single result per node per task which may be discarded, while
:py:class:`PermanentStorage` permanently stores a single result per
``task_id``.
Is it necessary to use a temporal controller storage? Of course not!
If the controller does not need to keep the intermediate results it can
store them right to the permanent result.

.. _firststep_application:


Applications
------------
By combining controllers, storages and projects users create Kaylee
`Applications`. Speaking in technical terms, an application
is an instance of :class:`Controller` class with bound :class:`Project`,
:class:`TemporalStorage` and :class:`PermanentStorage` objects.

Continue with :ref:`tutorial`.

.. [1] http://www.w3schools.com/html5/html5_webworkers.asp
