# -*- coding: utf-8 -*-
from hashlib import md5
from kaylee.project import Project, Task

func_table = {
    'md5' : lambda key, salt = None: md5(key),
    'md5(md5(k) + s)' : lambda key, salt : md5(md5(key).digest() + salt),
}


class HashCrackerProject(Project):
    def __init__(self, *args, **kwargs):
        super(HashCrackerProject, self).__init__(*args, **kwargs)
        self.alphabet = kwargs['alphabet']
        self.key_length  = kwargs['key_length']
        self.hash_func = kwargs['hash_func']
        self.hashes_per_task = kwargs['hashes_per_task']

    def __iter__(self):
        # TODO
        return self

    def __next__(self):
        # TODO
        raise StopIteration()

    def __getitem__(self, task_id):
        # TODO
        return Task(task_id)


    @property
    def hash_func(self):
        return self._hash_func

    @hash_func.setter
    def hash_func(self, val):
        if isinstance(val, basestring):
            self._hash_func = func_table[val]
        else:
            self._hash_func = val

