.. _communication:

Kaylee communication
====================

.. module:: kaylee

Tasks and results
-----------------

As it has been mentioned many times, Kaylee communicates via JSON. On the
server-side a task data returned by a Project is a JSON-serializable dict
with a mandatory ``id`` key in it::

  { 'id' : 't1' }

.. note:: The value of ``task['id']`` is always automatically converted to
          *string*.

The result returned by the client side of a project should be also formatted
in a dict-like (JavaScript object) manner::

  { 'speed' : 30, 'acceleration' : 10 }


Session data
------------

The famous `reCAPTCHA`_ project provides a very efficient CAPTCHA mechanism
and at the same time helps digitizing the text from paper books. reCAPTCHA
gives a task of recognizing two words from a picture. One of the words
is a piece of a scanned book page, while another is generated artificially.
`reCAPTCHA` has to remember that a particular user has received a particular
artificial word in order to validate the input.

How would one solve a similar problem with Kaylee? Kaylee has an efficient
and simple
:class:`Session data managers <kaylee.session.SessionDataManager>`
mechanism to keep Kaylee <-> Node session data between getting a task and
accepting a result requests. In case of solving the `reCAPTCHA` issue, the
artificial word should be stored as a session variable.

In order to become a `session variable`, the variable's name should start
with a hash (``'#'``) symbol, for example::

  task = {
      'id' : '1',
      'image_path' : 'http:/my.site.com/captcha/tmp/ahU2jcXz.jpg',
      '#artificial_word' : 'abyrvalg'
  }

The session data manager scans the outgoing tasks and stores all the session
variables unless the Node returns a result. In other words, before the above
task is dispatched to the Node, it is stripped of the session variables::

  {
      'id' : '1',
      'image_path' : 'http:/my.site.com/captcha/tmp/ahU2jcXz.jpg',
  }

The session variable is attached to the result the moment it arrives to the
server::

  {
      'word1' : 'Enormous',
      'word2' : 'abyrvalg', # this one has been entered by a user
      '#artificial_word' : 'abyrvalg' # this one is the session data
  }


Built-in session data managers
..............................



Currently there are three session data managers available out of the box:

* :class:`PhonySessionDataManager <kaylee.session.PhonySessionDataManager>`
  - the default manager which throws :class:`KayleeError` if a task contains
  session variables.

* :class:`NodeSessionDataManager <kaylee.session.NodeSessionDataManager>`
  - keeps the session data attached to :attr:`Node.session_data`.

* :class:`JSONSessionDataManager <kaylee.session.JSONSessionDataManager>`
  - transfers an encrypted session data among the tasks and results,
  without keeping any data on the server.



.. _default-communication:

Default API
-----------

Although Kaylee comes with a default communication API, the user is free to
communicate with Kaylee in any way possible as long as the transferred data
is kept in JSON format. The default API implemented on both contrib front-ends
(:ref:`contrib front-ends <contrib_front_ends>`) and client side
(:js:attr:`kl.api`) is described below.

Register
........

=========== ==========================
Server      :py:meth:`Kaylee.register`
Client      :js:func:`kl.api.register`
URL         ``/kaylee/register``
HTTP Method ``GET``
=========== ==========================


Subscribe
.........

=========== ===============================================
Server      :py:meth:`Kaylee.subscribe`
Client      :js:func:`kl.api.subscribe`
URL         ``/kaylee/apps/{app_name}/subscribe/{node_id}``
HTTP Method ``POST``
POST data   null
Parameters  * ``app_name`` - Application name to which the
              node is being subscribed.
            * ``node_id`` - Node ID.
=========== ===============================================


Get Action
..........

=========== =============================
Server      :py:meth:`Kaylee.get_action`
Client      :js:func:`kl.api.get_action`
URL         ``/kaylee/actions/{node_id}``
HTTP Method ``GET``
Parameters  * ``node_id`` - Node ID.
=========== =============================


Accept Results
..............

=========== ===============================
Server      :py:meth:`Kaylee.accept_result`
Client      :js:func:`kl.api.send_result`
URL         ``/kaylee/actions/{node_id}``
HTTP Method ``POST``
Post Data   Calculation results.
Parameters  * ``node_id`` - Node ID.
=========== ===============================

|
|
|

.. _reCAPTCHA: http://recaptcha.net
