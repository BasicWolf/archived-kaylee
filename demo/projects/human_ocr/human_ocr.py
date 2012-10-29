# -*- coding: utf-8 -*-
import os
import errno
import random
import tempfile
import Image, ImageFont, ImageDraw

from kaylee import Project, Task
from kaylee.project import MANUAL_PROJECT_MODE, attach_session_data
from kaylee.util import random_string

LIPSUM = "Lorem ipsum dolor sit amet"

class HumanOCRProject(Project):
    mode = MANUAL_PROJECT_MODE

    def __init__(self, *args, **kwargs):
        super(HumanOCRProject, self).__init__(*args, **kwargs)
        self.font_path = kwargs['font_path']
        self.img_dir = kwargs['img_dir']
        self.img_dir_url = kwargs['img_dir_url']

        self.lipsum_words = LIPSUM.split(' ')
        self.tasks_count = len(self.lipsum_words)
        self._tasks_counter = -1

        try:
            os.makedirs(self.img_dir)
        except OSError as e:
            # pass 'file exists' error
            if e.errno != errno.EEXIST:
                raise e

    def next_task(self):
        if self._tasks_counter < self.tasks_count:
            self._tasks_counter += 1
            return self[self._tasks_counter]
        else:
            return None

    def __getitem__(self, task_id):
        word = self.lipsum_words[task_id]
        return HumanOCRTask(task_id, word, self.font_path, self.img_dir,
                            self.img_dir_url)
    @attach_session_data
    def normalize(self, task_id, data):
        if data['captcha'].lower() != data['random_string'].lower():
            
        return data


class HumanOCRTask(Task):
    serializable = ['url', '#random_string']

    def __init__(self, task_id, text, font_path, img_dir, img_url_dir):
        super(HumanOCRTask, self).__init__(task_id)
        self.random_string = random_string(4)
        img = self._generate_image(text, font_path)
        img_path = self._save_image(img, img_dir)
        self.url = os.path.join(img_url_dir, os.path.basename(img_path))

    def _save_image(self, image, img_dir):
        # removing the temp file should be done via e.g. cron job
        fd, fpath = tempfile.mkstemp(suffix='.png', prefix=img_dir)
        f = os.fdopen(fd, 'w')
        image.save(f, 'PNG')
        f.close()
        return fpath

    def _generate_image(self, text, font_path):
        text += ' ' + self.random_string
        font = ImageFont.truetype(font_path, 48)
        size = font.getsize(text)
        size = (int(size[0]), int(size[1]))

        # a blank image with white background
        image = Image.new('RGB', size, '#FFF')
        draw = ImageDraw.Draw(image)

        draw.text((0, 0), text, font=font, fill='#000000')

        # add white noise
        noise = []
        for x in range (0, size[0]):
            for y in range (0, size[1]):
                if random.random() > 0.3:
                    noise.append((x, y))
        draw.point(noise, '#FFF')

        return image

