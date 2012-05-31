# -*- coding: utf-8 --*
"""
    kaylee
    ~~~~~~

    Kaylee is distributed computing framework.

    It implements all the functionality required to distribute computation
    among nodes and collect the results. Kaylee aims to let a user
    completely focus on project's business logic and handle all other
    stuff automatically.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

__version__ = '0.1'

from .kaylee import Kaylee, Applications
from .node import Node, NodeID
from .storage import NodesStorage
from .controller import Controller
from .project import Project
from .loader import load
from .errors import KayleeError

