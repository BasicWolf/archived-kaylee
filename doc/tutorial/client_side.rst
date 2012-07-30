.. _tutorial-client-side:

Step X: Client-Side Code
========================

Pseudo-random generator
-----------------------
As we discussed before, the random numbers are what makes Monte Carlo method
to work. The problem with the javascript's standard `Math.random()` is that
there is no official way to start a random numbers sequence from a certain
seed. Thus, it is impossible to reproduce the sequence hence reproduce and
verify the results.
However there are great javascript libraries for pseudo-random numbers
generation. One of them is the `alea.js`_ library which we are going to use.

So before writing the client-side code please `download <../_static/alea.js>`_
and include `alea.js` in project's `js` directory.



.. _alea.js: http://baagoe.org/en/w/index.php/Better_random_numbers_for_javascript
