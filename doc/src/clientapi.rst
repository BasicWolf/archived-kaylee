.. _clientapi:

Client API
==========

.. module:: kaylee

This part of the documentation covers all the client-side interfaces of Kaylee.

Projects
--------

A typical Kaylee project implements two callbacks in the ``pj`` namespce:

.. js:function:: pj.init(app_config)

   The callback is invoked only once, when the client-side of the
   application is initialized. The long-term resources like scripts and
   stylesheets should be imported here (e.g. via :js:func:`kl.include`)
   then, the :js:attr:`kl.project_imported` event should be triggered,
   for example:

   .. code-block:: coffeescript

      pj.init = (app_config) ->
          pj._config = app_config  # store config for later use
          to_include = [app_config.some_script.js,
                        app_config.another_script.js,
                        app_config.some_stylesheet.css]
          kl.include(to_include, kl.project_imported.trigger)

   Or, if there are no resources to import:

   .. code-block:: coffeescript

      pj.init = (app_config) ->
          pj._config = app_config
          kl.project_imported.trigger()


   :param app_config: JSON-formatted application configuration received
                      from the server-side of the project (see
                      :attr:`Project.client_config`)

.. js:function:: pj.process_task(task)

   The callback is invoked every time a project receives a new task from
   the server. To notify Kaylee that the task has been completed and the
   results are available the :js:attr:`kl.task_completed` event should be
   triggered.

   :param task: JSON-formatted task data.


Core
----

.. js:attribute:: kl.api

   Contains the function-attributes which define the HTTP API between the
   server and Kaylee client. ``kl.api`` is an object with four functions
   in it:

   * :js:attr:`register <kl.api.register>`
   * :js:attr:`subscribe <kl.api.subscribe>`
   * :js:attr:`get_action <kl.api.get_action>`
   * :js:attr:`send_result <kl.api.send_result>`

   Each of these calls corresponds to a particular method of the
   core :py:class:`Kaylee` object on the server side
   (see :ref:`default-communication`). It is expected that the
   function will trigger a certain event, for example:

   .. code-block:: coffeescript

        kl.api.register = () ->
            kl.get('/kaylee/register', kl.node_registered.trigger)

   .. warning:: Kaylee relies on the corresponding events to be triggered,
                and will fail  to function properly, if the events are not
                triggered at the proper time.

   .. js:attribute:: kl.api.register

      Registers Kaylee node (see :py:meth:`Kaylee.register`).
      Triggers :js:attr:`kl.node_registered`.

   .. js:attribute:: kl.api.subscribe(app_name)

      Subscribes the node to an application (see :py:meth:`Kaylee.subscribe`).
      Triggers :js:attr:`kl.node_subscribed`.

   .. js:attribute:: kl.api.get_action

      Gets the next available action (see :py:meth:`Kaylee.get_action`).
      Triggers :js:attr:`kl.action_received`.

   .. js:attribute:: kl.api.send_result(data)

      Sends task results to the server (see :py:meth:`Kaylee.accept_result`).
      Triggers :js:attr:`kl.result_sent` **and** in case that Kaylee
      immediately returns a new action :js:attr:`kl.action_received`.

.. js:attribute:: kl.config

   Kaylee client config received from the server after the node has been
   registered. For full configuration description see
   :ref:`configuration`.

.. js:function:: kl.error(message)

   Logs the message with "ERROR: " prefix and **throws**
   :js:class:`kl.KayleeError`. This means that if ``kl.error`` is called
   outside a ``try..catch`` block the exception will be thrown further unless
   it reaches the global scope. ``kl.error()`` should be called only in case
   that something went completely wrong and it is not wise to continue
   running Kaylee on the Node.
   For example ``kl.error()`` is called by Kaylee when the incoming or
   outgoing data is malformed.

.. js:class:: kl.KayleeError(message)

   Kaylee generic error class, extends ``Error``. The class should not be
   thrown directly, instead use :js:func:`kl.error`.

.. js:function:: kl.log(message)

   Logs the message to browser console and triggers
   :js:attr:`kl.message_logged`.

.. js:attribute:: kl.node_id

   Current node id. Set when after the node has been registered by the server.

Events
------

