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

__version__ = '0.1'

import os

from .core import Kaylee, Applications
from .node import Node, NodeID, NodesRegistry
from .storage import (TemporalStorage,
                      PermanentStorage )
from .controller import Controller
from .project import Project, Task
from .errors import KayleeError

from . import loader
kl = loader.LazyKaylee()


def setup(config):
    kl._setup(loader.load(config))
