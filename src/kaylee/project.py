from abc import ABCMeta, abstractmethod

class Project(object):
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kwargs):
        self.nodes_config = {}
        self.tasks = iter(self)

    def __iter__(self):
        """ """
        return self

    def next(self):
        return self.__next__()

    @abstractmethod
    def __next__(self):
        """ """

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

    def validate(self, data):
        return True

    def normalize(self, data):
        return data
