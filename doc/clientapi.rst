.. _clientapi:

Client API
==========

This part of the documentation covers all the client-side interfaces of Kaylee.

Kaylee Projects
---------------
Kaylee distrubuted application are executed via Web workers introduced in
HTML5 web standard.

Web Workers allow for concurrent execution of the browser threads and one
or more JavaScript threads running in the background.
The browser which follows a single thread of execution will have to wait on
JavaScript programs to finish executing before proceeding and this may take
significant time which the programmer may like to hide from the user.
It allows for the browser to continue with normal operation while running in
the background [1]_.

Since web workers are in external files, they do not have access to the
following JavaScript objects [2]_:

* The window object
* The document object
* The parent object


A typical Kaylee project implements two callbacks in the `pj` namespce:

.. js:function:: pj.init(kl_config, app_config)

   The function is called only once, when the client-side of the
   application is initialized. You can import required libraries via
   `importScript()` here.

   :param kl_config: JSON-formatted Kaylee configuration set by
                     :js:func:`kl.setup`
   :param app_config: JSON-formatted application configuration recieved
                      from Kaylee server.

.. js:function:: pj.on_task_recieved(data)

   This function is called every time when a project recieves a new task
   from the server. :js:func:`klw.task_completed` is then used to notify
   Kaylee that the results of the task are available and they can be sent
   to the server.

   :param data: JSON-formatted task data.


Kaylee Worker
-------------

.. js:function:: klw.task_completed(result)

   :param result: todo

.. js:function:: klw.log(message)

   :param message: todo


Kaylee Global
-------------

.. js:function:: kl.setup(config)

Kaylee Events
-------------

.. js:function:: kl.log(message)

   Triggered when a message requires to be logged.

   :param message: message to log.

.. js:function:: kl.node_registered(config)

   Triggered when Kaylee registeres the node.

   :param config: Kaylee configuration.

.. js:function:: kl.node_subscribed(app_config)

   Triggered when Kaylee subcsribes the node to an application.

   :param config: application configuration.

.. js:function:: kl.node_unsubscibed()

   Triggered when Kaylee unsubscribes the node from an application.

.. js:function:: kl.project_imported()

   Triggered when Kaylee worker finishes importing a project required
   by an application (this includes successful call to :js:func:`pj.init`).

.. js:function:: kl.results_sent()

   Triggered when Kaylee acknowledge the receipt of the task results.


.. js:function:: kl.server_raised_error(message)

   Triggered when a request to server has not been completed successfully (e.g. HTTP status 404 or 500).

   :param message: Error message.

.. js:function:: kl.task_completed(result)

   :param result: task results. Triggered by :js:func:`klw.task_completed`.

.. js:function:: kl.task_recieved(data)

   Triggered when the client recieves a task from the server.

   :param data: task data.

.. js:function:: kl.worker_raised_error(error)

   Triggered when Kaylee worker raises an error.

   :param error: error object. Available fields:

                 * filename
                 * lineno
                 * message


.. [1] http://en.wikipedia.org/wiki/Web_worker
.. [2] http://www.w3schools.com/html5/html5_webworkers.asp

