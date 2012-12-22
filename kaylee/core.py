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
from functools import partial
from contextlib import closing
from functools import wraps

from .node import Node, NodeID
from .errors import KayleeError, InvalidResultError, NodeRequestRejectedError
from .controller import KL_RESULT

log = logging.getLogger(__name__)

#: Returns the results of :function:`json.dumps` in compact encoding
json.dumps = partial(json.dumps, separators=(',', ':'))

ACTION_TASK = 'task'
ACTION_UNSUBSCRIBE = 'unsubscribe'
ACTION_NOP = 'nop'


def json_error_handler(f):
    """A decorator that wraps a function into try..catch block and returns
    JSON-formatted "{ error : str(Exception) }" if an exception has been
    raised.
    """
    #pylint: disable-msg=W0703
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            exc_str = str(e)

            if log.getEffectiveLevel() == logging.DEBUG:
                with closing(StringIO()) as buf:
                    # exc_type, exc_value, exc_traceback = sys.exc_info()
                    exc_traceback = sys.exc_info()[2]
                    traceback.print_tb(exc_traceback,
                                       limit = None,
                                       file = buf)
                    exc_str += '\n' + buf.getvalue()
            return json.dumps({ 'error' : exc_str })

    return wrapper


class Kaylee(object):
    """The Kaylee class serves as a layer between a WSGI server (framework)
    and Kaylee applications. The data flow between Kaylee server and the
    client is kept in JSON format.

    .. note:: It is the job of the WSGI front-end to set the response
              content-type to "application/json".

    See :ref:`loading_kaylee_object` for  Kaylee object initialization and
    loading procedure.

    :param registry: active nodes registry
    :param session_data_manager: global session data manager
    :param applications: a list of applications (:class:`Controller` objects)
    :param kwargs: Kaylee configuration arguments.
    :type registry: :class:`NodesRegistry`
    :type session_data_manager: :class:`SessionDataManager` or None
    :type applications: list or None
    """
    def __init__(self, registry, session_data_manager = None,
                 applications = None, **kwargs):
        #: An internal configuration storage object which maintains
        #: the configuration initially parsed from ``**kwargs**``.
        #: The options are accessed as object attributes, e.g.:
        #: ``kl.config.WORKER_SCRIPT_URL``.
        self._config = Config(**kwargs)

        #: Active nodes registry (an instance of :class:`NodesRegistry`).
        self.registry = registry

        self.session_data_manager = session_data_manager
        if applications is not None:
            self._applications = Applications(applications)
        else:
            self._applications = Applications.empty()

    @json_error_handler
    def register(self, remote_host):
        """Registers the remote host (browser) as Kaylee Node and returns
        JSON-formatted data with the following fields:

        * node_id - node id (hex-formatted string)
        * config  - client configuration (see :ref:`configuration`).
        * applications - a list of Kaylee applications' names.

        :param remote_host: the IP address of the remote host
        :type remote_host: string
        """
        node = Node(NodeID.for_host(remote_host))
        self.registry.add(node)
        return json.dumps ({ 'node_id' : str(node.id),
                             'config' : self._config.to_dict(),
                             'applications' : self._applications.names } )

    @json_error_handler
    def unregister(self, node_id):
        """Removes the node from the nodes registry. Practically this means
        that the remote host (browser) disconnects or is disconnected from
        the Kaylee server.

        :param node_id: a valid node id
        :type node_id: string
        """
        del self.registry[node_id]

    @json_error_handler
    def subscribe(self, node_id, application):
        """Subscribes a node to an application. After a successful subscription
        the node receives a client-side application configuration and invokes
        client-side project initialization routines.

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
            app = self._applications[application]
            client_config = node.subscribe(app)
            return json.dumps(client_config)
        except KeyError:
            raise KayleeError('Application "{}" was not found'.format(app))

    @json_error_handler
    def unsubscribe(self, node_id):
        """Unsubscribes the node from the bound application.

        :param node_id: a valid node id.
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
        the attached data. The valid <actions> are:

        * **"task"** - indicated that <data> contains task data
        * **"unsubscribe"** - indicates that Kaylee server has unsubscribed
          the Node from the application. Any further action request by the
          node raises :class:`NodeNotSubscribedError
          <kaylee.error.NodeNotSubscribedError>`.
        * **"nop"** - indicates that no operation should be carried out by
          the node right now.

        :param node_id: a valid node id
        :type node_id: string
        """
        node = self.registry[node_id]
        try:
            task = node.get_task()
            self._store_session_data(node, task)
            # update node before returning a task
            if node.dirty:
                self.registry.update(node)
                node.dirty = False
            return self._json_action(ACTION_TASK, task)
        except NodeRequestRejectedError as e:
            return self._json_action(ACTION_UNSUBSCRIBE,
                                     'The node has been automatically '
                                     'unsubscribed: {}'.format(e))

    @json_error_handler
    def accept_result(self, node_id, result):
        """Accepts the results from the node. Returns the next action if
        :config:`AUTO_GET_ACTION` configuration option is True. Otherwise
        returns the "nop" (no operatiotion) action.

        :param node_id: a valid node id
        :param result: the result returned by the node.
        :type node_id: string
        :type result: string with JSON-encoded dict data.
        :returns: A task (an action) returned by :meth:`get_action` or
                 "nop" action.
        """
        node = self.registry[node_id]
        try:
            if not isinstance(result, basestring):
                raise ValueError('Kaylee expects the incoming result to be in '
                                 'string format, not {}'.format(
                                     result.__class__.__name__))
            parsed_result = json.loads(result)
            if not isinstance(parsed_result, dict):
                raise ValueError('The returned result was not parsed '
                                 'as dict: {}'.format(parsed_result))
            self._restore_session_data(node, parsed_result)
            node.accept_result(parsed_result)
        except InvalidResultError as e:
            self.unsubscribe(node)
            raise e

        if self._config.AUTO_GET_ACTION:
            return self.get_action(node.id)
        return self._json_action(ACTION_NOP)

    def clean(self):
        """Removes the outdated nodes from Kaylee's nodes storage."""
        self.registry.clean()

    def _store_session_data(self, node, task):
        if self.session_data_manager is not None:
            self.session_data_manager.store(node, task)

    def _restore_session_data(self, node, result):
        if not KL_RESULT in result:
            if self.session_data_manager is not None:
                self.session_data_manager.restore(node, result)

    @property
    def applications(self):
        """Available applications container (
        :class:`kaylee.core.Applications` object)"""
        return self._applications

    @staticmethod
    def _json_action(action, data = ''):
        return json.dumps( { 'action' : action, 'data' : data } )


