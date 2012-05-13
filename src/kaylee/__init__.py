# -*- coding: utf-8 --*

__version__ = '0.1'

import os
import imp
settings = imp.load_source('settings', os.environ['KAYLEE_SETTINGS_PATH'])

from .project import Project
from .objectid import NodeID

from .dispatcher import DefaultDispatcher
dispatcher = DefaultDispatcher()
