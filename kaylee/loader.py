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
from copy import deepcopy
from collections import defaultdict

import kaylee.contrib
from .core import Kaylee
from .errors import KayleeError
from .util import LazyObject, is_strong_subclass
from . import storage, controller, project, node, session

import logging
log = logging.getLogger(__name__)

_default_settings = {
    'AUTO_GET_ACTION' : True,
}


class LazyKaylee(LazyObject):
    def _setup(self, obj = None):
        if isinstance(obj, Kaylee):
            self._wrapped = obj
        elif obj is None:
            self._wrapped = None # release the object
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
        settings = {k : v for k, v in settings.iteritems() if k == k.upper()}

    # at this point, if settings is not a dict, then object type is wrong.
    if not isinstance(settings, dict):
        raise TypeError('settings must be an instance of '
                        '{}, {}, {} or {} not {}'.format(
                            dict.__name__,
                            type.__name__,
                            types.ModuleType.__name__,
                            basestring.__name__,
                            type(settings).__name__))

    new_settings = deepcopy(_default_settings)
    new_settings.update(settings)
    try:
        loader = Loader(new_settings)
        registry = loader.registry
        sdm = loader.session_data_manager
        apps = loader.applications
    except (KeyError, AttributeError) as e:
        raise KayleeError('Settings error or object was not found: "{}"'
                          .format(e.args[0]))
    return Kaylee(registry=registry,
                  session_data_manager=sdm,
                  applications=apps,
                  **settings)



class Loader(object):
    _loadable_base_classes = [
        project.Project,
        controller.Controller,
        node.NodesRegistry,
        storage.PermanentStorage,
        storage.TemporalStorage,
        session.SessionDataManager,
    ]

    def __init__(self, settings):
        self._classes = defaultdict(dict)
        self._settings = settings

        # load classes from contrib (non-refreshable)
        self._update_classes(kaylee.contrib)
        # load session data managers
        self._update_classes(kaylee.session)
        # load classes from project modules (refreshable for new modules only)
        if 'PROJECTS_DIR' in settings:
            projects_dir = settings['PROJECTS_DIR']
            for mod in find_modules(projects_dir):
                self._update_classes(mod)

    @property
    def registry(self):
        settings = self._settings
        clsname = settings['REGISTRY']['name']
        regcls = self._classes[node.NodesRegistry][clsname]
        return regcls(**settings['REGISTRY']['config'])

    @property
    def session_data_manager(self):
        settings = self._settings
        if 'SESSION_DATA_MANAGER' in settings:
            clsname = settings['SESSION_DATA_MANAGER']['name']
            sdmcls = self._classes[session.SessionDataManager][clsname]
            sdm_config = settings['SESSION_DATA_MANAGER'].get('config', {})
        else:
            # Load default (should be Phony) session data manager in case it
            # is not defined in settings.
            default_manager = session.KL_LOADER_DEFAULT_SESSION_DATA_MANAGER
            sdmcls = default_manager
            sdm_config = {}
        return sdmcls(**sdm_config)

    @property
    def applications(self):
        settings = self._settings
        apps = []
        if 'APPLICATIONS' in settings:
            for conf in settings['APPLICATIONS']:
                ct = self._load_controller(conf)
                apps.append(ct)
        return apps

    def _update_classes(self, module):
        """Updates the _classes field by the classes found in
        the module."""
        classes_from_module = get_classes_from_module(module)
        for base_class in self._loadable_base_classes:
            # update _classes[base_class] with
            # { class_name : class } pairs, where `class` is a subclass of
            # `base_class`
            name_class_pairs = {c.__name__ : c for c in classes_from_module
                                if is_strong_subclass(c, base_class)}
            self._classes[base_class].update(name_class_pairs)

    def _load_permanent_storage(self, conf):
        psconf = conf['controller']['permanent_storage']
        clsname = psconf['name']
        pscls = self._classes[storage.PermanentStorage][clsname]
        return pscls(**psconf.get('config', {}))

    def _load_temporal_storage(self, conf):
        if not 'temporal_storage' in conf['controller']:
            return None
        tsconf = conf['controller']['temporal_storage']
        clsname = tsconf['name']
        tscls = self._classes[storage.TemporalStorage][clsname]
        return tscls(**tsconf.get('config', {}))

    def _load_project(self, conf):
        clsname = conf['project']['name']
        pcls = self._classes[project.Project][clsname]
        pj_config = conf['project'].get('config', {})
        return pcls(**pj_config)

    def _load_controller(self, conf):
        # initialize objects
        clsname = conf['controller']['name']
        ccls = self._classes[controller.Controller][clsname]
        app_name = conf['name']
        pjobj = self._load_project(conf)
        psobj = self._load_permanent_storage(conf)
        tsobj = self._load_temporal_storage(conf)

        cobj = ccls(app_name, pjobj, psobj, tsobj,
                    **conf['controller'].get('config', {}))
        return cobj


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

def find_modules(path):
    """A generator which yields python modules found in the given path."""
    for package_name in find_packages(path):
        try:
            pymod = importlib.import_module(package_name)
            yield pymod
        except ImportError as e:
            log.error('Unable to import project package "{}": {}'
                      .format(package_name, e))
