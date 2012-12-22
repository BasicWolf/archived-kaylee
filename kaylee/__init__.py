# -*- coding: utf-8 --*
"""
    kaylee
    ~~~~~~

    Kaylee is distributed and volunteer computing framework.

    It implements all the functionality required to distribute computation
    among nodes and collect the results. Kaylee aims to let a user
    completely focus on project's business logic and handle all other
    stuff automatically.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.2'

import os

from . import loader
kl = loader.LazyKaylee()

from .core import Kaylee, Applications
from .node import Node, NodeID, NodesRegistry
from .storage import (TemporalStorage,
                      PermanentStorage )
from .session import SessionDataManager
from .controller import Controller
from .project import Project
from .errors import (KayleeError,
                     InvalidNodeIDError,
                     NodeNotSubscribedError,
                     InvalidResultError,
                     NodeRequestRejectedError,
                     ApplicationCompletedError,)


def setup(config):
    #pylint: disable-msg=W0212
    #W0212: Access to a protected member _setup
    if config is not None:
        # In this case we are trying to load Kaylee from the given config
        kl._setup(loader.load(config))
    else:
        # In this case the user probably(!) asks us to "release" Kaylee
        # instance from the proxy.
        kl._setup(None)
