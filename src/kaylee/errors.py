# -*- coding: utf-8 -*-
"""
    kaylee.errors
    ~~~~~~~~~~~~~

    This module implements all exceptions raised by the Kaylee package.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""



class KayleeError(Exception):
    """Base class for all Kaylee exceptions."""

class InvalidNodeIDError(KayleeError):
    def __init__(self, node_id):
        KayleeError.__init__(self, '{} is not a valid node id'.format(node_id))

class NodeUnsubscribedError(KayleeError):
    def __init__(self, node):
        KayleeError.__init__(self, 'Node {} is not subscribed'.format(node))

class AppCompletedError(StopIteration, KayleeError):
    def __init__(self, app_name):
        KayleeError.__init__(self, 'All calculations for application {} '
                                   'were completed'.format(app_name))

class InvalidResultError(ValueError, KayleeError):
    def __init__(self, result, why = ''):
        KayleeError.__init__(self, 'Invalid result "{}": {}'
                             .format(result, why))
