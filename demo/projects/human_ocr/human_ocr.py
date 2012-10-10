# -*- coding: utf-8 -*-
import os
import random
import tempfile
import Image, ImageFont, ImageDraw

import kaylee
from kaylee.util import random_string

LIPSUM = "Lorem ipsum dolor sit amet"

class HumanOCRProject(kaylee.Project):
    def __init__(self, *args, **kwargs):
        super(HumanOCRProject, self).__init__(*args, **kwargs)
        self.font_path = kwargs['font_path']
        self.img_dir = kwargs['img_dir']
        self.img_dir_url = kwargs['img_dir_url']

        self.lipsum_words = LIPSUM.split(' ')
        self.tasks_count = len(lipsum_words)
        self._tasks_counter = -1


    def get_next_task(self):
        if self._tasks_counter < self.tasks_count:
            self._tasks_counter += 1
            return self[self._tasks_counter]
        else:
            return None

    def __getitem__(self, task_id):
        word = self.lipsum_words[task_id]
        return HumanOCRTask(task_id, word, self.font_path, self.img_dir,
                            self.img_url_dir)


class HumanOCRTask(kaylee.Task):
    serializable = ['#random_string']

    def __init__(self, task_id, text, font_path, img_dir, img_url_dir):
        super(HumanOCRTask, self).__init__(task_id)
        self.random_string = random_string(4)
        img = self._generate_image(text, font_path)
        self._save_image(img, img_dir)

    def _save_image(self, image, path):
        tempfile.mkstemp(path)
        image.save(path)

    def _generate_image(self, text, font_path):
        text += ' ' + self.random_string
        font = ImageFont.truetype(self.font_path, 16)
        size = font.getsize(text)
        size = (int(size[0]), int(size[1] - size[1]*0.2))

        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)
        noise = []
        for x in range (0, 300):
            for y in range (0, 300):
                if rnd_task.random() > 0.5:
                    noise.append((x, y))

        draw.point(noise, (255, 255, 255))
        draw.text((0, 0), text, font=font, fill="#000000")

