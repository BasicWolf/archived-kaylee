# -*- coding: utf-8 -*-
"""
    kaylee.project
    ~~~~~~~~~~~~~~

    This module provides basic interfaces for Kaylee projects.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

from abc import abstractmethod
from functools import wraps
from copy import deepcopy

from .util import (AutoFilterABCMeta, BASE_FILTERS, CONFIG_FILTERS,
                   get_secret_key, encrypt, decrypt)
from .errors import KayleeError

AUTO_PROJECT_MODE = 0x2
MANUAL_PROJECT_MODE = 0x4

KL_RESULT = '__kl_result__'
KL_PROJECT_MODE = '__kl_project_mode__'
KL_PROJECT_SCRIPT = '__kl_project_script__'
KL_PROJECT_STYLES = '__kl_project_styles__'

SESSION_DATA_ATTRIBUTE = '__kl_tsd__'

### Auto filters ###

def ignore_null_result(f):
    """Ignores ``None`` data by **not** calling the wrapped method.

    .. note:: This is a base filter applied to :meth:`Project.normalize_result`
              and :meth:`Project.store_result`.
    """
    @wraps(f)
    def wrapper(self, task_id, data):
        if data is not None:
            return f(self, task_id, data)
        return None
    return wrapper


def attach_session_data(f):
    """Automatically decrypts session data and attaches it to the results.

    The filter can be effectively applied to Project.normalize_result() in
    order to handle the project tasks' session data. The filter works as
    follows:

    1. Get encrypted session data from the incoming results (dict)
    2. Decrypt session data -> dict
    3. Update the results with the session data
    4. Remove the encrypted session data from the results dict.
    """
    @wraps(f)
    def wrapper(self, task_id, data):
        if not isinstance(data, dict):
            raise ValueError('Cannot attach session data to a non-dict result')
        sd = deserialize(data[SESSION_DATA_ATTRIBUTE])
        data.update(sd)
        return f(self, task_id, data)
    return wrapper


def attach_task_id_to_returned_value(f):
    """TODOC, TODO:TEST"""
    @wraps(f)
    def wrapper(self, task_id):
        res = f(self, task_id)
        res['id'] = task_id
        return res
    return wrapper


def returns_session_data(f):
    """TODOC, TODO:TEST"""
    @wraps(f)
    def wrapper(self, task_id):
        task = f(self, task_id)
        hashed_data = { key : task[key] for key in task
                        if key.startswith('#') }
        # encrypt and attach data to the task
        task[SESSION_DATA_ATTRIBUTE] = encrypt(hashed_data)
        # remove the just encrypted key-value pairs, as they are
        # no longer required
        for key in hashed_data:
            del task[key]
        return task
    return wrapper


class Project(object):
    """Kaylee Projects abstract base class.

    Metaclass: :class:`AutoFilterABCMeta <kaylee.util.AutoFilterABCMeta>`.

    :param script: The URL of the project's client part (\*.js file).
    :param storage: Permanent results storage.
    :type storage: :class:`PermanentStorage`
    """
    __metaclass__ = AutoFilterABCMeta
    auto_filter = BASE_FILTERS | CONFIG_FILTERS
    auto_filters = {
        'normalize_result' : [ignore_null_result, ],
        'store_result' : [ignore_null_result, ],
        '__getitem__' : [attach_task_id_to_returned_value, ],
    }

    #: Project mode.
    mode = AUTO_PROJECT_MODE

    def __init__(self, script, storage, *args, **kwargs):
        #: A dictionary wi]th configuration
        #: details used by every client-side node. If the project is loaded
        #: via a configuration object ``client_config`` is extended by
        #: ``project.config`` section's value (see :ref:`loading`).
        self.client_config = {
            KL_PROJECT_SCRIPT : script,
            KL_PROJECT_MODE   : self.mode,
            KL_PROJECT_STYLES : kwargs.get('styles', None)
        }
        #: Project's permanent results storage (an instance of
        #: :class:`PermanentStorage` subclass).
        self.storage = storage
        #: Indicates whether the project was completed.
        self.completed = False

    @abstractmethod
    def next_task(self):
        """
        TODOC
        Returns the next task. The returned ``None`` value indicates that
        there will be no more new tasks from the project, but the bound
        controller can still refer to the old tasks via ``project[task_id]``.

        :returns: an instance of :class:`Task` or ``None``.
        """

    @abstractmethod
    def __getitem__(self, task_id):
        """TODOC:
        Returns a task with the required id.

        :rtype: :class:`Task`
        """

    def normalize_result(self, task_id, data):
        """Normalizes and validates a solution.

        :param task_id: the ID of the task.
        :param data: the solution to be validated and/or normalized.
        :throws ValueError: if the data is invalid.
        :return: normalized data.
        """
        return data


    def store_result(self, task_id, data):
        """Stores the results to the permanent storage.

        :param task_id: Task ID.
        :param data: Task results.
        :type data: dict or list (parsed JSON)
        """
        self.storage.add(task_id, data)