class Config(object):
    """The ``Config`` object maintains the run-time Kaylee
    configuration options (see :ref:`configuration` for full description).
    """
    serialized_attributes = [
        'AUTO_GET_ACTION',
        'WORKER_SCRIPT_URL',
    ]

    def __init__(self, **kwargs):
        self._dirty = True
        self._cached_dict = {}

        # first, set the options with default values
        self.AUTO_GET_ACTION = kwargs.get('AUTO_GET_ACTION', True)
        self.SECRET_KEY = kwargs.get('SECRET_KEY', None)

        # next, set the options with required values
        try:
            self.WORKER_SCRIPT_URL = kwargs.get('WORKER_SCRIPT_URL', None)
        except KeyError as e:
            raise KeyError('The required config option is missing: {}'
                           .format(e.args[0]))

    def __setattr__(self, name, value):
        if name != '_dirty':
            self.__dict__[name] = value
            self.__dict__['_dirty'] = True
        else:
            self.__dict__[name] = value

    def to_dict(self):
        if self._dirty:
            self._cached_dict = { k : getattr(self, k)
                                  for k in self.serialized_attributes }
            self._dirty = False
        return self._cached_dict


class Applications(object):
    """A readonly container for active Kaylee applications.

    :param controllers: A list of :class:`Controller` objects.
    """
    def __init__(self, controllers):
        self._controllers = {c.name : c for c in controllers}

        #: A list of apllications' names
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
