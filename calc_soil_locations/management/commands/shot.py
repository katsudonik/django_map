# -*- coding:utf-8 -*-


from django.core.management.base import BaseCommand
from django.conf import settings
from modules.screenshot import shot_jpg

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('task_id', nargs='+', type=int)

    def handle(self, *args, **options):
        print(options['task_id'])
        for task_id in options['task_id']:
            shot_jpg(
                settings.SOIL_LOCATIONS['default']['url'] + '?task_id=' + str(task_id),
                settings.SOIL_LOCATIONS['default']['width'],
                settings.SOIL_LOCATIONS['default']['height'],
                settings.SOIL_LOCATIONS['default']['quality'],
                settings.SOIL_LOCATIONS['default']['image_dir'] + str(task_id)
            )
