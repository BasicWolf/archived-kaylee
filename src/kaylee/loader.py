# -*- coding: utf-8 -*-
"""
    kaylee.loader
    ~~~~~~~~~~~~~

    Implements Kaylee projects, controllers and Kaylee loader.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""
import os
import imp
import importlib
import inspect

from .errors import KayleeError
from .kaylee import Kaylee, Applications


def load(settings = None):
    try:
        return Kaylee(*load_kaylee_objects(settings))
    except (KeyError, AttributeError) as e:
        raise KayleeError('Settings error or object was not found: '
                          ' "{}"'.format(e.args[0]))

def load_kaylee_objects(settings = None):
    """Loads Kaylee objects using configuration from settings.

    :param: Python module or class with Kaylee settings. If the value
            of settings is None, then the loader tries to load the
            settings using KAYLEE_SETTINGS_MODULE environmental
            variable.
    :returns: Nodes configuration, nodes storage and applications.
    :rtype: (dict, :class:`NodesStorage`, :class:`Applcations`)
    """
    from . import storage
    from . import controller
    from . import project

    if settings is None:
        settings = imp.load_source('settings',
                                   os.environ['KAYLEE_SETTINGS_MODULE'])
    # scan for classes
    project_classes = {}
    controller_classes = {}
    nstorage_classes = {}
    crstorage_classes = {}
    arstorage_classes = {}

    # load built-in kaylee classes
    ctrl_classes = _get_classes( controller.__dict__.values()  )
    stg_classes = _get_classes( storage.__dict__.values() )
    _store_classes(controller_classes, ctrl_classes, controller.Controller)
    _store_classes(nstorage_classes, stg_classes, storage.NodesStorage)
    _store_classes(arstorage_classes, stg_classes, storage.AppResultsStorage)
    _store_classes(crstorage_classes, stg_classes,
                   storage.ControllerResultsStorage)

    # load classes from project modules
    for sub_dir in os.listdir(settings.PROJECTS_DIR):
        project_dir_path = os.path.join(settings.PROJECTS_DIR, sub_dir)
        if not os.path.isdir(project_dir_path):
            continue
        if '__init__.py' not in os.listdir(project_dir_path):
            continue
        # looks like a python module
        try:
            pymod = importlib.import_module(sub_dir)
        except ImportError as e:
            raise ImportError('Unable to import project package: {}'
                              .format(e))
        mod_classes = _get_classes( pymod.__dict__.values() )
        _store_classes(project_classes, mod_classes, project.Project)
        _store_classes(controller_classes, mod_classes, controller.Controller)

    # load controllers/projects classes and initialize applications
    controllers = {}
    _idx = 0
    for conf in settings.APPLICATIONS:
        app_name = conf['name']
        if not isinstance(app_name, basestring):
            raise KayleeError('Configuration error: app name {} is not a string'
                              .format(app_name))

        pname = conf['project']['name']
        cname = conf['controller']['name']
        crsname = conf['controller']['results_storage']['name']
        arsname = conf['controller']['app_results_storage']['name']
        pcls = project_classes[pname]
        ccls = controller_classes[cname]
        crscls = crstorage_classes[crsname]
        arscls = arstorage_classes[arsname]

        # initialize objects
        project = pcls(**conf['project']['config'])
        crstorage = crscls(**conf['controller']['results_storage']['config'])
        arstorage = arscls(**conf['controller']['app_results_storage']
                             ['config'])
        # initialize controller and store it local controllers dict
        controller = ccls(_idx, app_name, project, crstorage, arstorage,
                          **conf['controller']['config'])
        controllers[app_name] = controller
        _idx += 1
    applications = Applications(controllers)

    # build Kaylee nodes configuration
    nconfig = {'projects_static_root' : settings.PROJECTS_STATIC_ROOT,
               'kaylee_js_root' : settings.KAYLEE_JS_ROOT,
               'lib_js_root' : settings.LIB_JS_ROOT,
               }
    # initialize Kaylee objects
    nsname = settings.NODES_STORAGE['name']
    nscls = nstorage_classes[nsname]
    nstorage = nscls(**settings.NODES_STORAGE['config'])
    return nconfig, nstorage, applications, settings

def _store_classes(dest, classes, cls):
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        dest[c.__name__] = c

def _get_classes(attr_list):
    return list( attr for attr in attr_list if inspect.isclass(attr) )
