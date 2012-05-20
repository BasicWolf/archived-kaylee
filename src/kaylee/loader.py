# -*- coding: utf-8 -*-
"""
    kaylee.loader
    ~~~~~~~~~~~~~

    Implements Kaylee projects, controllers and dispatcher loader.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: GPL, see LICENSE for more details.
"""
import os
import importlib
import inspect
from operator import attrgetter

class Applications(object):
    def __init__(self, controllers):
        self._controllers = controllers
        self._idx_controllers = sorted([c for c in controllers.itervalues()],
                                       key = attrgetter('id'))
        self.names = list(controllers.keys())

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._idx_controllers[key]
        else:
            return self._controllers[key]


def load_kaylee(settings):
    from . import storage
    from . import controller
    from . import project
    from . errors import KayleeError
    from .dispatcher import Dispatcher
    from .py3compat import string_types, string_type, binary_type

    """Load Kaylee's global objects using configuration from settings.
    """
    # scan for classes
    project_classes = {}
    controller_classes = {}
    nstorage_classes = {}
    crstorage_classes = {}
    arstorage_classes = {}
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
        ctrl_classes = _get_classes( controller.__dict__.values()  )
        stg_classes = _get_classes( storage.__dict__.values() )
        _store_classes(project_classes, mod_classes, project.Project)
        _store_classes(controller_classes, mod_classes, controller.Controller)
        _store_classes(controller_classes, ctrl_classes, controller.Controller)
        _store_classes(nstorage_classes, stg_classes, storage.NodesStorage)
        _store_classes(crstorage_classes, stg_classes,
                       storage.ControllerResultsStorage)
        _store_classes(arstorage_classes, stg_classes,
                       storage.AppResultsStorage)
    # load controllers/projects classes and initialize applications
    controllers = {}
    _idx = 0
    for conf in settings.APPLICATIONS:
        app_name = conf['name']
        if not isinstance(app_name, string_types):
            raise KayleeError('Configuration error: app name {} is not a string'
                              .format(app_name))
        try:
            pname = conf['project']['name']
            cname = conf['controller']['name']
            crsname = conf['controller']['results_storage']['name']
            arsname = conf['controller']['app_results_storage']['name']
            pcls = project_classes[pname]
            ccls = controller_classes[cname]
            crscls = crstorage_classes[crsname]
            arscls = arstorage_classes[arsname]
        except KeyError as e:
            raise KayleeError('Configuration error or required class '
                              'was not found: "{}"'.format(e.args[0]))
        # initialize objects
        project = pcls(**conf['project']['config'])
        crstorage = crscls(**conf['controller']['results_storage']['config'])
        arstorage = arscls(**conf['controller']['app_results_storage']['config'])
        # initialize controller and store it local controllers dict
        controller = ccls(_idx, app_name, project, crstorage, arstorage,
                          **conf['controller']['config'])
        controllers[app_name] = controller
        _idx += 1
    applications = Applications(controllers)
    # initialize Dispatcher
    nsname = settings.DISPATCHER['nodes_storage']['name']
    nscls = nstorage_classes[nsname]
    nstorage = nscls(**settings.DISPATCHER['nodes_storage']['config'])
    dispatcher = Dispatcher(applications, nstorage)
    return dispatcher

def _store_classes(dest, classes, cls):
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        dest[c.__name__] = c

def _get_classes(attr_list):
    return list( attr for attr in attr_list if inspect.isclass(attr) )
