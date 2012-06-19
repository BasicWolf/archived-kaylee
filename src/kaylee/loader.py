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
from .util import LazyObject, import_object

SETTINGS_ENV_VAR = 'KAYLEE_SETTINGS_MODULE'


class Settings(object):
    def __init__(self):
        pass


class LazySettings(LazyObject):
    """
    A lazy proxy for either global Kaylee settings or a custom settings object.
    The user can manually configure settings prior to using them. Otherwise,
    Kaylee uses the settings module pointed to by KAYLEE_SETTINGS_MODULE.
    """
    def _setup(self):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        try:
            settings_path = os.environ[SETTINGS_ENV_VAR]
            if not settings_path: # If it's set but is an empty string.
                raise KeyError
        except KeyError:
            # NOTE: This is arguably an EnvironmentError, but that causes
            # problems with Python's interactive help.
            raise ImportError("Settings cannot be imported, because "
                              "environment variable {} is undefined."
                              .format(SETTINGS_ENV_VAR))
        self._wrapped = Settings()

        mod = imp.load_source('settings', settings_path)
        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                setattr(self._wrapped, setting, setting_value)

    @property
    def configured(self):
        """Returns True if the settings have already been configured."""
        return self._wrapped is not empty


class LazyKaylee(LazyObject):
    def _setup(self):
        self._wrapped = load()

def load(settings = None):
    from .kaylee import Kaylee
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
    from .kaylee import Applications
    if settings is None:
        from . import settings

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

        # initialize objects
        project = _get_project_object(conf, project_classes)
        crstorage = _get_tmp_storage_object(conf, crstorage_classes)
        arstorage = _get_app_storage_object(conf, arstorage_classes)
        controller = _get_controller_object(_idx, app_name, project, crstorage,
                                            arstorage, conf, controller_classes)

        # initialize store controller to local controllers dict
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
    return nconfig, nstorage, applications


def _store_classes(dest, classes, cls):
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        dest[c.__name__] = c

def _get_classes(attr_list):
    return list( attr for attr in attr_list if inspect.isclass(attr) )

def _get_project_object(conf, project_classes):
    pname = conf['project']['name']
    pcls = project_classes[pname]
    return pcls(**conf['project'].get('config', {}))

def _get_tmp_storage_object(conf, crstorage_classes):
    if not 'tmp_storage' in conf['controller']:
        return None
    crsname = conf['controller']['tmp_storage']['name']
    crscls = crstorage_classes[crsname]
    return crscls(**conf['controller']['tmp_storage'].get('config', {}))

def _get_app_storage_object(conf, arstorage_classes):
    arsname = conf['controller']['app_storage']['name']
    arscls = arstorage_classes[arsname]
    return arscls(**conf['controller']['app_storage'].get('config', {}))

def _get_controller_object(idx, app_name, project, crstorage, arstorage,
                           conf, controller_classes):
    cname = conf['controller']['name']
    ccls = controller_classes[cname]
    cobj = ccls(idx, app_name, project, crstorage, arstorage,
                **conf['controller'].get('config', {}))

    if not ccls.auto_filter:
        return cobj

    # dynamically decorate controller methods with filters
    # (if required and if there are any filters defined).
    try:
        filters = conf['controller']['filters']
        for method_name, filter_name in filters.iteritems():
            method = getattr(cobj, method_name)
            filter_decorator = import_object(filter_name)
            setattr(cobj, 'method_name', filter_decorator(method))
    except KeyError:
        pass
    finally:
        return cobj
