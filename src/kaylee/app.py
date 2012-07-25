# -*- coding: utf-8 -*-
"""
    kaylee.kaylee
    ~~~~~~~~~~~~~~~~~

    This module implements Kaylee's lower level front-end which could
    be easily used with any web framework.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
import sys
import json
import traceback
from StringIO import StringIO
from operator import attrgetter
from functools import partial
from contextlib import closing
from functools import wraps

from .node import Node, NodeID
from .errors import KayleeError, InvalidResultError
from . import settings

#: Returns the results of :function:`json.dumps` in compact encoding
json.dumps = partial(json.dumps, separators=(',',':'))


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
            if settings.DEBUG:
                with closing(StringIO()) as buf:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    traceback.print_tb(exc_traceback,
                                       limit = None,
                                       file = buf)
                    exc_str += '\n' + buf.getvalue()
            return json.dumps({ 'error' : exc_str })

    return wrapper


class Kaylee(object):
    """The Kaylee class serves as a proxy between WSGI framework and Kaylee
    applications. It handles requests from clients and returns JSON-formatted
    data. Note that it is the job of a particular front-end to set the
    response content-type to "application/json".

    Usually an instance of :class:`Kaylee` is not created by a user,
    but loaded automatically and can be used as follows::

        from kaylee import kl

    :param client_config: settings-based configuration required by every node
                          in order to function properly. This includes for
                          example the URL root of the projects' script files.
    :param client_config: an instance of :class:`NodesRegistry`.
    :param applications: an instance of :class:`Applications` object.
    """
    def __init__(self, client_config, registry, applications):
        self.client_config = client_config
        self.registry = registry
        self.applications = applications

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
        self.registry.add(node)
        return json.dumps ({ 'node_id' : str(node.id),
                             'config' : self.client_config,
                             'applications' : self.applications.names } )

    @json_error_handler
    def unregister(self, node_id):
        """Remove the node from Kaylee. Kaylee will reject any further
        requests from the node unless it registers again.

        :param node_id: a valid node id
        :type node_id: string
        """
        del self.registry[node_id]

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
            node = self.registry[node_id]
        except KeyError:
            raise KayleeError('Node "{}" is not registered'.format(node_id))

        try:
            app = self.applications[application]
            return json.dumps( app.subscribe(node) )
        except KeyError:
            raise KayleeError('Application "{}" was not found'.format(app))

    @json_error_handler
    def unsubscribe(self, node_id):
        """Unsubscribes the node from the bound application.

        :param node_id: a valid node id
        :type node_id: string
        """
        self.registry[node_id].unsubscribe()

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
        node = self.registry[node_id]
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
        :py:attr:`Settings.GET_NEXT_ACTION_ON_ACCEPT_RESULTS` is True.
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
        node = self.registry[node_id]
        try:
            # parse data if it is still a JSON string
            if isinstance(data, basestring):
                data = json.loads(data)
            node.accept_result(data)
        except ValueError as e:
            self.unsubscribe(node)
            raise InvalidResultError(data, str(e))

        if settings.AUTO_GET_NEXT_ACTION_ON_ACCEPT_RESULTS:
            return self.get_action(node.id)
        return self._json_action('pass')


    def clean(self):
        """Removes outdated nodes from Kaylee's nodes storage."""
        self.registry.clean()

    def _json_action(self, action, data = ''):
        return json.dumps( { 'action' : action, 'data' : data } )


class Applications(object):
    def __init__(self, controllers):
        self._controllers = controllers
        self.names = list(controllers.keys())

    def __getitem__(self, key):
        return self._controllers[key]

    def __contains__(self, key):
        return key in self._controllers

    def __len__(self):
        return len(self._controllers)

    @staticmethod
    def empty():
        return Applications({})
