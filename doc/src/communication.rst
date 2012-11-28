.. _communication:

Kaylee communication
====================

.. _default-communication:

Default API
...........

Although Kaylee comes with a default communication API, a user is free to
communicate with Kaylee in any way possible as long as the transferred data
is kept in JSON format. The default API is implemented on both server
(:ref:`contrib front-ends <contrib_front_ends>`) and client side
(:js:attr:`kl.api`) is described below.

.. module:: kaylee

Register
--------

=========== ==========================
Server      :py:meth:`Kaylee.register`
Client      :js:attr:`kl.api.register`
URL         ``/kaylee/register``
HTTP Method ``GET``
=========== ==========================


Subscribe
---------

=========== ===============================================
Server      :py:meth:`Kaylee.subscribe`
Client      :js:attr:`kl.api.subscribe`
URL         ``/kaylee/apps/{app_name}/subscribe/{node_id}``
HTTP Method ``POST``
POST data   null
Parameters  * ``app_name`` - Application name to which the
              node is being subscribed.
            * ``node_id`` - Node ID.
=========== ===============================================


Get Action
----------

=========== =============================
Server      :py:meth:`Kaylee.get_action`
Client      :js:attr:`kl.api.get_action`
URL         ``/kaylee/actions/{node_id}``
HTTP Method ``GET``
Parameters  * ``node_id`` - Node ID.
=========== =============================


Accept Results
--------------

=========== ===============================
Server      :py:meth:`Kaylee.accept_result`
Client      :js:attr:`kl.api.send_result`
URL         ``/kaylee/actions/{node_id}``
HTTP Method ``POST``
Post Data   Calculation results.
=========== ===============================



Tasks and results data flow
...........................

As it has been mentioned many times, Kaylee communicates via JSON. On
server-side a task data returned by a ``Project`` is a ``dict`` with a
mandatory ``id`` key in it. The type of ``task['id']`` is *string*::

  { 'id' : 't1' }


\
\
