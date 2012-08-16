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

import kaylee.contrib.controllers
import kaylee.contrib.storages
import kaylee.contrib.registries
from .core import Kaylee
from .errors import KayleeError
from .util import LazyObject, import_object, CONFIG_FILTERS

# global (current module scope) holders of classes loaded
# via refresh()
_contrib_classes = {}
_controller_classes = {}
_registry_classes = {}
_pstorage_classes = {}
_tstorage_classes = {}
_project_classes = {}


class LazyKaylee(LazyObject):
    def _setup(self, obj = None):
        if isinstance(obj, Kaylee):
            self._wrapped = obj
        else:
            raise TypeError('obj must be an instance of {} not {}'
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
    elif isinstance(config, dict):
        config = { k : v for k, v in config.iteritems() if k == k.upper() }

    # at this point, if config is not a dict, then object type is wrong.
    if not isinstance(config, dict):
        raise TypeError('config must be an instance of {}, {}, {} or {} not {}'
                        .format(dict.__name__,
                                type.__name__,
                                types.ModuleType.__name__,
                                basestring.__name__,
                                type(obj).__name__))
    refresh(config)
    try:
        registry = _build_registry_object(config)
        apps = build_application_objects(config)
        return Kaylee(registry, apps, **config)
    except (KeyError, AttributeError) as e:
        raise KayleeError('Config error or object was not found: "{}"'
                          .format(e.args[0]))


def build_application_objects(config):
    """Loads Kaylee objects.

    :returns: Nodes configuration, nodes storage and applications.
    :rtype: (dict, :class:`NodesRegistry`, :class:`Applcations`)
    """

    apps = {}
    if 'APPLICATIONS' in config:
        for conf in config['APPLICATIONS']:
            app_name = conf['name']
            if not isinstance(app_name, basestring):
                raise KayleeError('Configuration error: app name {} is not a string'
                                  .format(app_name))

            # initialize objects
            project = _build_project_object(conf)
            controller = _build_controller_object(conf, app_name, project)
            # initialize store controller to local apps dict
            apps[app_name] = controller
    return apps

def _build_registry_object(conf):
    regcls = _registry_classes[conf['REGISTRY']['name']]
    return regcls(**conf['REGISTRY']['config'])

def refresh(config):
    """TODO: document me"""
    global _contrib_classes, _controller_classes, _registry_classes, \
        _pstorage_classes, _tstorage_classes, _project_classes

    from . import storage, controller, project, node
    _contrib_classes = _get_classes_from_module(kaylee.contrib.controllers,
                                                kaylee.contrib.storages,
                                                kaylee.contrib.registries)
    _controller_classes = _get_classes(_contrib_classes, controller.Controller)
    _registry_classes = _get_classes(_contrib_classes, node.NodesRegistry)
    _pstorage_classes = _get_classes(_contrib_classes,
                                     storage.PermanentStorage)
    _tstorage_classes = _get_classes(_contrib_classes, storage.TemporalStorage)

    # load classes from project modules
    _project_classes = {}
    if 'PROJECTS_DIR' in config:
        PDIR = config['PROJECTS_DIR']
        for sub_dir in os.listdir(PDIR):
            PDIR_PATH = os.path.join(PDIR, sub_dir)
            if not os.path.isdir(PDIR_PATH):
                continue
            if '__init__.py' not in os.listdir(PDIR_PATH):
                continue

            # looks like a python module
            try:
                pymod = importlib.import_module(sub_dir)
            except ImportError as e:
                raise ImportError('Unable to import project package: {}'
                                  .format(e))
            mod_cls = _get_classes_from_module(pymod)
            _project_classes.update(_get_classes(mod_cls, project.Project))
            _controller_classes.update(_get_classes(mod_cls, controller.Controller))
            _registry_classes.update(_get_classes(mod_cls, node.NodesRegistry))
            _pstorage_classes.update(
                _get_classes(mod_cls, storage.PermanentStorage))
            _tstorage_classes.update(
                _get_classes(mod_cls, storage.TemporalStorage))


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

def _build_project_storage_object(conf):
    if not 'storage' in conf['project']:
        return None
    psname = conf['project']['storage']['name']
    pscls = _pstorage_classes[psname]
    return pscls(**conf['project']['storage'].get('config', {}))

def _build_temporal_storage_object(conf):
    if not 'storage' in conf['controller']:
        return None
    tsname = conf['controller']['storage']['name']
    tscls = _tstorage_classes[tsname]
    return tscls(**conf['controller']['storage'].get('config', {}))

def _build_project_object(conf):
    pname = conf['project']['name']
    pcls = _project_classes[pname]
    pj_config = conf['project'].get('config', {})
    pj_storage = _build_project_storage_object(conf)
    return pcls(storage=pj_storage, **pj_config)

def _build_controller_object(conf, app_name, project):
    cname = conf['controller']['name']
    ccls = _controller_classes[cname]
    tstorage = _build_temporal_storage_object(conf)
    cobj = ccls(app_name, project, tstorage,
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
