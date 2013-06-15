.. _installation:

Installation
============

Pre-requirements
----------------

Kaylee is based on the following technologies:

* `Python 2.7 <http://python.org>`_. Kaylee is mainly written in Python.
* `Werkzeug`_. The built-in test server utilizes the Werkzeug framework.
* `CoffeeScript <http://coffeescript.org>`_. The client side of Kaylee is
  written in CoffeeScript which compiles into JavaScript. Yet, a user
  is free to write the client-side of the applications in *vanilla
  JavaScript*, *ClojureScript*, *JTalk*, *CoffeeScript* and any other
  programming language that is translated (compiled) into JavaScript and
  understood by the modern browsers.
* `HTML5 Web Workers <http://en.wikipedia.org/wiki/Web_worker>`_. This
  technology enables executing JavaScript code in parallel with the
  browser's main JavaScript event loop. Kaylee client is able to execute
  user project's code in a web worker.

Kaylee also requires a server front-end to run. The out-of-the box support
is available for:

* `Werkzeug`_
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

In all these cases, `virtualenv`_ can help you.  It creates an
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
  $ virtualenv env --system-site-packages
  Installing distribute..............done.
  Installing pip.....................done.

The ``--system-site-packages`` option tells the virtual environment to give
access to the global site-packages dir (e.g. for global python-imaging
or python-crypto access).

Now, whenever you want to work on a project, you only have to activate the
corresponding environment::

  $ . env/bin/activate

Now the virtual environment is activated and everything you install via PIP
will end up in it::

  $ pip install kaylee

You can install the supported front-end(s) as well::

  $ pip install flask django


Demo projects
-------------

All Kaylee demo projects as well as instructions to setup and run
the demo environment are available in the following Github repository:
http://github.com/BasicWolf/kaylee-demo-projects

|

Continue with :ref:`basics`.

.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Flask: http://flask.pocoo.org
.. _Django: http://djangoproject.com
.. _virtualenv: http://www.virtualenv.org
