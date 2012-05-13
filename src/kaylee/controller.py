# -*- coding: utf-8 -*-
import os
import importlib
import inspect

from . import settings
from . import storage
from .project import Project
from .errors import KayleeError
from .node import Node


class Controller(object):
    def __init__(self, app_name, project, nodes_storage, *args, **kwargs):
        self.app_name = app_name
        self.project = project
        self.nodes = nodes_storage

    def subscribe(self, nid):
        """Subscribe Node for bound project"""
        node = Node(nid)
        node.subscribe()
        self.nodes.add(node)
        return self.project.node_config

class ResultsComparatorController(Controller):
    def __init__(self, *args, **kwargs):
        super(ResultsComparatorController, self).__init__(*args, **kwargs)


def load_applications():
    # scan for classes
    project_classes = {}
    controller_classes = {}
    nstorage_classes = {}
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
        mod_classes = _get_classes( pymod.__dict__.values() )
        loc_classes = _get_classes( globals().values() )
        ns_classes = _get_classes( storage.__dict__.values() )
        _store_classes(project_classes, mod_classes, Project)
        _store_classes(controller_classes, mod_classes, Controller)
        _store_classes(controller_classes, loc_classes, Controller)
        _store_classes(nstorage_classes, ns_classes,
                       storage.NodesStorage)
    # load controllers/projects classes and initialize controllers
    controllers = {}
    for conf in settings.APPLICATIONS:
        try:
            pname = conf['project']['name']
            cname = conf['controller']['name']
            nsname = conf['controller']['nodes_storage']['name']
            pcls = project_classes[pname]
            ccls = controller_classes[cname]
            nscls = nstorage_classes[nsname]
        except KeyError as e:
            raise KayleeError('Configuration error or required class '
                              'was not found: "{}"'.format(e.args[0]))
        project = pcls(**conf['project']['config'])
        nstorage = nscls(**conf['controller']['nodes_storage']['config'])
        app_name = conf['name']
        controllers[app_name] = ccls(app_name, project, nstorage,
                                    **conf['controller']['config'])
    return controllers

def _store_classes(dest, classes, cls):
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        dest[c.__name__] = c

def _get_classes(attr_list):
    return list( attr for attr in attr_list if inspect.isclass(attr) )
