.. _communication:

Kaylee communication
====================

.. _default-communication:

Default API
-----------

Although Kaylee comes with a default communication API, a user is free to
communicate with Kaylee in any way possible as long as the transferred data
is kept in JSON format. The default API is implemented on both server
(:ref:`contrib front-ends <contrib_front_ends>`) and client side
(:js:attr:`kl.api`) is described below.

.. module:: kaylee

Register
........

=========== ==========================
Server      :py:meth:`Kaylee.register`
Client      :js:attr:`kl.api.register`
URL         ``/kaylee/register``
HTTP Method ``GET``
=========== ==========================


Subscribe
.........

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
..........

=========== =============================
Server      :py:meth:`Kaylee.get_action`
Client      :js:attr:`kl.api.get_action`
URL         ``/kaylee/actions/{node_id}``
HTTP Method ``GET``
Parameters  * ``node_id`` - Node ID.
=========== =============================


Accept Results
..............

=========== ===============================
Server      :py:meth:`Kaylee.accept_result`
Client      :js:attr:`kl.api.send_result`
URL         ``/kaylee/actions/{node_id}``
HTTP Method ``POST``
Post Data   Calculation results.
=========== ===============================



Tasks and results
-----------------

As it has been mentioned many times, Kaylee communicates via JSON. On
server-side a task data returned by a ``Project`` is a JSON-serializable
``dict`` with a mandatory ``id`` key in it::

  { 'id' : 't1' }

.. note:: The value of ``task['id']`` is always  automaically converted to
          *string*.

A solution is any valid JSON-deserializable data.


Session data
............

The famous `reRECAPTCHA`_ provides a very efficient CAPTCHA mechanism and
at the same time it helps decyphering books. There are two words which
should be recognized and entered by the user. One of the words is a piece
of a scanned book page, while another is generated artificially.
It means that reCAPTCHA has to "remember" that a particular user has
recieved a particular artificial word in order to validate the user's input.

How would one solve a similar problem via Kaylee? One way would be saving
the session data on server-side by sticking it to the Node data.

The problem
of this approach is that a :cls:`NodesRegistry` may not be able to contain user may session data may contain

Well, it is possible to
generate the following task::

  {
      'id' : '1',
      'image_path' : 'http:/my.site.com/captcha/tmp/ahU2jcXz.jpg',
      'artificial_word' : 'sunlight'
  }

And return the following results::

  {
      '
  }

.. _reCAPTCHA: http://recaptcha.net
