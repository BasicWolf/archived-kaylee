.. _tutorial-server-side:

Step 4: Server-Side Code
========================

.. module:: kaylee

The server-side skeleton of the tutorial project should be already
available in ``montecarlopi.py``. Let's go through it line-by line.
First, the required components of Kaylee are imported::

  # montecarlopi.py

  from kaylee.project import AUTO_PROJECT_MODE
  from kaylee import Project, InvalidResultError

The ``MonteCarloPi`` subclasses :class:`kaylee.Project` in order for
Kaylee importing system to recognize it::

  class MonteCarloPi(Project):
      ...

What kind of configuration is required in order to initialize the project?
As it was discussed in :ref:`tutorial-requirements` and implemented in
:ref:`tutorial-client-side`, the configuration consists of the amount
of random points, the URL of the ``alea.js`` script and the total amount
of tasks to be supplied by the application::

  def __init__(self, *args, **kwargs):
      super(MonteCarloPi, self).__init__(mode=AUTO_PROJECT_MODE, *args, **kwargs)
      self.client_config.update({
          'alea_script'   : kwargs['alea_script'],
          'random_points' : kwargs['random_points']
      })
      self.tasks_count = kwargs['tasks_count']
      self._tasks_counter = 0

Here, :py:attr:`Project.client_config` attribute is the configuration
object sent to the client and ``self.tasks_count`` and ``self._tasks_counter``
are the attributes related to the amount of the supplied tasks.

Notice the ``mode`` argument, which determines the
:py:attr:`Project.mode`.
It tells Kaylee how project tasks are going to be solved:
*automatically*, without a user being even notified about them
or *manually*, involving the user. The ``MonteCarloPi`` project is fully
automated and requires no user interaction. Thus, its mode is set to
:data:`AUTO_PROJECT_MODE <project.AUTO_PROJECT_MODE>`.

Next, let's implement two tasks which supply Kaylee Project methods::

  def __getitem__(self, task_id):
      return {'id': task_id}

  def next_task(self):
      if self._tasks_counter < self.tasks_count:
          self._tasks_counter += 1
          return self[self._tasks_counter]
      else:
          return None

The :py:meth:`next_task() <Project.next_task>` in conjunction
with :py:meth:`__getitem__() <Project.__getitem__>` methods return a
:class:`dict` with an obligatory ``id`` key and a value derived from
``self._tasks_counter``.

The next important part of every project is the :py:meth:`normalize_result()
<Project.normalize_result>` method. It is used to verify and normalize the
results returned by the client. In this case the calculated value of PI is
extracted from the parsed JSON object (dict) and converted to float::

  def normalize_result(self, task_id, data):
      try:
          return float(data['pi'])
      except KeyError:
          raise InvalidResultError(data, '"pi" key was not found')
      except ValueError:
          raise InvalidResultError(data, 'error converting the value of "pi" to float')

And finally, :py:meth:`Project.result_stored` - is the callback invoked
by the bound controller. This is a good place to check, whether all the
required data is collected hence, the application is completed::

  def result_stored(self, task_id, data, storage):
      if len(storage) == self.tasks_count:
          self.completed = True
          self._announce_results(storage)

Ah, almost missed the part which announces the final results::

  def _announce_results(self, storage):
      mid_pi = (sum(res[0] for res in storage.values()) / len(storage))
      print('The  value of PI computed by the Monte-Carlo method is: {}'
            .format(mid_pi))

You would see the printed results in the shell from which Kaylee process
is launched.

The last step concerning the server side : the project has to be imported
in ``__init__.py`` in order for Kaylee to be able to find it::

  from .monte_carlo_pi import MonteCarloPi

Continue with :ref:`tutorial-configuration`.
