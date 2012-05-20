from abc import ABCMeta, abstractmethod

class Project(object):
    __metaclass__ = ABCMeta
    def __init__(self, *args, **kwargs):
        self.nodes_config = {}
        self.tasks = iter(self)

    def __iter__(self):
        """ """
        return self

    def __next__(self):
        """ """
        raise StopIteration()

    def next(self):
        return self.__next__()

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

