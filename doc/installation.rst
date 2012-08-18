.. _installation:

Installation
============

Pre-requirements
----------------

Kaylee is based on the following technologies:

* `Python 2.7 <http://python.org>`_ is required to run Kaylee server.
* `CoffeeScript <http://coffeescript.org>`_ is required only if working with
   Kaylee sources, e.g. for compiling client and projects if they are
   written in CoffeeScript.
* HTML5 Web Workers support is required in browsers in order to run the
  client side of Kaylee and the projects.

Kaylee also requires a server front-end to run. The out-of-the box support
is available for:

* `Flask`_
* `Django`_


virtualenv
----------

Imagine you have an application that
needs version 1 of LibFoo, but another application requires version
2.  How can you use both these applications?  If you install
everything into ``/usr/lib/python2.7/site-packages`` (or whatever your
platform's standard location is), it's easy to end up in a situation
where you unintentionally upgrade an application that shouldn't be
upgraded.

Or more generally, what if you want to install an application *and
leave it be*?  If an application works, any change in its libraries or
the versions of those libraries can break the application.

Also, what if you can't install packages into the global
``site-packages`` directory?  For instance, on a shared host.

In all these cases, ``virtualenv`` can help you.  It creates an
environment that has its own installation directories, that doesn't
share libraries with other virtualenv environments (and optionally
doesn't access the globally installed libraries either).

``virtualenv`` is probably availabale for the Linux distribution you're
currently using, e.g. on Debian and Debian-based (Ubuntu, Mint etc.) systems::

  $ sudo apt-get install python-virtualenv

On \*BSD and MacOSX (or in case that ``virtualenv`` is not available for your
Linux distro) run::

  $ pip install virtualenv

Once you have virtualenv installed, just fire up a shell and create your own
virtual environment. I usually create a project folder and an ``env`` folder
within::

  $ mkdir mykaylee
  $ cd mykaylee
  $ virtualenv env
  Installing distribute..............done.
  Installing pip.....................done.

Now, whenever you want to work on a project, you only have to activate the
corresponding environment::

  $ . env/bin/activate

Now the virtual environment is activated and everything you install via PIP
will end up in it::

  $ pip install kaylee

You can install Kaylee front-end(s) as well::

  $ pip install flask


.. _demo:

Demo
----
To test whether you have install Kaylee successfully, let's run
a demo "Hash cracker" application.

To start the demo activate the virtual environment, run
``python demo/run.py`` from the package and open the browser with the
corresponding address and port (e.g. the default address of Flask is
http://127.0.0.1:5000).

If everything was successful you should see a page with a black rectangle
in the middle which represents an "echo" console. Don't worry, it is a part
of the demo, not Kaylee in general. In a few seconds something weird will
happen and at last you will see something like this:

.. image:: _static/demo2.png
   :align: center
   :alt: Console with HashCracker application output.
   :scale: 75 %
   :width: 800
   :height: 400

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
  ...

.. _Flask: http://flask.pocoo.org/
.. _Django: http://djangoproject.com/
