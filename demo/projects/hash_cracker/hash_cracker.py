# -*- coding: utf-8 -*-
from hashlib import md5
from kaylee import Project, Task

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
        self._tasks_counter = -1


    def next_task(self):
        if self._tasks_counter < self.tasks_count:
            self._tasks_counter += 1
            return self[self._tasks_counter]
        else:
            return None

    def __getitem__(self, task_id):
        return HashCrackerTask(task_id, self.hash_to_crack, self.salt)

    def normalize(self, task_id, key):
        try:
            if md5(key + self.salt).hexdigest() == self.hash_to_crack:
                return key
        except KeyError:
            raise ValueError('Required data is missing')
        raise ValueError('Invalid hash key')

    def store_result(self, task_id, data):
        super(HashCrackerProject, self).store_result(task_id, data)
        if len(self.storage) == 1:
            # it is enough to have a single result to complete the project
            self._announce_results()
            self.completed = True

    def _announce_results(self):
        key = list(self.storage.values())[0][0]
        print('The cracked hash key is: {}'.format(key))



class HashCrackerTask(Task):
    serializable = ['hash_to_crack', 'salt']

    def __init__(self, task_id, hash_to_crack, salt):
        super(HashCrackerTask, self).__init__(task_id)
        self.hash_to_crack = hash_to_crack
        self.salt = salt
