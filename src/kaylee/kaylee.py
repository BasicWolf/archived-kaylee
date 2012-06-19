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
    data. Note that it is the task of the particular front-end to set the
    response content-type to "application/json".

    Usually an instance of :class:`Kaylee` is not created by a user,
    but via :function:`kaylee.load` function, which parses settings and
    returns initialized Kaylee object.

    :param nodes_config: settings-based configuration required by every node
                         in order to function properly. This includes for
                         example the URL root of the projects' script files.
    :param nodes_storage: an instance of :class:`kaylee.NodesStorage`.
    :param applications: an instance of :class:`kaylee.Applications` object.
    """
    def __init__(self, nodes_config, nodes_storage, applications):
        self.nodes_config = nodes_config
        self.nodes = nodes_storage
        self.applications = applications

    @json_error_handler
    def register(self, remote_host):
        """Registers the remote host as Kaylee Node and returns
        JSON-formatted data with the following fields:

        * node_id - hex-formatted node id
        * config  - global nodes configuration (see :module:`loader`)
        * applications - a list of Kaylee applications' names.

        :param remote_host: an IP address of the remote host
        :type remote_host: string
        """
        node = Node(NodeID.for_host(remote_host))
        self.nodes.add(node)
        return json.dumps ({ 'node_id' : str(node.id),
                             'config' : self.nodes_config,
                             'applications' : self.applications.names } )

    @json_error_handler
    def unregister(self, node_id):
        """Remove the node from Kaylee. Kaylee will reject any further
        requests from the node unless it registers again.

        :param node_id: a valid node id
        :type node_id: string
        """
        del self.nodes[node_id]

    @json_error_handler
    def subscribe(self, node_id, application):
        """Subscribe a node to an application.  In practice it means that
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
            node = self.nodes[node_id]
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
        self.nodes[node_id].unsubscribe()

    @json_error_handler
    def get_task(self, node_id):
        """Returns a task from the subscribed application.
        The format of the JSON response is:
        {
            'action' : <action>,
            'data'   : <data>
        }
        Here, <action> tells the Node, what should it do and <data> is
        the attached data. The available values of <action> are:

        * 'task'        - indicated that <data> contains task data
        * 'unsubscribe' - indicates that there is no need for the Node to
                          request tasks from the subscribed application
                          any more.

        :param node_id: a valid node id
        :type node_id: string
        """
        node = self.nodes[node_id]
        try:
            data = node.get_task().serialize()
            return self._json_action('task', data)
        except StopIteration as e:
            self.unsubscribe(node)
            return self._json_action('unsubscribe',
                'The node has been automatically unsubscribed: {}.'.format(e))

    @json_error_handler
    def accept_result(self, node_id, data):
        """Accepts the results from the node and returns a new task.
        Unsubscribes the node if the returned result is invalid.

        :param node_id: a valid node id
        :param data: the data returned by the node. This data will be later
                     normalized and validated by the project and then
                     stored to the application's storages.
        :type node_id: string
        :type data: string
        :returns: a task returned by :function:`Kaylee.get_task`.
        """
        node = self.nodes[node_id]
        try:
            node.accept_result(data)
        except ValueError as e:
            self.unsubscribe(node)
            raise InvalidResultError(node)

        return self.get_task(node.id)

    def clean(self):
        """Removes outdated nodes from Kaylee's nodes storage."""
        self.nodes.clean()

    def _json_action(self, action, data):
        return json.dumps( { 'action' : action, 'data' : data } )


class Applications(object):
    def __init__(self, controllers):
        self._controllers = controllers
        self._idx_controllers = sorted([c for c in controllers.itervalues()],
                                       key = attrgetter('id'))
        self.names = list(controllers.keys())

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._idx_controllers[key]
        else:
            return self._controllers[key]

    def __contains__(self, key):
        return key in self._controllers

    def __len__(self):
        return len(self._controllers)

    @staticmethod
    def empty():
        return Applications({})
