.. _basics:

Basic concepts
==============

This section briefly describes the basic concepts used in Kaylee with a
minimum of technical details.

.. module:: kaylee

Server and Nodes
----------------

Kaylee consists of two parts: the server-side Python brains, which
distribute the tasks and gather the results and the client Nodes
which execute the tasks inside the users' browsers.

The server performs the following routines:

  * Registers the nodes. During the registration process Kaylee decides
    whether the host can be registered as a node and assigns the host
    a unique :py:class:`node id <NodeID>`. The information about the nodes
    is maintained on the server via an instance of :py:class:`NodesRegistry`.
  * Subscribes the nodes to applications. During the subscription process
    the node loads and initializes the application's client-side script(s).
  * Dispatches the tasks to the nodes. At this stage the subscribed nodes
    receive the tasks, solve them and send the results back to the server.
  * Collects the results from the nodes. Kaylee decides whether the results
    are satisfactory and stores them to a permanent storage.

.. _basics_projects_and_tasks:


Projects and Tasks
------------------

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
        'id': 'a10',
        'speed': 50,
        'distance': 200,
    }


The ``id`` field is used to generate the same task if required.
For example::

  t1 = project.next_task() # t1 = {'id': 10, 'somedata': 'somevalue'}
  t2 = project[t1['id']]   # t2 = {'id': 10, 'somedata': 'somevalue'}
  t1 == t2
  # >>> True

The client-side of a project contains the code which actually solves the
given tasks (see :ref:`clientapi`). In general a user has to implement
two simple callbacks in order to complete the project's client side
(an example in CoffeeScript):

.. code-block:: coffeescript

  pj.init = (app_config) ->
      # Initialize the project, import additional resources
      # (scripts, stylesheets) if any...
      # Notify Kaylee that the project has been imported successfully.
      kl.project_imported.trigger()
      return

  pj.process_task = (task) ->
      # Process the task generate the result and notify Kaylee that
      # the task has been completed.
      result =
          param: value,
          other_param: other_value,
          # ...

      kl.task_completed.trigger(result)
      return

To keep things simple the data between the client and the server is
transferred in JSON format only.

Finally, a project has to `verify` and `normalize` the results. This is done
via the :meth:`Project.normalize_result(task_id, result)
<Project.normalize_result>` method. `Verifying` a result means confirming
that it is correct, while `normalizing` a result means converting it to a
common form which has enough information to be stored to the permanent
results storage. For example::

  def normalize_result(self, task_id, result):
      try:
          speed = int(result['speed'])
          if speed < 0:
              raise InvalidResultError(result, 'The value of speed '
                                               'cannot be negative.')
          # The speed value is the only value returned
          return result['speed']
      except KeyError as e:
          raise InvalidResultError(result, 'The "speed" key was not '
                                           'found in result.')

Controllers
-----------
A controller is an object which stands between the outer Kaylee interface
and a project. A controller keeps the track of the subscribed nodes, decides
what kind of task every node will recieve and how the results are collected.

Why do we need controllers at all? Why not communicate directly with the
projects? It is simple: the world on the other side of Kaylee is not perfect.
You can never be sure whether a node with the assigned task will return the
results (as it can disconnect without notifying Kaylee) or the results
will be correct at all. A controller can be designed to send the same
task to multiple nodes instead of a single one. That kind of redundancy
is the fee for the results' integrity and accuracy. For more details see
:py:class:`Controller API <Controller>`).


Storages
--------
As we speak of the tasks' solutions you may wonder, how these results are
maintained on the server? Kaylee provides abstract storage interfaces
for both :py:class:`temporal <TemporalStorage>` and
:py:class:`permanent <PermanentStorage>`) results.
This allows using any kind of storage solutions: from simple
in-memory objects to relational or NoSQL databases.

The difference between these interfaces is that the controllers temporally
refer to the results by both ``node id`` and ``task id``. On the other
hand there is no need to keep the node ID information when the result has
been confirmed. It is also important to remember that
:py:class:`TemporalStorage` stores a single result per node per task which
may be discarded, while :py:class:`PermanentStorage` permanently stores a
single result per ``task_id``.
Is it necessary to use a temporal controller storage? Of course not!
If the controller does not need to keep the intermediate results it can
store them directly to the permanent storage.

.. _basics_application:


Applications
------------
By combining controllers, storages and projects users create Kaylee
`Applications`. Speaking in technical terms, an application
is an instance of :class:`Controller` class with bound :class:`Project`,
:class:`TemporalStorage` and :class:`PermanentStorage` objects.

.. note:: A single project can be instantiated into
  multiple *applications* that differ by the project's or the stroages'
  configurations. For example, a project which is used to model a complex
  weather process can be instantiated based on various initial wind, humidity,
  temperature etc. conditions. Each of these project instances will work
  as a separate Kaylee Application.


Continue with :ref:`tutorial`.
