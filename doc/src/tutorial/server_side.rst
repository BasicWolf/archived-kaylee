.. _tutorial-server-side:

Step 4: Server-Side Code
========================

Now, let's code a bit on the server-side. First, we need to import the
required components of Kaylee::

  # monte_carlo_pi.py

  from kaylee import Project, Task
  from kaylee.errors import InvalidResultError

Next, we have to subclass ``Project`` in order for Kaylee's import system
to recognize it::

  class MonteCarloPiProject(Project):
      ...

Before continuing with the code, lets first think, what kind of
configuration is required in order to initialize the project? As it was
discussed in :ref:`tutorial-requirements` and implemented in
:ref:`tutorial-client-side`, the configuration consists of the amount
of random points and the URL of ``alea.js`` script to be passed to the
client and the amount of tasks to execute on the server::

  def __init__(self, *args, **kwargs):
      super(MonteCarloPiProject, self).__init__(*args, **kwargs)
      self.client_config.update({
          'alea_script'   : kwargs['alea_script'],
          'random_points' : kwargs['random_points']
      })
      self.tasks_count = kwargs['tasks_count']
      self._tasks_counter = 0

.. module:: kaylee

Here, the :py:attr:`Project.client_config` attribute is the configuration
object sent to the client and ``self.tasks_count`` and ``self._tasks_counter``
are the attributes related to the amount of tasks to be executed.

Next, let's implement two basic abstract methods of Kaylee Project::

  def __getitem__(self, task_id):
      return Task(task_id)

  def __next__(self):
      if self._tasks_counter < self.tasks_count:
          self._tasks_counter += 1
          return self[self._tasks_counter]
      else:
          raise StopIteration()

As you can see, ``__next__()`` in conjunction with ``__getitem__()`` yields
a :py:class:`task <Task>` object with numerical id derived from
``self._tasks_counter``.

The next important part of every project is the :py:meth:`normalize
<Project.normalize>` method. It is used to verify and normalize the results
returned by the client. In this case the calculated value of PI is
extracted from the parsed JSON object (dictionary)::

  def normalize(self, task_id, data):
      try:
          return data['pi']
      except KeyError:
          raise InvalidResultError(data, '"pi" key was not found')


And finally, :py:meth:`Project.store_result` - the method which stores
the distributed computation results and determines whether all required
data is collected and the application is completed::

  def store_result(self, task_id, data):
      super(MonteCarloPiProject, self).store_result(task_id, data)
      if len(self.storage) == self.tasks_count:
          self.completed = True
          self._announce_results()


Ah, almost missed the part which announces the final results::

  def _announce_results(self):
      mid_pi = (sum(res[0] for res in self.storage.values()) /
                len(self.storage))
      print('The  value of PI computed by the Monte-Carlo method is: {}'
            .format(mid_pi))

That is the message you're going to see in Kaylee's front-end shell or
logs.

The last step to do with the code: the project is still has to be imported
in ``__init__.py`` in order for Kaylee to be able to find it::

  from .monte_carlo_pi import MonteCarloPiProject

Continue with :ref:`tutorial-configuration`.
