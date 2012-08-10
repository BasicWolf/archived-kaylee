.. _tutorial-requirements:

Step 2: Project Requirements
============================


Pseudo-Random Generator
-----------------------
As we discussed before, the random numbers are what makes Monte Carlo method
possible. Unfortunately it is not that easy to quickly generate truly random
numbers on a computer. Instead the ``pseudo-random`` generators are used for
this purpose. The problem with the javascript's standard ``Math.random()`` is
that there is no official way to start a random numbers sequence from a certain
seed. Thus, it is impossible to reproduce the sequence hence reproduce and
verify the results.
However there are great javascript libraries for pseudo-random numbers
generation. One of them is the `alea.js`_ library which we are going to use.

So before continuing, please `download <../_static/alea.js>`_
and include ``alea.js`` in project's ``js`` directory.


.. _tutorial-requirements-configuration:

Configuration
-------------
The client-side application configuration is a JSON object passed from the
server to the client when application is initialized on the client side.
It contains shared and application-specific information required for the
project initialization.
What kind of configuration do we need to pass to the client?
First of all, a Node should know the number of random points to be generated.
Second, the project requires the ``alea.js`` library and should be able to load
it. Luckily the standard ``importScripts()`` function is available in HTML5
Web Workers in order to load javascript code. Thus, we just need to pass the
URL of the library. Considering these requirements, the configuration would be
similar to::

  {
      'alea_script' : '/static/projects/monte_carlo_pi/alea.js',
      'random_points' : 100000,
  }

On server-side, the project needs to know the amount of completed *tasks*
that would be enough for the overall calculations.


Tasks and Solutions Data
------------------------
Every random numbers sequence needs a seed to start with. And such unique seed
already exists in every task: it is unique task's ``id`` provided by the project.
For our purpose, even a numerical incremental id is enough to server as a seed.
The returned solution is simpy the calculated value of PI.


The Algorithm
-------------

The algorithm of calculating PI is based on the theory explained in
:ref:`introduction <tutorial-introduction>`::

  let points_counter = 0
  repeat random_points times:
      let x, y be random numbers in (0, 1) range.
      if x^2 + y^2 <= 1 then
          # the points is inside the circle
          points_counter += 1
  pi = 4 * points_counter / random_points

.. _alea.js: http://baagoe.org/en/w/index.php/Better_random_numbers_for_javascript
