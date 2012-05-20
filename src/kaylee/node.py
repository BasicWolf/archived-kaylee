# -*- coding: utf-8 -*-
from datetime import datetime

class Node(object):
    __slots__ = ('id', '_task_id', 'subscription_timestamp', 'task_timestamp',
                 'controller')

    def __init__(self, node_id):
        self.id = node_id
        self._task_id = None
        self.subscription_timestamp = None
        self.task_timestamp = None
        self.controller = None

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, val):
        self._task_id = val
        self.task_timestamp = datetime.now()

    def __hash__(self):
        return hash(self.id)