.. js:class:: Event([primary_handler])

   A simple built-in events mechanism. Sample usage:

   .. code-block:: coffeescript

       # Declare an event
       my_event = new Event()

       # This function will serve as an event handler
       on_my_event = (data) ->
           alert(data)

       # Bind the handler function to the event
       my_event.bind(on_my_event)

       # Trigger the event. This will call the subscribed handlers
       # in order of subscription (e.g. fist-to-subscribe will be
       # called first).
       my_event.trigger('Event data goes here')

       # Unbind handler from the event.
       my_event.unbind(on_my_event)

   :param function primary_handler: an optional event handler which will
                                    be the first in the handlers queue


   .. js:function:: bind(handler)

      Binds a handler to the event.

   .. js:function:: trigger([arg1, arg2, ...])

      Triggers the event. This calls all bound handlers with the provided
      arguments.

   .. js:function:: unbind(handler)

      Unbinds the handler.


Events tirggered by projects
............................

.. js:function:: kl.project_imported()

   Should be triggered by a project when it has been successfully imported.
   This is usually done in :js:func:`pj.init`.

.. js:function:: kl.task_completed(result)

   Should be triggered by a project when a task is compelted. This is
   usually done in :js:func:`pj.process_task`.

   :param result: Task results (javascript object).


Events triggered by Kaylee
..........................

The events below are the basic Kaylee client-side logic events and should
**not** be triggered by the user's project code in order to avoid unpredictable
behaviour. Nevertheless, feel free to bind to these events to the code outside
of the project and track how Kaylee works internally.

For example, the following code will echo all log messages to the browser
console:

   .. code-block:: coffeescript

       kl.message_logged.bind(console.log)

In the following example the total amount of tasks is kept in a counter:

   .. code-block:: coffeescript

      tasks_count = 0

      kl.task_received.bind( (task) -> tasks_count += 1 )

.. js:function:: kl.action_received

   Triggered when an action is received from the server.
   See :py:meth:`Kaylee.get_action` for more details.

   :param action: The action data received from the server.

.. js:function:: kl.node_registered(config)

   Triggered when the node has been successfully registered on the server.

   :param config: Kaylee configuration

.. js:function:: kl.node_subscribed(app_config)

   Triggered when the node has been subcsribed to an application.

   :param app_config: Application configuration.

.. js:function:: kl.node_unsubscibed()

   Triggered when Kaylee has unsubscribed the node from an application.

.. js:function:: kl.message_logged(message)

   Triggered by :js:func:`kl.log`.

   :param message: The logged message.

.. js:function:: kl.result_sent(result)

   Triggered when Kaylee acknowledges receiving the result.

   :param result: The result sent to the server.

.. js:function:: kl.server_error(message)

   Triggered when a request to server has not been completed successfully
   (e.g. HTTP status 404 or 500).

   :param message: Error message from the server. This can be used to
                   e.g. log the server error traceback

.. js:function:: kl.task_received(task)

   Triggered when the client receives a task from the server.

   :param task: The received task.


AJAX
----

The ``AJAX`` module provides convenient way to make ``GET/POST`` requests to
the server. It also provides routines to load javascript and stylesheet files
on-fly. The functions are accessible by both auto(worker-based) and
manual(DOM-based) projects.

.. js:function:: kl.get( url [, data] [, success(data)] [, fail(message)] )

   Invokes asynchronous GET request.

   :param url: Request URL.
   :param data: JavaScript object which is transformed to a query string.
   :param success: The callback invoked in case of successful request.
   :param fail: The callback invoked in of request failure.

   Simple usage:

   .. code-block:: coffeescript

     kl.get('/some/url', (data) ->
         alert(data)
     )



.. js:function:: kl.post( url [, data] [, success] [, fail] )

   Invokes asynchronous POST request with JSON data.

   :param url: Request URL.
   :param data: JSON object.
   :param success: The callback invoked in case of successful request.
   :param fail: The callback invoked in case of request failure.


.. js:function:: kl.include(urls, [, success] [, fail])

   Dynamically imports javascript (``*.js``) or stylesheet ``*.css`` files.
   Importing stylesheets is available for manual projects only.

   :param urls: A single URL or an *array* of URLs to import.
   :param success: The callback invoked in case of successful import.
   :param fail: The callback invoked in case of failure (does not work for
                stylesheets!).
