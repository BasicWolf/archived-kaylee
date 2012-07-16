.. _quickstart:

Quickstart
==========

Eager to get started?  This page gives a good introduction in how to get
started with Kaylee. We will first launch a demo application and then
go through the code to see, how Kaylee actually works.
This assumes you already have Kaylee installed.
If you do not, head over to the :ref:`installation` section.

Running the demo application
----------------------------
Kaylee is designed to easily interact with any Python web framework.
Out of the box Kaylee contains extensions for
`Flask <http://flask.pocoo.org/>`_ and `Django <http://djangoproject.com/>`_
frameworks.
To start the demo run `src/bin/run.py` from the package and open
the browser with the corresponding address and port (e.g. the address
for the default Flask built-in is http://127.0.0.1:5000).

If everything was successful you should see a page with a black rectangle
in the middle which represents an "echo" console. Don't worry, it's part
of the demo, not Kaylee in general. In few seconds something weird will
happen and at last you will see something like this:

|demo2|

Congratulations! You've just cracked a salted MD5 hash. 
If you scroll the console on the web page
to the top, you'll see the steps of project's initialization process.
Finally, check out the shell, you may notice a message from Kaylee
which says what the cracked hash key was::

  * Running on http://127.0.0.1:5000/
  * Restarting with reloader
  127.0.0.1 - "GET / HTTP/1.1" 200 -
  127.0.0.1 - "GET /static/css/all.css HTTP/1.1" 200 -
  127.0.0.1 - "GET /static/js/lib/jquery.min.js HTTP/1.1" 200 -
  127.0.0.1 - "GET /static/js/kaylee/kaylee.js HTTP/1.1" 200 -
  127.0.0.1 - "GET /static/js/kaylee/klconsole.js HTTP/1.1" 200 -
  127.0.0.1 - "GET /static/js/kaylee/kldemo.js HTTP/1.1" 200 -
  127.0.0.1 - "GET /kaylee/register HTTP/1.1" 200 -
  127.0.0.1 - "POST /kaylee/apps/hash_cracker.1/subscribe/500315e30000f528764d HTTP/1.1" 200 -
  127.0.0.1 - "GET /kaylee/actions/500315e30000f528764d HTTP/1.1" 200 -
  127.0.0.1 - "POST /kaylee/actions/500315e30000f528764d HTTP/1.1" 200 -
  127.0.0.1 - "POST /kaylee/actions/500315e30000f528764d HTTP/1.1" 200 -
  The cracked hash key is: kl
  127.0.0.1 - "POST /kaylee/actions/500315e30000f528764d HTTP/1.1" 200 -


.. |demo2| image:: /images/demo2.png
    :align: middle
    :alt: Console with HashCracker application output.

It is time to find out, how the heck does Kaylee work.


Server and Nodes
----------------

Kaylee is divided in two parts: the server-side Python brains which controls
the tasks distribution and results collection and client-side
(browser-side) JavaScript Nodes which do the dirty computation work.

The server performs the following routines:

  * Registers the nodes.
  * Subscribes the nodes to applications.
  * Dispatches the tasks to the nodes.
  * Collects the results from the odes.

There are multiple simple and complex sub-routines among this large ones,
but we will talk about them later.

Kaylee Nodes exploit the new HTML5 Web Workers [1]_ in order to avoid
interfering with browser's main JavaScript event loop.
After registering and subscribing to Kaylee application, a Node has a single
job to do: solve given tasks and report the results.



.. [1] http://www.w3schools.com/html5/html5_webworkers.asp
