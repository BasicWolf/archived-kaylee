# -*- coding: utf-8 -*-
"""
    kaylee.loader
    ~~~~~~~~~~~~~

    Implements projects, controllers and Kaylee instance loader.

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

#: Points to the environmental variable which holds the absolute path to the
#: settings `*.py` file.
SETTINGS_ENV_VAR = 'KAYLEE_SETTINGS_MODULE'


class Settings(object):
    """Settings class documentation"""
    nodes_config_settings = set([
            'KAYLEE_WORKER_SCRIPT',
            'AUTO_GET_NEXT_ACTION_ON_ACCEPT_RESULTS',
            ])

    #: Field description
    AUTO_GET_NEXT_ACTION_ON_ACCEPT_RESULTS = True

    def __init__(self):
        self._locked = False

    def validate(self):
        pass


class LazySettings(LazyObject):
    """
    A lazy proxy for either global Kaylee settings. Uses either a custom
    object or the settings module pointed to by :py:data:`SETTINGS_ENV_VAR`.
    """
    def _setup(self, obj = None):
        """
        Loads and wraps the settings module pointed to by the environment
        variable or the `obj` argument.

        :param obj: Python module or class with settings attributes.
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

        # at this point *mod* is either a Python module or a class
        # with settings as attributes
        self._wrapped = Settings()

        # load settings from module or class if any
        for setting in dir(mod):
            if setting == setting.upper():
                value = getattr(mod, setting)
                setattr(self._wrapped, setting, value)


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
    """Loads Kaylee.

    :param settings: Python module or class with Kaylee settings. If the value
            of settings is None, then the loader tries to load the
            settings using KAYLEE_SETTINGS_MODULE environmental
            variable.
    :returns: Kaylee object.
    """
    from .app import Kaylee
    try:
        if settings is None:
            from . import settings
        return Kaylee(*load_kaylee_objects(settings))
    except (KeyError, AttributeError) as e:
        raise KayleeError('Settings error or object was not found: '
                          ' "{}"'.format(e.args[0]))

def load_kaylee_objects(settings):
    """Loads Kaylee objects.

    :returns: Nodes configuration, nodes storage and applications.
    :rtype: (dict, :class:`NodesRegistry`, :class:`Applcations`)
    """
    from . import storage, controller, project, node
    from .app import Applications
    import kaylee.contrib.controllers
    import kaylee.contrib.storages
    import kaylee.contrib.registries

    # load contrib classes
    contrib_cls = _get_classes_from_module(kaylee.contrib.controllers,
                                           kaylee.contrib.storages,
                                           kaylee.contrib.registries)

    controller_classes = _get_classes(contrib_cls, controller.Controller)
    nregistry_classes = _get_classes(contrib_cls, node.NodesRegistry)
    pstorage_classes = _get_classes(contrib_cls, storage.ProjectResultsStorage)
    crstorage_classes = _get_classes(contrib_cls,
                                     storage.ControllerResultsStorage)

    # load classes from project modules
    project_classes = {}
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
        mod_cls = _get_classes_from_module(pymod)
        project_classes.update(_get_classes(mod_cls, project.Project))
        controller_classes.update(_get_classes(mod_cls, controller.Controller))
        nregistry_classes.update(_get_classes(mod_cls, node.NodesRegistry))
        pstorage_classes.update(
            _get_classes(mod_cls, storage.ProjectResultsStorage))
        crstorage_classes.update(
            _get_classes(mod_cls, storage.ControllerResultsStorage))

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

    # initialize objects to return
    nconfig = { key : getattr(settings, key)
                for key in Settings.nodes_config_settings }
    applications = Applications(controllers)

    nsname = settings.NODES_STORAGE['name']
    nrcls = nregistry_classes[nsname]
    nreg = nrcls(**settings.NODES_STORAGE['config'])
    return nconfig, nreg, applications


def _get_classes(classes, cls):
    """Returns a {'class_name' : class} dictionary, where each class
    is a subclass of the given cls argument.
    """
    ret = {}
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        ret[c.__name__] = c
    return ret

def _get_classes_from_module(*modules):
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
