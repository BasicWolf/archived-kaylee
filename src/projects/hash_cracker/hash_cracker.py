# -*- coding: utf-8 -*-
from hashlib import md5
from kaylee import Project, Task

func_table = {
    'md5' : lambda key, salt = None: md5(key),
    'md5(md5(k) + s)' : lambda key, salt : md5(md5(key).digest() + salt),
}


class HashCrackerProject(Project):
    def __init__(self, *args, **kwargs):
        super(HashCrackerProject, self).__init__(*args, **kwargs)
        self.alphabet = kwargs['alphabet']
        self.key_length  = kwargs['key_length']
        self._hash_func_name = ''
        self.hash_func = kwargs['hash_func']
        self.hashes_per_task = kwargs['hashes_per_task']
        self.hash_to_crack = kwargs['hash_to_crack']
        self.salt = kwargs['salt']
        self.tasks_count = len(self.alphabet) ** self.key_length / self.hashes_per_task + 1
        self.nodes_config.update({
                'alphabet' : self.alphabet,
                'key_length' : self.key_length,
                'hash_func' : self._hash_func_name,
                'hashes_per_task' : self.hashes_per_task,
                })

    def __iter__(self):
        self._tasks_counter = -1
        return self

    def __next__(self):
        if self._tasks_counter < self.tasks_count:
            self._tasks_counter += 1
            return self[self._tasks_counter]
        else:
            raise StopIteration()

    def __getitem__(self, task_id):
        return HashCrackerTask(task_id, self.hash_to_crack, salt)

    @property
    def hash_func(self):
        return self._hash_func

    @hash_func.setter
    def hash_func(self, val):
        if isinstance(val, basestring):
            self._hash_func_name = val
            self._hash_func = func_table[val]
        else:
            self._hash_func_name = val.__name__
            self._hash_func = val


class HashCrackerTask(Task):
    serializable = ['hash_to_crack', 'salt']

    def __init__(self, task_id, hash_to_crack, salt):
        super(HashCrackerTask, self).__init__(task_id)
        self.hash_to_crack = hash_to_crack
        self.salt = salt
