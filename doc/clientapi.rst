.. _clientapi:

Client API
==========

This part of the documentation covers all the client-side interfaces of Kaylee.

Kaylee Projects
---------------
A typical project implements two functions in the `pj` namespce:

.. js:function:: pj.init(kl_config, app_config)

   The function is called only once, when the client-side of the
   application is initialized. 

   :param kl_config: Kaylee configuration set by :js:func:`kl.setup`  :param app_config: Application config recieved from Kaylee server
   

Kaylee global
-------------

.. js:function:: kl.setup(config)

