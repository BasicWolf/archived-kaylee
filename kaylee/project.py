# -*- coding: utf-8 -*-
"""
    kaylee.project
    ~~~~~~~~~~~~~~

    This module provides basic interfaces for Kaylee projects.

    :copyright: (c) 2012 by Zaur Nasibov.
    :license: MIT, see LICENSE for more details.
"""

from abc import ABCMeta, abstractmethod


#: Defines auto project mode (see :attr:`Project.mode`)
AUTO_PROJECT_MODE = 0x2

#: Defines manual project mode (see :attr:`Project.mode`)
MANUAL_PROJECT_MODE = 0x4

#: Defines the unknown amount of tasks to be solved by a Kaylee
#: application.
UNKNOWN_AMOUNT = 0x1

KL_PROJECT_MODE = '__kl_project_mode__'
KL_PROJECT_SCRIPT_URL = '__kl_project_script_url__'
KL_PROJECT_STYLES = '__kl_project_styles__'



class Project(object):
    """Kaylee Projects abstract base class.

    :param script_url: The URL of the project's client part (\\*.js file).
    :param mode: defines :attr:`Project.mode <kaylee.Project.mode>`.
    """
    __metaclass__ = ABCMeta

    def __init__(self, script_url, mode, **kwargs):
        if mode not in [AUTO_PROJECT_MODE, MANUAL_PROJECT_MODE]:
            raise ValueError('Wrong project mode: {}'.format(mode))

        #: Indicates the mode in which project works on the client side.
        #: Available modes:
        #:
        #: * :data:`AUTO_PROJECT_MODE <kaylee.project.AUTO_PROJECT_MODE>`
        #: * :data:`MANUAL_PROJECT_MODE <kaylee.project.MANUAL_PROJECT_MODE>`
        #:
        #: For detailed description and usage see :ref:`projects_modes`.
        self.mode = mode

        #: A dictionary which contains the configuration passed to the
        #: client-side of the project in :js:func:`pj.init`.
        #: If the project is loaded from a :ref:`configuration object
        #: <loading>` the base value of ``client_config`` is extended by
        #: ``project.config`` configuration section.
        #:
        #: .. note:: Initially ``Project.client_config`` contains only the
        #:           data necessary to properly initialize the client-side
        #:           of the project.
        self.client_config = {
            KL_PROJECT_SCRIPT_URL: script_url,
            KL_PROJECT_MODE: self.mode,
            KL_PROJECT_STYLES: kwargs.get('styles', None),
        }

        #: Indicates whether the project was completed.
        self.completed = False

    @abstractmethod
    def next_task(self):
        """Returns the next task. The returned ``None`` value indicates that
        there will be no more new tasks from the project, but the bound
        controller can still refer to the old tasks via ``project[task_id]``.

        :returns: task :class:`dict` or ``None``.
        """

    @abstractmethod
    def __getitem__(self, task_id):
        """Returns a task with the required id. A task is simply
        a :class:`dict` with at least an 'id' key in it::

          {
              'id' : '10',
              'somedata' : somevalue,
              # etc.
          }

        :rtype: :class:`dict`
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

        :param task_id: Task ID
        :param data: Normalized task result
        :param storage: The application's permanent results storage
        :type storage: :class:`PermanentStorage`
        """
        pass

    # @abstractproperty
    # def progress(self):
    #     """A tuple of 2 items indicating progress:
    #     ``(amount_of_tasks_completed, total_amount_of_tasks)``

    #     A negative (:data:`UNKNOWN_AMOUNT`) value of the second item in
    #     the tuple indicates that the project is not able to calculate the
    #     total amount of tasks.
    #     """
    #     pass
