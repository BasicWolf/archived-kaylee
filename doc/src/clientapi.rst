.. _clientapi:

Client API
==========

.. module:: kaylee

This part of the documentation covers all the client-side interfaces of Kaylee.

Projects
--------
There are two kind of Projects available in Kaylee. The ``automatic`` or
simply ``auto`` applications are executed inside a HTML5 web worker
controlled by Kaylee. The ``manual`` or ``DOM-based`` projects are executed
inside the web page's main javascript loop.


Auto projects
.............
A browser which follows a single thread of execution has to wait on
JavaScript programs to finish executing before proceeding and this may take
significant time which the programmer may like to hide from the user.
HTML5 Web Workers allow concurrent execution of the browser threads and one
or more JavaScript threads running in the background. A browser can continue
operating normally while running heavy-performance-dependent javascript
applications in the background [1]_.

Web workers' code is kept and loaded from external javascript files. That is
why they do not have access to the following JavaScript objects [2]_:

* The window object
* The document object
* The parent object

A project which is executed in a Kaylee-controlled web worker and does not
depend on the objects listed above in called an ``Auto`` Kaylee project
(or a project in auto mode). This can be for example a hash-cracking,
complex function optimization, etc. application.


Manual projects
...............

A "manual" project is something that cannot be cannot be calculated
automatically and involves user interaction. 


A typical Kaylee project implements two callbacks in the ``pj`` namespce:

.. js:function:: pj.init(app_config)

   The callback is invoked only once, when the client-side of the
   application is initialized. The long-term resources like scripts and
   stylesheets should be imported here (e.g. via :js:func:`kl.include`).

   :param app_config: JSON-formatted application configuration received
                      from Kaylee server.

.. js:function:: pj.process_task(task)

   The callback is invoked every time a project receives a new task from
   the server. To notify Kaylee that the task has been completed and the
   results are available the :js:func:`kl.task_completed` event should be
   triggered.

   :param task: JSON-formatted task data.


Core
----

.. js:attribute:: kl.api

   This is a very important, a bit complex-syntaxed yet poferwul way
   of lettings the user to define the HTTP API between the server and
   Kaylee client.

   ``kl.api`` is an object with four functions in it:

   * :js:attr:`register <kl.api.register>`
   * :js:attr:`subscribe <kl.api.subscribe>`
   * :js:attr:`get_action <kl.api.get_action>`
   * :js:attr:`send_result <kl.api.send_result>`

   Each of these calls corresponds to a particular method of the
   :py:class:`Kaylee` object on the server side (see :ref:`default-communication`).
   It is expected that the function will trigger a certain event,
   for example::

        kl.api.register = function () {
            kl.get("/kaylee/register", kl.node_registered.trigger);
        }

   .. warning:: Kaylee relies on the corresponding events to be triggered,
                and will fail  to function properly, if the events are not
                triggered at the proper time.

   .. js:attribute:: kl.api.register

      Registers Kaylee node (see :py:meth:`Kaylee.register`).
      Triggers :js:func:`kl.node_registered`.

   .. js:attribute:: kl.api.subscribe(app_name)

      Subscribes the node to an application (see :py:meth:`Kaylee.subscribe`).
      Triggers :js:func:`kl.node_subscribed`.

      :param string app_name: application name.

   .. js:attribute:: kl.api.get_action

      Gets the next available action (see :py:meth:`Kaylee.get_action`).
      Triggers :js:func:`kl.action_received`.

   .. js:attribute:: kl.api.send_result(data)

      Sends task results to the server (see :py:meth:`Kaylee.accept_result`).
      Triggers :js:func:`kl.result_sent` **and** in case that Kaylee
      immediately returns a new action :js:func:`kl.action_received`.



.. js:attribute:: kl.config

   Kaylee nodes-specific config received from the server.
   Currently contains a single attribute:

   * **kl_worker_script** - defines a URL of Kaylee worker script.


.. js:function:: kl.get_action()

   Invokes :js:attr:`kl.api.get_action`.


.. js:attribute:: kl.node_id

   Current node id. Set when a node is registered by the server.


