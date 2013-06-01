.. _contrib:

Contrib
=======

.. module:: kaylee

Kaylee comes with a small ``contrib`` package which currently plays a role
of :py:class:`Controller`, :py:class:`TemporalStorage` and
:py:class:`PermanentStorage` implementation examples.

Contrib also contains Werkzeug, Flask and Django applications which support
the :ref:`default communication API <default-communication>`.

.. _contrib_front_ends:

Front-ends
----------

Flask
.....

Kaylee provides Flask ``blueprint`` which can be used in the following
fashion::

  from flask import Flask
  from kaylee.contrib.frontends.flask_frontend import kaylee_blueprint

  app = Flask(__name__)

  app.register_blueprint(kaylee_blueprint,
                         url_prefix='/kaylee')


Django
......

Kaylee provides Django ``application`` which can be used in the following
fashion::

  # Project's urls.py

  from django.conf.urls import patterns, include, url

  urlpatterns = patterns('',
      # ...,
      url(r'^kaylee/', include('kaylee.contrib.frontends.django_frontend.urls'))
  )


Werkzeug
........

Kaylee provides Werkzeug ``werkzeug.routing.Map`` object as follows::

  from kaylee.contrib.frontends.werkzeug_frontend import make_url_map

  my_map = make_url_map(url_prefix='/kaylee')


Controllers
-----------

.. module:: kaylee.contrib

.. autoclass:: SimpleController

.. autoclass:: ResultsComparatorController

See :ref:`Controller API <controllersapi>` for more details.

Storages
--------

.. autoclass:: MemoryTemporalStorage

.. autoclass:: MemoryPermanentStorage

See :ref:`Storages API <storagesapi>` for more details.
