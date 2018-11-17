# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from modules.screenshot import shot_jpg
from calc_soil_locations.models import SoilDisposalTask
import string
import random
import os
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('task_id', nargs='+', type=int)
    def handle(self, *args, **options):
        print(options['task_id'])
        for task_id in options['task_id']:
            img_dir = settings.SOIL_LOCATIONS['default']['image_dir']
            os.makedirs(img_dir, exist_ok=True)
            file_name = self.random_character(10)
            img_path = img_dir + file_name
            
            shot_jpg(
                settings.SOIL_LOCATIONS['default']['url'] + '?task_id=' + str(task_id),
                settings.SOIL_LOCATIONS['default']['width'],
                settings.SOIL_LOCATIONS['default']['height'],
                settings.SOIL_LOCATIONS['default']['quality'],
                img_path,
                settings.PHANTOM_JS['path']
            )
        
            task = self.fetch_task(task_id)
            task.file_name = file_name + '.jpg'
            task.updated_at = timezone.now()
            task.save()
    def fetch_task(self, task_id):
        task = SoilDisposalTask.objects.filter(id=task_id).first()
        if task is None:
            raise UnboundLocalError
        if task.at_time_field_latitude is None:
            raise UnboundLocalError
        if task.at_time_field_longitude is None:
            raise UnboundLocalError
        if task.at_time_soil_disposal_site_latitude is None:
            raise UnboundLocalError
        if task.at_time_soil_disposal_site_longitude is None:
            raise UnboundLocalError
        return task
    def random_character(self, n):
        c = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join([random.choice(c) for i in range(n)])
