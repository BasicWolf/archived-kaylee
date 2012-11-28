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

import kaylee.contrib
from .core import Kaylee
from .errors import KayleeError
from .util import LazyObject, import_object, CONFIG_FILTERS
from . import storage, controller, project, node, session

import logging
log = logging.getLogger(__name__)

# global (current module scope) holder of classes loaded
# via refresh() and retrieved via _get_class()
_classes = {}

_classes_types = [
    project.Project,
    controller.Controller,
    node.NodesRegistry,
    storage.PermanentStorage,
    storage.TemporalStorage,
    session.JSONSessionDataManager,
]


class LazyKaylee(LazyObject):
    def _setup(self, obj = None):
        if isinstance(obj, Kaylee):
            self._wrapped = obj
        elif obj is None:
            self._wrapped = None # release the object
            log.debug('Releasing {}'.format(obj))
        else:
            raise TypeError('obj must be an instance of {} or '
                            'a Kaylee config object, not {}'
                            .format(Kaylee.__name__, type(obj).__name__))


def load(config):
    """Loads Kaylee.

    :param config: Kaylee initial configuration object.
    :type config: dict, class, module or absolute Python module path.
    :returns: Kaylee object.
    """

    # check if python module path
    if isinstance(config, basestring):
        config = imp.load_source('kl_config', config)
    if isinstance(config, (type, types.ModuleType)):
        # convert to dict
        d = {}
        for attr in dir(config):
            if attr == attr.upper():
                d[attr] = getattr(config, attr)
        config = d
    if isinstance(config, dict):
        config = { k : v for k, v in config.iteritems() if k == k.upper() }

    # at this point, if config is not a dict, then object type is wrong.
    if not isinstance(config, dict):
        raise TypeError('config must be an instance of {}, {}, {} or {} not {}'
                        .format(dict.__name__,
                                type.__name__,
                                types.ModuleType.__name__,
                                basestring.__name__,
                                type(config).__name__))
    try:
        refresh(config)
        registry = _load_registry(config)
        apps = _load_applications(config)
    except (KeyError, AttributeError) as e:
        raise KayleeError('Config error or object was not found: "{}"'
                          .format(e.args[0]))

    return Kaylee(registry, apps, **config)


def refresh(config):
    # load classes from contrib (non-refreshable)
    _update_classes(kaylee.contrib)

    # load classes from project modules (refreshable for new modules only)
    if 'PROJECTS_DIR' in config:
        path = config['PROJECTS_DIR']
        for mod in _projects_modules(path):
            _update_classes(mod)
    else:
        log.warning('"PROJECTS_DIR" is not found in configuration."')


def _load_registry(conf):
    regcls = _registry_classes[conf['REGISTRY']['name']]
    return regcls(**conf['REGISTRY']['config'])


def _load_session_data_manager(config):
    if 'SESSION_DATA_MANAGER' not in config:
        return None
    clsname = config['SESSION_DATA_MANAGER']['name']
    sdmcls = _session_data_manager_classes[clsname]
    sdm_config = conf['SESSION_DATA_MANAGER'].get('config', {})
    return sdmcls(**sdm_config)


def _load_applications(config):
    apps = []
    if 'APPLICATIONS' in config:
        for conf in config['APPLICATIONS']:
            controller = _load_controller(conf)
            apps.append(controller)
    return apps


def _project_modules(path):
    """A generator which yields python modules found by given path."""
    for sub_dir in os.listdir(path):
        PDIR_PATH = os.path.join(PDIR, sub_dir)
        if not os.path.isdir(PDIR_PATH):
            continue
        if '__init__.py' not in os.listdir(PDIR_PATH):
            continue

        # looks like a python module
        try:
            pymod = importlib.import_module(sub_dir)
        except ImportError as e:
            raise ImportError('Unable to import project package "{}": {}'
                              .format(sub_dir, e))
        yield pymod


def _update_classes(module):
    """Updates the global _classes variable by the classes found in module."""
    global _classes
    for cls in  _get_classes_from_module(module):
        for cls_type in _classes_types:
            _classes.update(_get_classes(cls_type))


def _get_classes(classes, cls):
    """Returns a {'class_name' : class} dictionary, where each class
    is a subclass of the given cls argument.
    """
    ret = {}
    for c in (c for c in classes if issubclass (c, cls) and c is not cls ):
        ret[c.__name__] = c
    return ret


def _get_classes_from_module(*modules):
    """TODOC

    :returns: a list of classes loaded from the modules
    :rtype: list
    """
    ret = []
    for mod in modules:
        ret.extend(list( attr for attr in mod.__dict__.values()
                         if inspect.isclass(attr) ))
    return ret


def _load_permanent_storage(conf):
    psconf = conf['controller']['permanent_storage']
    clsname = psconf['name']
    pscls = _pstorage_classes[clsname]
    return pscls(**psconf.get('config', {}))


def _load_temporal_storage(conf):
    if not 'temporal_storage' in conf['controller']:
        return None
    tsconf = conf['controller']['temporal_storage']
    clsname = tsconf['name']
    tscls = _tstorage_classes[clsname]
    return tscls(**tsconf.get('config', {}))


def _load_project(conf):
    clsname = conf['project']['name']
    pcls = _project_classes[clsname]
    pj_config = conf['project'].get('config', {})
    return pcls(**pj_config)


def _load_controller(conf):
    # initialize objects
    clsname = conf['controller']['name']
    ccls = _controller_classes[clsname]
    app_name = conf['name']
    project = _load_project(conf)
    pstorage = _load_permanent_storage(conf)
    tstorage = _load_temporal_storage(conf)
    cobj = ccls(app_name, project, pstorage, tstorage,
                **conf['controller'].get('config', {}))

    if not ccls.auto_filter & CONFIG_FILTERS:
        return cobj

    # dynamically decorate controller methods with filters
    # (if required and if there are any filters defined).
    if 'filters' in conf['controller']:
        filters = conf['controller']['filters']
        for method_name, filters in filters.iteritems():
            method = getattr(cobj, method_name)
            for filter_name in filters:
                filter_decorator = import_object(filter_name)
            decorated = types.MethodType(filter_decorator(method.__func__),
                                         cobj, None)
            setattr(cobj, method_name, decorated)
    return cobj
