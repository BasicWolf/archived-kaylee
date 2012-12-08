# -*- coding: utf-8 -*-
"""
    kaylee.project
    ~~~~~~~~~~~~~~

    This module provides basic interfaces for Kaylee projects.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

from abc import abstractmethod

from .util import AutoFilterABCMeta, BASE_FILTERS, CONFIG_FILTERS
from .errors import KayleeError
from .filters import ignore_null_result


AUTO_PROJECT_MODE = 0x2
MANUAL_PROJECT_MODE = 0x4
KL_PROJECT_MODE = '__kl_project_mode__'
KL_PROJECT_SCRIPT = '__kl_project_script__'
KL_PROJECT_STYLES = '__kl_project_styles__'


class Project(object):
    """Kaylee Projects abstract base class.

    Metaclass: :class:`AutoFilterABCMeta <kaylee.util.AutoFilterABCMeta>`.

    :param script: The URL of the project's client part (\*.js file).
    """
    __metaclass__ = AutoFilterABCMeta
    auto_filter = BASE_FILTERS | CONFIG_FILTERS
    auto_filters = {
        'normalize_result' : [ignore_null_result, ],
    }

    #: Project mode.
    mode = AUTO_PROJECT_MODE

    def __init__(self, script, *args, **kwargs):
        #: A dictionary wi]th configuration
        #: details used by every client-side node. If the project is loaded
        #: via a configuration object ``client_config`` is extended by
        #: ``project.config`` section's value (see :ref:`loading`).
        self.client_config = {
            KL_PROJECT_SCRIPT : script,
            KL_PROJECT_MODE   : self.mode,
            KL_PROJECT_STYLES : kwargs.get('styles', None)
        }
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

    @abstractmethod
    def normalize_result(self, task_id, result):
        """Validates and normalizes the result.

        :param task_id: The ID of the task.
        :param result: The result to be validated and normalized.
        :throws ValueError: If the data is invalid.
        :return: normalized result.
        """

    def result_stored(self, task_id, data, storage):
        """A callback invoked by the bound controller when
        a result is successfully stored to a permanent storage.

        :param task_id: Task ID.
        :param data: Task results.
        :param storage: Application's permanent results storage
        :type data: dict or list (parsed JSON)
        :type storage: :class:`PermanentStorage`
        """
        pass
