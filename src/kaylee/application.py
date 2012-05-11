import os
import importlib

from . import settings
from . import controller
from .project import Project
from .controller import Controller
from .errors import KayleeError

class Application(object):
    def __init__(self, name, controller, project):
        self.name = name
        self.controller = controller
        self.project = project

    @staticmethod
    def load():
        _project_classes, _controller_classes = Application.scan()
        apps = []
        for conf in settings.APPLICATIONS:
            pname = conf['project']['name'].lower()
            cname = conf['controller']['name'].lower()
            if pname not in _project_classes:
                raise KayleeError('Configuration error or project class is '
                                  'missing: "{}"'.format(pname))
            if cname not in _controller_classes:
                raise KayleeError('Configuration error or controller class is '
                                  'missing: "{}"'.format(pname))
            pcls = _project_classes[pname]
            ccls = _controller_classes[cname]
            pobj = pcls(**conf['project']['config'])
            cobj = ccls(**conf['controller']['config'])
            apps.append( Application(conf['name'], cobj, pobj) )
        return apps

    @staticmethod
    def scan():
        _project_classes = {}
        _controller_classes = {}
        for sub_dir in os.listdir(settings.PROJECTS_DIR):
            project_dir_path = os.path.join(settings.PROJECTS_DIR, sub_dir)
            if not os.path.isdir(project_dir_path):
                continue
            if '__init__.py' not in os.listdir(project_dir_path):
                continue
            # looks like a python module
            try:
                pymod = importlib.import_module(sub_dir)
            except ImportError:
                raise ImportError('Unable to import project package {}'
                                  .format(name))
            classes = ( attr for attr in pymod.__dict__.values()
                        if isinstance(attr, type) )
            # store project classes
            for cls in (cls for cls in classes if issubclass (cls, Project) ):
                _project_classes[cls.__name__.lower()] = cls
            # store custom controller classes
            for cls in (cls for cls in classes if issubclass (cls, Controller) ):
                _controller_classes[cls.__name__.lower()] = cls
            # store local controller classes
            for cls in ( attr for attr in controller.__dict__.values()
                         if isinstance(attr, type) and
                         issubclass (attr, Controller) and
                         attr is not Controller ):
                _controller_classes[cls.__name__.lower()] = cls
        return _project_classes,  _controller_classes
