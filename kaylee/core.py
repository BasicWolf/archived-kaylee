# -*- coding: utf-8 -*-
"""
    kaylee.core
    ~~~~~~~~~~~

    This module implements Kaylee's lower level front-end which could
    be easily used with any web framework.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import sys
import json
import traceback
import logging
from StringIO import StringIO
from operator import attrgetter
from functools import partial
from contextlib import closing
from functools import wraps

from .node import Node, NodeID
from .errors import KayleeError, InvalidResultError

log = logging.getLogger(__name__)

#: Returns the results of :function:`json.dumps` in compact encoding
json.dumps = partial(json.dumps, separators=(',', ':'))


def json_error_handler(f):
    """A decorator that wraps a function into try..catch block and returns
    JSON-formatted "{ error : str(Exception) }" if an exception has been
    raised.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            exc_str = str(e)

            if log.getEffectiveLevel() == logging.DEBUG:
                with closing(StringIO()) as buf:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback,
                                       limit = None,
                                       file = buf)
                    exc_str += '\n' + buf.getvalue()
            return json.dumps({ 'error' : exc_str })

    return wrapper


class Kaylee(object):
    """The Kaylee class serves as a layer between WSGI framework and Kaylee
    applications. It handles requests from clients and returns JSON-formatted
    data.

    .. note:: It is the job of a particular front-end to set the
              response content-type to "application/json".

    A convenient way of creating ``Kaylee`` object is via
    :meth:`kaylee.loader.load` factory.

    :param registry: an instance of :class:`NodesRegistry`.
    :param applications: a list of applications (:class:`Controller`
                         instances).
    :param kwargs: Kaylee configuration arguments.
    """
    def __init__(self, registry, applications = None, **kwargs):
        #: An instance of :class:`Config` with Kaylee configuration parsed
        #: from ``**kwargs``. The configuration parameters are accessed as
        #: follows:::
        #: kl.config.CONFIG_PARAMETER
        self.config = Config(**kwargs)
        self._registry = registry
        self._applications = Applications(applications) or Applications.empty()

    @json_error_handler
    def register(self, remote_host):
        """Registers the remote host as Kaylee Node and returns
        JSON-formatted data with the following fields:

        * node_id - hex-formatted node id
        * config  - global nodes configuration (see :mod:`loader` module)
        * applications - a list of Kaylee applications' names.

        :param remote_host: an IP address of the remote host
        :type remote_host: string
        """
        node = Node(NodeID.for_host(remote_host))
        self._registry.add(node)
        return json.dumps ({ 'node_id' : str(node.id),
                             'config' : self.config.to_dict(),
                             'applications' : self._applications.names } )

    @json_error_handler
    def unregister(self, node_id):
        """Remove the node from Kaylee. Kaylee will reject any further
        requests from the node unless it registers again.

        :param node_id: a valid node id
        :type node_id: string
        """
        del self._registry[node_id]

    @json_error_handler
    def subscribe(self, node_id, application):
        """Subscribe a node to an application. In practice it means that
        Kaylee will send task from particular application to this node.
        When a node subscribes to an application it received the its
        configuration defined for nodes.

        :param node_id: a valid node id
        :param application: registered Kaylee application name
        :type node_id: string
        :type application: string
        :returns: jsonified node configuration
        """
        try:
            node = self._registry[node_id]
        except KeyError:
            raise KayleeError('Node "{}" is not registered'.format(node_id))

        try:
            app = self._applications[application]
            return json.dumps( app.subscribe(node) )
        except KeyError:
            raise KayleeError('Application "{}" was not found'.format(app))

    @json_error_handler
    def unsubscribe(self, node_id):
        """Unsubscribes the node from the bound application.

        :param node_id: a valid node id
        :type node_id: string
        """
        self._registry[node_id].unsubscribe()

    @json_error_handler
    def get_action(self, node_id):
        """Returns an action (usually a task from the subscribed application).
        The format of the JSON response is::

          {
              'action' : <action>,
              'data'   : <data>
          }

        Here, <action> tells the Node, what should it do and <data> is
        the attached data. The available values of <action> are:

        * **"task"** - indicated that <data> contains task data
        * **"unsubscribe"** - indicates that there is no need for the Node to
          request tasks from the subscribed application anymore.

        :param node_id: a valid node id
        :type node_id: string
        """
        node = self._registry[node_id]
        try:
            data = node.get_task().serialize()
            return self._json_action('task', data)
        except StopIteration as e:
            self.unsubscribe(node)
            return self._json_action('unsubscribe',
                'The node has been automatically unsubscribed: {}.'.format(e))

    @json_error_handler
    def accept_result(self, node_id, data):
        """Accepts the results from the node. Returns the next action if
        :py:attr:`Config.AUTO_GET_ACTION` is True.
        Otherwise returns "pass" action.
        Unsubscribes the node if the returned result is invalid.

        :param node_id: a valid node id
        :param data: the data returned by the node. This data will be later
                     normalized and validated by the project and then
                     stored to the application's storages.
        :type node_id: string or JSON-parsed dict/list
        :type data: string
        :returns: a task returned by :meth:`get_action` or "pass" action.
        """
        node = self._registry[node_id]
        try:
            # parse data if it is still a JSON string
            if isinstance(data, basestring):
                data = json.loads(data)
            node.accept_result(data)
        except ValueError as e:
            self.unsubscribe(node)
            raise InvalidResultError(data, str(e))

        if self.config.AUTO_GET_ACTION:
            return self.get_action(node.id)
        return self._json_action('pass')


    def clean(self):
        """Removes outdated nodes from Kaylee's nodes storage."""
        self._registry.clean()

    @property
    def applications(self):
        """Loaded applications dictionary-like container."""
        return self._applications

    @property
    def registry(self):
        """Active nodes registry (an instance of :class:`NodesRegistry`)."""
        return self._registry

    def _json_action(self, action, data = ''):
        return json.dumps( { 'action' : action, 'data' : data } )


class Config(object):
    """Kaylee Configuration repository."""
    fields = ['AUTO_GET_ACTION',
              'WORKER_SCRIPT',
              ]

    def __init__(self, **kwargs):
        self._dirty = True
        self._cached_dict = {}

        self.AUTO_GET_ACTION = kwargs.get('AUTO_GET_ACTION', True)
        self.WORKER_SCRIPT = kwargs['WORKER_SCRIPT']

    def __setattr__(self, name, value):
        if name != '_dirty':
            self.__dict__[name] = value
            self.__dict__['_dirty'] = True
        else:
            self.__dict__[name] = value

    def to_dict(self):
        if self._dirty:
            self._cached_dict = { k : getattr(self, k) for k in self.fields }
            self._dirty = False
        return self._cached_dict


class Applications(object):
    """A container for active Kaylee applications.

    :param controllers: A list of :class:`Controller` objects.
    """
    def __init__(self, controllers):
        self._controllers = {c.app_name : c for c in controllers}
        self.names = sorted(self._controllers.keys())

    def __getitem__(self, name):
        """Gets an application (an instance of :class:`Controller`)
        by its name.
        """
        return self._controllers[name]

    def __contains__(self, name):
        """Checks if the container contains application with requested
        name."""
        return name in self._controllers

    def __len__(self):
        """Returns the amount of applications in the container."""
        return len(self._controllers)

    @staticmethod
    def empty():
        return Applications([])
