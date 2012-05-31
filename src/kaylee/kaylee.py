# -*- coding: utf-8 -*-
"""
    kaylee.kaylee
    ~~~~~~~~~~~~~~~~~

    This module implements Kaylee's lower level front-end which could
    be easily used with any web framework.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
import threading
import json
from operator import attrgetter
from functools import partial

from .node import Node, NodeID
from .errors import KayleeError

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
            return json.dumps({ 'error' : str(e) })
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
        self._lock = threading.Lock()

    @json_error_handler
    def register(self, remote_host):
        """Registers the remote host as Kaylee Node and returns
        JSON-formatted data with the following fields:

        * node_id - hex-formatted node id
        * config  - global nodes configuration (see :module:`loader`)
        * applications - a list of Kaylee applications' names.
        """
        node = Node(NodeID.for_host(remote_host))
        with self._lock:
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
        """Unsubscribes the node from bound application."""
        self.nodes[node_id].reset()

    @json_error_handler
    def get_task(self, node_id):
        node = self.nodes[node_id]
        try:
            data = node.get_task().serialize()
            return self._json_action('task', data)
        except StopIteration as e:
            # at this point Controller indicates that
            return self._json_action('stop', e.message)

    @json_error_handler
    def accept_result(self, node_id, data):
        node = self.nodes[node_id]
        node.accept_result(data)
        return self.get_task(node.id)

    def clean(self):
        """The method removes all timed-out nodes from Kaylee."""
        raise NotImplementedError()
        # with self._lock:
        #     for node in self.nodes:
        #         pass

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
