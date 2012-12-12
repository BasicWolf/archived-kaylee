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

class InvalidNodeIDError(KayleeError):
    def __init__(self, node_id):
        KayleeError.__init__(self, '{} is not a valid node id'.format(node_id))

class NodeNotSubscribedError(KayleeError):
    def __init__(self, node):
        KayleeError.__init__(self, 'Node {} is not subscribed'.format(node))

class InvalidResultError(ValueError, KayleeError):
    def __init__(self, result, why = ''):
        super(InvalidResultError, self).__init__(
            'Invalid result "{}": {}'.format(result, why))

class NodeRejectedError(KayleeError):
    def __init__(self):
        KayleeError.__init__(self, 'The node was rejected.')

class ApplicationCompletedError(NodeRejectedError):
    def __init__(self, application):
        self.application = application
        super(NodeRejectedError, self).__init__(
            'The application "{}" has been completed.'.format(
                application.name))

class KayleeWarning(UserWarning):
    pass

def warn(message):
    warnings.warn(message, KayleeWarning, 3)
