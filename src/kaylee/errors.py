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

class NodeUnsubscribedError(KayleeError):
    def __init__(self, node):
        KayleeError.__init__(self, 'Node {} is not subscribed'.format(node))

class StopApplication(KayleeError, StopIteration):
    def __init__(self, app_name):
        super(StopApplication, self).__init__(
            self, ('All calculations for application {} were completed'
                   .format(app_name)))

class InvalidResultError(KayleeError, ValueError):
    def __init__(self, result, why = ''):
        super(InvalidResultError, self).__init__(
            self, 'Invalid result "{}": {}'.format(result, why))

class KayleeWarning(UserWarning):
    pass

def warn(message):
    warnings.warn(message, KayleeWarning, 3)
