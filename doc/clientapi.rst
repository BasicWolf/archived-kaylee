.. _clientapi:

Client API
==========

.. module:: kaylee

This part of the documentation covers all the client-side interfaces of Kaylee.

Projects
--------
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

   :param kl_config: JSON-formatted Kaylee config set by
                       :js:func:`kl.setup`
   :param app_config: JSON-formatted application configuration received
                      from Kaylee server.

.. js:function:: pj.on_task_received(data)

   This function is called every time when a project receives a new task
   from the server. :js:func:`klw.task_completed` is then used to notify
   Kaylee that the results of the task are available and they can be sent
   to the server.

   :param data: JSON-formatted task data.


.. _client_workerapi:

Worker
------

.. js:function:: klw.task_completed(result)

   :param result: todo

.. js:function:: klw.log(message)

   :param message: todo


Core
----

.. js:attribute:: kl.api

   This is a very important complex-syntaxed yet poferwul way
   of lettings a user to define the HTTP API between the server and
   Kaylee client.

   `kl.api` is an object with four function attributes:

   * :js:attr:`register <kl.api.register>`
   * :js:attr:`subscribe <kl.api.subscribe>`
   * :js:attr:`get_action <kl.api.get_action>`
   * :js:attr:`send_results <kl.api.send_results>`

   Each of these calls corresponds to a particular method of the
   :py:class:`Kaylee` object on the server side. The default (TODO)
   Kaylee API is:...
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

      Gets next available action (see :py:meth:`Kaylee.get_action`).
      Triggers :js:func:`kl.action_received`.

   .. js:attribute:: kl.api.send_results(data)

      Sends task results to the server (see :py:meth:`Kaylee.accept_result`).
      Triggers :js:func:`kl.results_sent` **and** in case that Kaylee
      immediately returns a new action :js:func:`kl.action_received`.


.. js:attribute:: kl.node_id

   Current node id. Set when a node is registered by the server.

.. js:attribute:: kl.config

   Kaylee nodes-specific config received from the server.
   Currently contains a single attribute (TODO):

   * **kl_worker_script** - defines a URL of Kaylee worker script.

   The configuration is transfered to the project via :js:func:`pj.init`.

.. js:attribute:: kl.app

   `kl.app` is an object which contains active application data.

   The attributes of the object are:

   * **name** - application name, which is set *before* the server subscribes
     the node to an application.
   * **config** - application configuration object which is received from
     the server as a response to subscription request. It is later transfered
     to the project via :js:func:`pj.init`.
   * **subscribed** - a boolean flag which indicates whether the app is
     subscribed or not. It is set to `true` if subscription was succcessful
     and to `false` when the node is unsubscribed.
   * **worker** - the active Worker object.

   .. note:: This object is meant to be readonly.



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

   Triggered when Kaylee subcsribes the node to an application.

   :param object config: application configuration.

.. js:function:: kl.node_unsubscibed()

   Triggered when Kaylee unsubscribes the node from an application.

.. js:function:: kl.project_imported()

   Triggered when Kaylee worker finishes importing a project required
   by an application (this includes successful call to :js:func:`pj.init`).

.. js:function:: kl.results_sent(results)

   Triggered when Kaylee acknowledge the receipt of the task results.

   :param object data: results sent to the server.

.. js:function:: kl.server_raised_error(message)

   Triggered when a request to server has not been completed successfully
   (e.g. HTTP status 404 or 500).

   :param string message: Error message.

.. js:function:: kl.task_completed(result)

   :param object result: task results. Triggered by :js:func:`klw.task_completed`.

.. js:function:: kl.task_received(data)

   Triggered when the client receives a task from the server.

   :param object data: task data.

.. js:function:: kl.worker_raised_error(error)

   Triggered when Kaylee worker raises an error.

   :param object error: error information object. Available fields:

                        * filename
                        * lineno
                        * message


.. [1] http://en.wikipedia.org/wiki/Web_worker
.. [2] http://www.w3schools.com/html5/html5_webworkers.asp

