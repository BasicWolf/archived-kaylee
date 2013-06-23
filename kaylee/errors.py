# -*- coding: utf-8 -*-
"""
    kaylee.errors
    ~~~~~~~~~~~~~

    This module implements all exceptions raised by the Kaylee package.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

import warnings


class KayleeError(Exception):
    """Base class for all Kaylee exceptions."""


class KayleeProjectAssertError(KayleeError):
    """Base class for all Kaylee project-related runtime assertion
    (regular, **not** Python ``asert`` checks) errors."""
    pass


class InvalidNodeIDError(KayleeError):
    """Raised when parsing a node id (e.g. hex string) fails."""
    def __init__(self, node_id):
        KayleeError.__init__(self, '{} is not a valid node id'.format(node_id))


class NodeNotSubscribedError(KayleeError):
    """Raised when a Node requests an action or submits results without
    being subscribed to an application."""
    def __init__(self, node):
        KayleeError.__init__(self, 'Node {} is not subscribed'.format(node))


class InvalidResultError(ValueError, KayleeError):
    """Raised when a result received from the client is not valid (e.g.
    :meth:`Project.normalize_result` fails)."""
    def __init__(self, result, why = ''):
        super(InvalidResultError, self).__init__(
            'Invalid result "{}": {}'.format(result, why))


class NoneResultAssertError(KayleeProjectAssertError, ValueError):
    """Raised by controller if a normalized result returned by
    :meth:`Project.normalize_result` is ``None``."""
    def __init__(self, result):
        super(NoneResultAssertError, self).__init__(
            'A result {} has been normalized to None'.format(result))


class NodeRequestRejectedError(KayleeError):
    """Raised when a controller rejects a task request or result response
    from a node for some particular reason (e.g. if the node has submitted
    the same task result twice without "being asked" to do so)."""
    def __init__(self, message):
        KayleeError.__init__(self, ('The node has been rejected: {}'
                                    .format(message)) )


class ApplicationCompletedError(NodeRequestRejectedError):
    """Raised when a node request is rejected due to the
    :attr:`completed <Project.completed>` state of the application.

    Base class: :class:`NodeRequestRejectedError`."""
    def __init__(self, application):
        self.application = application
        super(ApplicationCompletedError, self).__init__(
            'The application "{}" has been completed.'
            .format(application.name) )


class InvalidConfigurationError(KayleeError):
    """Raised when :class:`Kaylee object <Kaylee>` configuration is
    configured improperly."""
    def __init__(self, message):
        super(InvalidConfigurationError, self).__init__(
            'Invalid configuration: ' + message)


class SessionKeyNameError(KayleeError):
    """Raised when a session variable name is invalid."""
    def __init__(self, why):
        KayleeError.__init__(self, 'Invalid session variable name: {}'.format(why))


class KayleeWarning(UserWarning):
    pass


def warn(message):
    warnings.warn(message, KayleeWarning, 3)
