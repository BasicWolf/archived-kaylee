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
import types

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
    def _setup(self, obj = None):
        """
        Loads the settings module pointed to by the environment variable or
        the `obj` argument.
        """
        if obj is not None:
            if isinstance(obj, type):
                mod = obj
            else:
                raise TypeError('obj must be {} not {}'
                                .format(Settings.__name__, type(obj).__name__))
        else:
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

            mod = imp.load_source('settings', settings_path)

        # at this point *mod* is either a Python module or a Settings(-inherited) class
        self._wrapped = Settings()
        for setting in dir(mod):
            if setting == setting.upper():
                setting_value = getattr(mod, setting)
                setattr(self._wrapped, setting, setting_value)

    @property
    def configured(self):
        """Returns True if the settings have already been configured."""
        return self._wrapped is not None


class LazyKaylee(LazyObject):
    def _setup(self, obj = None):
        if obj is not None:
            from .app import Kaylee
            if isinstance(obj, Kaylee):
                self._wrapped = obj
                return
            else:
                raise TypeError('obj must be an instance of {} not {}'
                                .format(Kaylee.__name__, type(obj).__name__))
        else:
            self._wrapped = load()

def load(settings = None):
    from .app import Kaylee
    try:
        return Kaylee(*load_kaylee_objects(settings))
    except (KeyError, AttributeError) as e:
        raise KayleeError('Settings error or object was not found: '
                          ' "{}"'.format(e.args[0]))

def load_kaylee_objects(settings = None):
    """Loads Kaylee objects using configuration from settings.

    :param settings: Python module or class with Kaylee settings. If the value
            of settings is None, then the loader tries to load the
            settings using KAYLEE_SETTINGS_MODULE environmental
            variable.
    :returns: Nodes configuration, nodes storage and applications.
    :rtype: (dict, :class:`NodesStorage`, :class:`Applcations`)
    """
    from . import storage
    from . import controller
    from . import project
    from .app import Applications
    import kaylee.contrib.controllers
    import kaylee.contrib.storages
    if settings is None:
        from . import settings

    # -- scan for classes --
    project_classes = {}
    controller_classes = {}
    nstorage_classes = {}
    crstorage_classes = {}
    pstorage_classes = {}

    # load built-in kaylee classes
    ctrl_classes = _get_classes(controller, kaylee.contrib.controllers)
    stg_classes = _get_classes(storage, kaylee.contrib.storages)
    _store_classes(controller_classes, ctrl_classes, controller.Controller)
    _store_classes(nstorage_classes, stg_classes, storage.NodesStorage)
    _store_classes(pstorage_classes, stg_classes, storage.ProjectResultsStorage)
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
        mod_classes = _get_classes(pymod)
        _store_classes(project_classes, mod_classes, project.Project)
        _store_classes(controller_classes, mod_classes, controller.Controller)

    # load controllers/projects classes and initialize applications
    controllers = {}
    for conf in settings.APPLICATIONS:
        app_name = conf['name']
        if not isinstance(app_name, basestring):
            raise KayleeError('Configuration error: app name {} is not a string'
                              .format(app_name))

        # initialize objects
        project = _get_project_object(conf, project_classes, pstorage_classes)
        crstorage = _get_controller_storage_object(conf, crstorage_classes)
        controller = _get_controller_object(app_name, project, crstorage,
                                            conf, controller_classes)
        # initialize store controller to local controllers dict
        controllers[app_name] = controller
    applications = Applications(controllers)

    # build Kaylee nodes configuration
    nconfig = {
        'kl_worker_script' : settings.KAYLEE_WORKER_SCRIPT,
    }

    # initialize Kaylee objects
    nsname = settings.NODES_STORAGE['name']
    nscls = nstorage_classes[nsname]
    nstorage = nscls(**settings.NODES_STORAGE['config'])
    return nconfig, nstorage, applications


def _store_classes(dest, classes, cls):
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        dest[c.__name__] = c

def _get_classes(*modules):
    ret = []
    for mod in modules:
        ret.extend(list( attr for attr in mod.__dict__.values()
                         if inspect.isclass(attr) ))
    return ret

def _get_project_object(conf, project_classes, pstorage_classes):
    pname = conf['project']['name']
    pcls = project_classes[pname]
    pj_config = conf['project'].get('config', {})
    pj_storage = _get_project_storage_object(conf, pstorage_classes)
    return pcls(storage = pj_storage, **pj_config)

def _get_controller_storage_object(conf, crstorage_classes):
    if not 'storage' in conf['controller']:
        return None
    crsname = conf['controller']['storage']['name']
    crscls = crstorage_classes[crsname]
    return crscls(**conf['controller']['storage'].get('config', {}))

def _get_project_storage_object(conf, pstorage_classes):
    if not 'storage' in conf['project']:
        return None
    psname = conf['project']['storage']['name']
    pscls = pstorage_classes[psname]
    return pscls(**conf['project']['storage'].get('config', {}))

def _get_controller_object(app_name, project, crstorage, conf,
                           controller_classes):
    cname = conf['controller']['name']
    ccls = controller_classes[cname]
    cobj = ccls(app_name, project, crstorage,
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
            decorated = types.MethodType(filter_decorator(method.__func__),
                                         cobj, None)
            setattr(cobj, method_name, decorated)
    except KeyError as e:
        pass
    return cobj
