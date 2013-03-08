# -*- coding: utf-8 -*-
"""
    kaylee.loader
    ~~~~~~~~~~~~~

    Implements projects, controllers and Kaylee instance loader.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

# TODO: config -> settings
# TODO: refactor the whole thing and make a class out of it.
# TODO: refactor _projects_modules

import os
import imp
import importlib
import inspect
import types
from collections import defaultdict

import kaylee.contrib
from .core import Kaylee
from .errors import KayleeError
from .util import LazyObject, is_strong_subclass
from . import storage, controller, project, node, session

import logging
log = logging.getLogger(__name__)

# global (current module scope) cache of classes loaded
# via refresh() and retrieved via _get_class()
_classes = None # set in refresh()

_loadable_base_classes = [
    project.Project,
    controller.Controller,
    node.NodesRegistry,
    storage.PermanentStorage,
    storage.TemporalStorage,
    session.SessionDataManager,
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
                            'a Kaylee settings object, not {}'
                            .format(Kaylee.__name__, type(obj).__name__))


def load(settings):
    """Loads Kaylee.

    :param settings: Kaylee settings object.
    :type settings: dict, class, module or absolute Python module path.
    :returns: Kaylee object.
    """
    # Whatever the initial settings type is, load it (optional) and
    # convert it to a dictionary.
    # Note, that only settings with uppercase names' are loaded.
    if isinstance(settings, basestring):
        if os.path.exists(settings):
            settings = imp.load_source('kl_settings', settings)
    if isinstance(settings, (type, types.ModuleType)):
        d = {}
        for attr in dir(settings):
            if attr == attr.upper():
                d[attr] = getattr(settings, attr)
        settings = d
    if isinstance(settings, dict):
        settings = { k : v for k, v in settings.iteritems() if k == k.upper() }

    # at this point, if settings is not a dict, then object type is wrong.
    if not isinstance(settings, dict):
        raise TypeError('settings must be an instance of {}, {}, {} or {} not {}'
                        .format(dict.__name__,
                                type.__name__,
                                types.ModuleType.__name__,
                                basestring.__name__,
                                type(settings).__name__))

    try:
        refresh(settings)
        registry = load_registry(settings)
        sdm = load_session_data_manager(settings)
        apps = load_applications(settings)
    except (KeyError, AttributeError) as e:
        raise KayleeError('Settings error or object was not found: "{}"'
                          .format(e.args[0]))
    return Kaylee(registry = registry,
                  session_data_manager = sdm,
                  applications = apps,
                  **settings)


def refresh(settings):
    #pylint: disable-msg=W0603
    #W0603: Using the global statement

    # reset the classes cache
    global _classes
    _classes = defaultdict(dict)

    # load classes from contrib (non-refreshable)
    _update_classes(kaylee.contrib)
    # load session data managers
    _update_classes(kaylee.session)
    # load classes from project modules (refreshable for new modules only)
    if 'PROJECTS_DIR' in settings:
        projects_dir = settings['PROJECTS_DIR']
        for mod in _projects_modules(projects_dir):
            _update_classes(mod)
    else:
        log.warning('Settings does not contain a "PROJECTS_DIR" field.')


def load_registry(settings):
    clsname = settings['REGISTRY']['name']
    regcls = _classes[node.NodesRegistry][clsname]
    return regcls(**settings['REGISTRY']['config'])


def load_session_data_manager(settings):
    if 'SESSION_DATA_MANAGER' in settings:
        clsname = settings['SESSION_DATA_MANAGER']['name']
        sdmcls = _classes[session.SessionDataManager][clsname]
        try:
            sdm_config = settings['SESSION_DATA_MANAGER'].get('config', {})
        except KeyError:
            log.warning('Loading session data manager with empty config')
            sdm_config = {}
    else:
        # Load default (should be Phony) session data manager in case it
        # is not defined in settings.
        default_manager = session.KL_LOADER_DEFAULT_SESSION_DATA_MANAGER
        log.info('No session data manager loaded, using default: {}'
                 .format(default_manager))
        sdmcls = default_manager
        sdm_config = {}
    return sdmcls(**sdm_config)


def load_applications(settings):
    apps = []
    if 'APPLICATIONS' in settings:
        for conf in settings['APPLICATIONS']:
            ct = _load_controller(conf)
            apps.append(ct)
        log.info('{} applications have been loaded'.format(len(apps)))
    else:
        log.info('No applications have been loaded')
    return apps


def _projects_modules(path):
    """A generator which yields python modules found by given path."""
    for package_name in find_packages(path):
        try:
            pymod = importlib.import_module(package_name)
            yield pymod
        except ImportError as e:
            log.error('Unable to import project package "{}": {}'
                      .format(package_name, e))


def _update_classes(module):
    """Updates the global _classes variable by the classes found in module."""
    classes_from_module = get_classes_from_module(module)
    for base_class in _loadable_base_classes:
        # update _classes[base_class] with
        # { class_name : class } pairs, where `class` is a subclass of
        # `base_class`
        name_class_pairs = { c.__name__ : c for c in classes_from_module
                             if is_strong_subclass(c, base_class) }
        _classes[base_class].update(name_class_pairs)


def get_classes_from_module(module):
    return [attr for attr in module.__dict__.values()
            if inspect.isclass(attr)]

def find_packages(path):
    for sub_dir in os.listdir(path):
        pdir_path = os.path.join(path, sub_dir)
        if not os.path.isdir(pdir_path):
            continue
        if '__init__.py' not in os.listdir(pdir_path):
            continue
        yield sub_dir


def _load_permanent_storage(conf):
    psconf = conf['controller']['permanent_storage']
    clsname = psconf['name']
    pscls = _classes[storage.PermanentStorage][clsname]
    return pscls(**psconf.get('config', {}))


def _load_temporal_storage(conf):
    if not 'temporal_storage' in conf['controller']:
        return None
    tsconf = conf['controller']['temporal_storage']
    clsname = tsconf['name']
    tscls = _classes[storage.TemporalStorage][clsname]
    return tscls(**tsconf.get('config', {}))


def _load_project(conf):
    clsname = conf['project']['name']
    pcls = _classes[project.Project][clsname]
    pj_config = conf['project'].get('config', {})
    return pcls(**pj_config)


def _load_controller(conf):
    # initialize objects
    clsname = conf['controller']['name']
    ccls = _classes[controller.Controller][clsname]
    app_name = conf['name']
    pjobj = _load_project(conf)
    psobj = _load_permanent_storage(conf)
    tsobj = _load_temporal_storage(conf)
    cobj = ccls(app_name, pjobj, psobj, tsobj,
                **conf['controller'].get('config', {}))
    return cobj
