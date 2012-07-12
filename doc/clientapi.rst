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


Kaylee worker
-------------

.. js:function:: klw.task_completed(result)

   :param result: todo

.. js:function:: klw.log(message)

   :param message: todo


Kaylee global
-------------

.. js:function:: kl.setup(config)

.. [1] http://en.wikipedia.org/wiki/Web_worker_
.. [2] http://www.w3schools.com/html5/html5_webworkers.asp_