.. js:function:: kl.register()

   Invokes :js:attr:`kl.api.register` after internal benchmark and minimum
   requirements (e.g. availability of web workers) tests.


.. js:function:: kl.send_result(data)

   Invokes :js:attr:`kl.api.send_result`.


.. js:function:: kl.subscribe(app_name)

   Setups :js:attr:`kl.app` and invokes :js:attr:`kl.api.subscribe`.


Events
------

.. js:class:: Event([primary_handler])

   A simple built-in events mechanism. Sample usage::

       // Declare an event
       my_event = new Event();

       // This function will server as an event handler
       on_my_event = function(data) {
           alert(data);
       }

       // Bind handler function to the event
       my_event.bind(on_my_event)

       // Trigger event. This will call subscribed functions
       // in order of subscription.
       my_event.trigger('Event data goes here')

       // Unbind handler from the event.
       my_event.unbind(on_my_event)

   :param function primary_handler: An optional event handler which will
                                    be the first in the handlers queue.


   .. js:function:: bind(handler)

      Bind handler to an event.

   .. js:function:: trigger([arg1, arg2, ...])

      Trigger event. This calls all bound handlers with provided arguments.

   .. js:function:: unbind(handler)

      Unbind handler.


Events tirggered by projects
..............--------------

.. js:function:: kl.project_imported()

   Should be triggered by a project when it has been successfully imported.
   This is usually done in :js:func:`pj.init`.

.. js:function:: kl.task_completed(result)

   Should be triggered by a project when a task is compelted. This is
   usually done in :js:func:`pj.process_task`.

   :param object result: task results (javascript object).


Events triggered by Kaylee
..........................

.. js:function:: kl.action_received(data)

   Triggered when an action from the server is received.
   See :py:meth:`Kaylee.get_action` for more details.

.. js:function:: kl.log(message)

   Triggered when a message requires to be logged.

   :param string message: message to log.

.. js:function:: kl.node_registered(config)

   Triggered when Kaylee registeres the node.

   :param object config: Kaylee configuration.

.. js:function:: kl.node_subscribed(app_config)

   Triggered when the node is subcsribed to an application.

   :param object config: application configuration.

.. js:function:: kl.node_unsubscibed()

   Triggered when Kaylee unsubscribes the node from an application.

.. js:function:: kl.result_sent(result)

   Triggered when Kaylee acknowledges the receipt of the task results.

   :param object result: results sent to the server.

.. js:function:: kl.server_error(message)

   Triggered when a request to server has not been completed successfully
   (e.g. HTTP status 404 or 500).

   :param string message: Error message from the server. This can be used to
                          e.g. log the server error traceback.

.. js:function:: kl.task_received(task)

   Triggered when the client receives a task from the server.

   :param object task: task data.


AJAX
----

The ``AJAX`` module is available in both auto(worker-based) and manual(DOM-based)
projects.

.. js:function:: kl.get( url[, data] [, success(data)] [, error(message)] )

   Invokes asynchronous GET request.

   :param url: request URL
   :param data: JavaScript object which is transformed to a query string
   :param success: callback invoked in case of successful request.
   :param error: callback invoked in of request failure.

   Simple usage case example::

     kl.get('/some/url', function(data) {
       alert(data);
     } );


.. js:function:: kl.post( url [, data] [, success] [, error] )

   Invokes asynchronous POST request with JSON data.

   :param url: request URL
   :param data: JSON object
   :param success: callback invoked in case of successful request.
   :param error: callback invoked in case of request failure.


.. js:function:: kl.include(urls, [, success] [, fail])

   Dynamically imports javascript (``*.js``) or stylesheet ``*.css`` files.
   Importing stylesheets is available for manual projects only.

   :param urls: a single URL or an array of URLs to import.
   :param success: callback invoked in case of successful import.
   :param fail: callback invoked in case of failure (does not work for
                stylesheets!)


.. [1] http://en.wikipedia.org/wiki/Web_worker
.. [2] http://www.w3schools.com/html5/html5_webworkers.asp
