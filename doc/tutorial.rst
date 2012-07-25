.. _tutorial:

Tutorial
========
The easiest way to start with Kaylee is to dive into a simple distributed
computing application. In this tutorial we are going to examine an application
which computes the value of PI via the `Monte Carlo method`_.

First, lets write down the requirements for the application:

1. The Monte Carlo method is based on a sequence of random numbers.
   The problem with the standard `Math.random()` is that there is no official
   way to start the sequence from a certain seed. Thus, it is impossible to
   reproduce the random sequence hence reproduce and verify the results.
   We're going to use a 3d party `alea.js`_ library in order to generate
   pseudo-random number sequences.

2. 


.. toctree::
   :maxdepth: 2


.. _Monte Carlo method: http://math.fullerton.edu/mathews/n2003/montecarlopimod.html
.. _alea.js: http://baagoe.com/en/RandomMusings/javascript/
