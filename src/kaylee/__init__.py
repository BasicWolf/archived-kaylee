import os
import imp
settings = imp.load_source('settings', os.environ['KAYLEE_SETTINGS_PATH'])

from .storage import Storage
from .dispatcher import DefaultDispatcher
from .objectid import NodeID
from .application import Application


dispatcher = DefaultDispatcher()
applications = Application.load()
