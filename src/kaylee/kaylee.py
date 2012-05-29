# -*- coding: utf-8 -*-
"""
    kaylee.kaylee
    ~~~~~~~~~~~~~~~~~

    This module implements Kaylee's lower level front-end which could
    be easily used with any web framework.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT or GPLv3, see LICENSE for more details.
"""
import threading
import json
from .node import Node, NodeID
from .errors import KayleeError
from .loader import Applications

class Kaylee(object):
    """The Kaylee class serves as a proxy between WSGI framework and Kaylee
    applications. It handles requests from clients and returns JSON-formatted
    data. Note that it is the task of particular front-end to set the
    content-type to "application/json".

    Usually you don't create an instance of :class:`Kaylee` is not created,
    but rather call :function:`kaylee.load` with settings as an argument.

    :param nodes_storage: an instance of :class:`kaylee.NodesStorage`.
    :param applications: an instance of :class:`kaylee.Applications` object.
    """
    def __init__(self, nodes_storage, applications = Applications({})):
        self.applications = applications
        self.nodes = nodes_storage
        self._lock = threading.Lock()

    def register(self, remote_host):
        with self._lock:
            node = Node(NodeID(remote_host))
            self.nodes.add(node)
        return json.dumps ({ 'node_id' : str(node.id),
                             'applications' : self.applications.names } )

    def unregister(self, node_id):
        self.nodes.remove(node_id)

    def subscribe(self, node_id, application):
        try:
            try:
                node = self.nodes[node_id]
            except KeyError:
                raise KayleeError('Node "{}" is not registered'.format(node_id))
            try:
                app = self.applications[application]
                return json.dumps( app.subscribe(node) )
            except KeyError:
                raise KayleeError('Application "{}" was not found'.format(app))
        except KayleeError as e:
            return self._json_error(e.message)

    def unsubscribe(self, node_id):
        raise NotImplementedError()

    def get_task(self, node_id):
        node = self.nodes[node_id]
        try:
            data = node.get_task().serialize()
            return self._json_action('task', data)
        except StopIteration as e:
            # at this point Controller indicates that
            return self._json_action('stop', e.message)
        except KayleeError as e:
            return self._json_error(e.message)

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
        return json.dumps( { 'action' : action, 'data' : data },
                           separators = (',', ':'))

    def _json_error(self, message):
        return json.dumps({ 'error' : message }, separators=(',',':'))
