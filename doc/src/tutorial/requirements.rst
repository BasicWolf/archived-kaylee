.. _tutorial-requirements:

Step 1: Project Requirements
============================


Pseudo-Random Generator
-----------------------
As we discussed before, the Monte Carlo method is based on random numbers'
sequences. Unfortunately it is not that easy to quickly generate truly random
numbers on a computer. Instead the ``pseudo-random`` generators are used for
this purpose. The problem with the javascript's standard ``Math.random()`` is
that there is no official way to start a random numbers sequence from a certain
seed. Thus, it is impossible to reproduce the sequence hence reproduce and
verify the results.
However there are great javascript libraries for pseudo-random numbers
generation. One of them is the `alea.js`_ library which we are going to use.

.. _tutorial-requirements-configuration:

Configuration
-------------
The client-side application configuration is a JSON object passed from the
server to the client during the application initialization process.
What kind of configuration does the tutorial app client requires?
First of all, a Node should know the number of random points to be generated.
Second, the project requires the ``alea.js`` library which can be loaded
on-fly via :js:func:`kl.include`. Considering these requirements, the desired
client-side configuration would be similar to::

  {
      'alea_script' : '/static/projects/monte_carlo_pi/alea.js',
      'random_points' : 100000,
  }

The server-side part of the application should be aware of the amount of
the completed tasks that would be enough to announce the computing process
to be `completed`::

  {
      'tasks_count' : 10
  }


Tasks and Solutions Data
------------------------
Every random numbers sequence needs a seed to start with. That kind of seed
already exists in every task: it is a unique ``id`` provided by the project.
Even a numerical id is enough to serve as a seed::

  {
      'id' : 1
  }

The returned solution is simpy the calculated value of PI::

  {
      'pi' : 3.14212
  }


The Algorithm
-------------

The algorithm of calculating PI is based on the theory explained in
:ref:`tutorial-introduction`::

  let points_counter = 0
  repeat random_points times:
      let x, y be random numbers in (0, 1) range.
      if x^2 + y^2 <= 1 then
          # the point is inside the circle
          points_counter += 1
  pi = 4 * points_counter / random_points

On server-side the results are collected and the mean value is calculated::

  pi = sum(pi_1, pi_2, ... pi_amount_of_tasks) / amount_of_tasks

Continue with :ref:`tutorial-project-structure`.

.. _alea.js: http://baagoe.org/en/w/index.php/Better_random_numbers_for_javascript
