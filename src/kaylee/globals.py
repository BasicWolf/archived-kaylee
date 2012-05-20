# -*- coding: utf-8 -*-
"""
    kaylee.globals
    ~~~~~~~~~~~~~

    Defines all global objects

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: GPL, see LICENSE for more details.
"""
import os
import imp
from .loader import load_kaylee

# GLOBALS 
settings = imp.load_source('settings', os.environ['KAYLEE_SETTINGS_PATH'])
dispatcher = load_kaylee(settings)
applications = dispatcher.applications # just a 'shortcut' to apps
