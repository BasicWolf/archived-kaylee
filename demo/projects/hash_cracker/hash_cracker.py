# -*- coding: utf-8 -*-
from hashlib import md5
from kaylee import Project

class HashCrackerProject(Project):
    def __init__(self, *args, **kwargs):
        super(HashCrackerProject, self).__init__(*args, **kwargs)
        self.alphabet = kwargs['alphabet']
        self.key_length  = kwargs['key_length']
        self.hashes_per_task = kwargs['hashes_per_task']
        self.hash_to_crack = kwargs['hash_to_crack']
        self.salt = kwargs['salt']
        self.client_config.update({
            'md5_script' : kwargs['md5_script'],
            'alphabet' : self.alphabet,
            'key_length' : self.key_length,
            'hashes_per_task' : self.hashes_per_task,
        })

        self.tasks_count = ((len(self.alphabet) ** self.key_length)
                            // self.hashes_per_task + 1)
        self._tasks_counter = 0

    def next_task(self):
        if self._tasks_counter < self.tasks_count:
            task = self[self._tasks_counter]
            self._tasks_counter += 1
            return task
        else:
            return None

    def __getitem__(self, task_id):
        return {
            'id' : task_id,
            'hash_to_crack' : self.hash_to_crack,
            'salt' : self.salt
        }

    def normalize_result(self, task_id, data):
        key = data['cracked_key']
        if md5(key + self.salt).hexdigest() == self.hash_to_crack:
            return key
        raise ValueError('Invalid cracked hash key')

    def result_stored(self, task_id, data, storage):
        if len(storage) == 1:
            # it is enough to have a single result to complete the project
            self._announce_results(storage)
            self.completed = True

    def _announce_results(self, storage):
        key = list(storage.values())[0][0]
        print('The cracked hash key is: {}'.format(key))
